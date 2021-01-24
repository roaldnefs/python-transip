# -*- coding: utf-8 -*-
#
# Copyright (C) 2020, 2021 Roald Nefs <info@roaldnefs.com>
#
# This file is part of python-transip.
#
# python-transip is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-transip is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-transip.  If not, see <https://www.gnu.org/licenses/>.
"""Wrapper for the TransIP API."""

from typing import Dict, Optional, Any, Type, Union, TYPE_CHECKING
from types import ModuleType

import importlib
import requests
import os

from transip.exceptions import TransIPHTTPError, TransIPParsingError
from transip.utils import generate_message_signature, generate_nonce


__title__ = "python-transip"
__version__ = "0.4.0"
__author__ = "Roald Nefs"
__email__ = "info@roaldnefs.com"
__copyright__ = "Copyright 2020-2021, Roald Nefs"
__license__ = "LGPL3"


if TYPE_CHECKING:
    # Imports only needed for type checking. These will not be imported at
    # runtime.
    from transip.base import ApiService


class TransIP:
    """Represents a TransIP server connection.

    Args:
        login (str): The TransIP username
        api_version (str): TransIP API version to use
        access_token (str): The TransIP API access token
        private_key (str): The content of the private key for accessing the
            TransIP API
        private_key_file (str): Path to the private key for accessing the
            TransIP API
    """

    def __init__(
        self,
        login: str = None,
        api_version: str = "6",
        access_token: Optional[str] = None,
        private_key: Optional[str] = None,
        private_key_file: Optional[str] = None,
    ) -> None:
        self._api_version: str = api_version
        self._url: str = f"https://api.transip.nl/v{api_version}"

        # Headers to use when making a request to TransIP
        self.headers: Dict[str, str] = {
            "User-Agent": f"{__title__}/{__version__}"
        }

        # Initialize a session object for making requests
        self.session: requests.Session = requests.Session()

        # Set authentication information
        self._login: Optional[str] = login
        self._access_token: Optional[str] = access_token
        self._private_key: Optional[str] = private_key
        self._private_key_file: Optional[str] = private_key_file
        self._set_auth_info()

        # Dynamically import the services for the specified API version
        objects: ModuleType = (
            importlib.import_module(f"transip.v{api_version}.objects")
        )

        self.api_test: Type['ApiService'] = (
            objects.ApiTestService(self)  # type: ignore
        )
        self.availability_zones: Type['ApiService'] = (
            objects.AvailabilityZoneService(self)  # type: ignore
        )
        self.products: Type['ApiService'] = (
            objects.ProductService(self)  # type: ignore
        )
        self.domains: Type['ApiService'] = (
            objects.DomainService(self)  # type: ignore
        )
        self.invoices: Type['ApiService'] = (
            objects.InvoiceService(self)  # type: ignore
        )
        self.ssh_keys: Type['ApiService'] = (
            objects.SshKeyService(self)  # type: ignore
        )
        self.vpss: Type['ApiService'] = (
            objects.VpsService(self)  # type: ignore
        )

    @property
    def url(self) -> str:
        """Return the API URL."""
        return self._url

    def _get_headers(
        self,
        content_type: Optional[str] = None
    ) -> Dict[str, str]:
        headers = self.headers.copy()
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def _build_url(self, path: str) -> str:
        return f"{self._url}{path}"

    def _request_access_token(self) -> str:
        """
        Request an access token using the supplied private key.

        Returns:
            str: The access token to use for authorization.

        Raises:
            TransIPParsingError: If the requested access token couldn't be
                extracted from the API response.
        """
        url: str = self._build_url('/auth')
        payload: Dict[str, Any] = {
            "login": self._login,
            # The TransIP API requires that the length of the nonce is between
            # 6 and 32 characters
            "nonce": generate_nonce(32),
            # TODO(roaldnefs): Allow the creation of read-only access tokens
            "read_only": False,
            # TODO(roaldnefs): Allow the expiration time of the access token
            # to be overwritten
            # "expiration_time": "30 minutes",
            # TODO(roaldnefs): Allow a custom label to be specified when
            # generating a new access token
            # "label": "python-transip",
            # TODO(roaldnefs): Allow the access token to only be use from
            # whitelisted IP-addresses
            "global_key": False
        }

        headers: Dict[str, str] = self.headers.copy()
        request: requests.Request = requests.Request(
            "POST", url, headers=headers, json=payload
        )
        prepped: requests.PreparedRequest = self.session.prepare_request(
            request
        )

        # Get the prepped body for signature generation
        body: Union[bytes, str] = prepped.body or ''
        if isinstance(body, bytes):
            body = body.decode('ascii')

        # Generate a signature if the request body
        signature: str = generate_message_signature(
            body, self._private_key  # type: ignore
        )

        # Add 'Signature' header to the prepared request
        prepped.headers["Signature"] = signature

        response: requests.Response = self.session.send(prepped)
        data = self._validate_response(response)

        # Attempt to extract the access token from the result
        try:
            return data['token']
        except (AttributeError, KeyError) as exc:
            raise TransIPParsingError(
                "Failed to extract access token from the API response"
            ) from exc

    def _read_private_key(self) -> str:
        """Read the private key from file.

        Returns:
            str: The private key content

        Raises:
            RuntimeError: If the private key file doesn't exist
        """
        if os.path.exists(self._private_key_file):  # type: ignore
            try:
                with open(self._private_key_file) as keyfile:  # type: ignore
                    return keyfile.read()
            except IOError as exc:
                raise RuntimeError("The private key couldn't be read") from exc
        else:
            raise RuntimeError("The private key doesn't exist")

    def _set_auth_info(self) -> None:
        """
        Set authentication information based upon the defined attributes.

        Raises:
            ValueError: If the required attributes are not defined.
        """
        if (not self._access_token and not self._private_key and not
                self._private_key_file):
            raise ValueError(
                "At least one of access_token, private_key and "
                "private_key_file should be defined"
            )
        if self._access_token and self._private_key:
            raise ValueError(
                "Only one of access_token and private_key should be defined"
            )
        if self._access_token and self._private_key_file:
            raise ValueError(
                "Only one of access_token and private_key_file should be "
                "defined"
            )
        if self._private_key and self._private_key_file:
            raise ValueError(
                "Only one of private_key and private_key_file should be "
                "defined"
            )
        if self._private_key and not self._login:
            raise ValueError(
                "Both private_key and login should be defined"
            )
        if self._private_key_file and not self._login:
            raise ValueError(
                "Both private_key_file and login should be defined"
            )

        # Read the private key from file
        if self._private_key_file:
            self._private_key = self._read_private_key()

        # Use the private key to request a new access token
        if self._private_key:
            self._access_token = self._request_access_token()

        # Set the 'Authorization' header
        self.headers["Authorization"] = f"Bearer {self._access_token}"

    def request(
        self,
        method: str,
        path: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Make an HTTP request to the TransIP API.

        Args:
            method (str): HTTP method to use
            path (str): The path to append to the API URL
            data (dict): The body to attach to the request
            json (dict): The json body to attach to the request
            params (dict): URL parameters to append to the URL

        Returns:
            Returns the json-encoded content of a response, if any.

        Raises:
            TransIPHTTPError: When the return code of the request is not 2xx
            TransIPParsingError: When the content couldn't be parsed as JSON
        """
        url: str = self._build_url(path)

        # Set the content type for the request if json is provided and data is
        # not specified
        content_type: Optional[str] = None
        if not data and json:
            content_type = "application/json"

        headers: Dict[str, str] = self._get_headers(content_type)
        request: requests.Request = requests.Request(
            method, url, headers=headers, data=data, json=json, params=params,
        )

        prepped: requests.PreparedRequest = self.session.prepare_request(
            request
        )
        response: requests.Response = self.session.send(prepped)
        return self._validate_response(response)

    def _validate_response(self, response: requests.Response) -> Any:
        """
        Validate the API response.

        Raises:
            TransIPHTTPError: When the return code of the request is not 2xx
            TransIPParsingError: When the content couldn't be parsed as JSON
        """
        if 200 <= response.status_code < 300:
            if response.text:
                try:
                    return response.json()
                except Exception:
                    raise TransIPParsingError(
                        message="Failed to parse the API response as JSON"
                    )
            return None

        error_message = str(response.content)
        try:
            error_json = response.json()
            if "error" in error_json:
                error_message = error_json["error"]
        except (KeyError, ValueError, TypeError):
            pass

        raise TransIPHTTPError(
            message=error_message,
            response_code=response.status_code
        )

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Make a GET request to the TransIP API.

        Args:
            path (str): The path to append to the API URL
            params (dict): URL parameters to append to the URL

        Returns:
            Returns the json-encoded content of a response, if any.

        Raises:
            TransIPHTTPError: When the return code of the request is not 2xx
        """
        return self.request(
            "GET", path, params=params
        )

    def post(
        self,
        path: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Make a POST request to the TransIP API.

        Args:
            path (str): The path to append to the API URL
            data (dict): The body to attach to the request
            json (dict): The json body to attach to the request
            params (dict): URL parameters to append to the URL

        Returns:
            Returns the json-encoded content of a response, if any.

        Raises:
            TransIPHTTPError: When the return code of the request is not 2xx
        """
        return self.request(
            "POST", path, data=data, json=json, params=params
        )

    def put(
        self,
        path: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Make a PUT request to the TransIP API.

        Args:
            path (str): The path to append to the API URL
            data (dict): The body to attach to the request
            json (dict): The json body to attach to the request
            params (dict): URL parameters to append to the URL

        Returns:
            Returns the json-encoded content of a response, if any.

        Raises:
            TransIPHTTPError: When the return code of the request is not 2xx
        """
        return self.request(
            "PUT", path, data=data, json=json, params=params
        )

    def patch(
        self,
        path: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Make a PATCH request to the TransIP API.

        Args:
            path (str): The path to append to the API URL
            data (dict): The body to attach to the request
            json (dict): The json body to attach to the request
            params (dict): URL parameters to append to the URL

        Returns:
            Returns the json-encoded content of a response, if any.

        Raises:
            TransIPHTTPError: When the return code of the request is not 2xx
        """
        return self.request(
            "PATCH", path, data=data, json=json, params=params
        )

    def delete(
        self,
        path: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Make a GET request to the TransIP API.

        Args:
            path (str): The path to append to the API URL
            data (dict): The body to attach to the request
            json (dict): The json body to attach to the request
            params (dict): URL parameters to append to the URL

        Returns:
            Returns the json-encoded content of a response, if any.

        Raises:
            TransIPHTTPError: When the return code of the request is not 2xx
        """
        return self.request(
            "DELETE", path, data=data, json=json, params=params
        )
