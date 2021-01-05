# -*- coding: utf-8 -*-
#
# Copyright (C) 2020, 2021 Roald Nefs <info@roaldnefs.com>
#
# This file is part of python-transip.

# python-transip is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# python-transip is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with python-transip.  If not, see <https://www.gnu.org/licenses/>.
"""Wrapper for the TransIP API."""

import importlib
import requests

from typing import Dict, Optional, Any, Type

from transip.exceptions import TransIPHTTPError, TransIPParsingError


__title__ = "python-transip"
__version__ = "0.2.0"
__author__ = "Roald Nefs"
__email__ = "info@roaldnefs.com"
__copyright__ = "Copyright 2020-2021, Roald Nefs"
__license__ = "LGPL3"


class TransIP:
    """Represents a TransIP server connection.

    Args:
        api_version (str): TransIP API version to use
        access_token (str): The TransIP API access token
    """

    def __init__(
        self,
        api_version: str = "6",
        access_token: Optional[str] = None
    ) -> None:

        self._api_version: str = api_version
        self._url: str = f"https://api.transip.nl/v{api_version}"
        self._access_token: Optional[str] = access_token

        # Headers to use when making a request to TransIP
        self.headers: Dict[str, str] = {
            "User-Agent": f"{__title__}/{__version__}",
            "Authorization": f"Bearer {access_token}"
        }

        # Initialize a session object for making requests
        self.session: requests.Session = requests.Session()

        # Dynamically import the services for the specified API version
        objects = importlib.import_module(f"transip.v{api_version}.objects")

        self.availability_zones: Type[Any] = (
            objects.AvailabilityZoneService(self)  # type: ignore
        )
        self.domains: Type[Any] = objects.DomainService(self)  # type: ignore
        self.invoices: Type[Any] = (
            objects.InvoiceService(self)  # type: ignore
        )
        self.ssh_keys: Type[Any] = objects.SshKeyService(self)  # type: ignore
        self.vpss: Type[Any] = objects.VpsService(self)  # type: ignore

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

    def _send(
        self,
        method: str,
        path: str,
        data: Optional[Any] = None,
        json: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """Make an HTTP request to the TransIP API.

        Args:
            method (str): HTTP method to use
            path (str): The path to append to the API URL
            data (dict): The body to attach to the request
            json (dict): The json body to attach to the request
            params (dict): URL parameters to append to the URL

        Returns:
            A requests response object.

        Raises:
            TransIPHTTPError: When the return code of the request is not 2xx
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

        if 200 <= response.status_code < 300:
            return response

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
        """
        response: requests.Response = self._send(
            method, path, data=data, json=json, params=params
        )

        if response.text:
            try:
                return response.json()
            except Exception:
                raise TransIPParsingError(
                    message="Failed to parse the API response as JSON"
                )
        return None

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
            "DELETE", path, params=params
        )
