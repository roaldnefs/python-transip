# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Roald Nefs <info@roaldnefs.com>
#
# This file is part of python-transip.

# python-transip is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
"""Wrapper for the TransIP API."""

import importlib
import requests

from typing import Dict, Optional, Any

from transip.exceptions import TransIPHTTPError

__title__ = "python-transip"
__version__ = "0.0.1"
__author__ = "Roald Nefs"
__email__ = "info@roaldnefs.com"
__copyright__ = "Copyright 2020, Roald Nefs"
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
        access_token: str = None
    ) -> None:

        self._api_version: str = api_version
        self._url: str = "https://api.transip.nl/v{version}".format(
            version=api_version
        )
        self._access_token: str = access_token

        # Headers to use when making a request to TransIP
        self.headers: Dict[str, str] = {
            "User-Agent": "{title}/{version}".format(
                title=__title__,
                version=__version__
            ),
            "Authorization": "Bearer {token}".format(
                token=access_token
            )
        }

        # Initialize a session object for making requests
        self.session: requests.Session = requests.Session()

        # Dynamically import the objects for the specified API version
        objects = importlib.import_module("transip.v{version}.objects".format(
                version=api_version
            )
        )

    @property
    def url(self) -> str:
        """Return the API URL."""
        return self._url

    def _get_headers(self, content_type: Optional[str] = None) -> Dict[str, str]:
        headers = self.headers.copy()
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def _build_url(self, path: str) -> str:
        return "{api_url}{path}".format(
            api_url=self._url,
            path=path
        )

    def request(
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
            path (str):
            data (dict): the body to attach to the request
            json (dict): the json body to attach to the request
            params (dict): URL parameters to append to the URL

        Returns:
            A requests result object.

        Raises:
            TransIPHTTPError: When the return code of the request is not 2xx
        """
        url: str = self._build_url(path)

        # Set the content type for the request if json is provided and data is
        # not specified
        content_type: str = None
        if not data and json:
            content_type = "application/json"

        headers: Dict[str, str] = self._get_headers(content_type) 
        request: request.Request = requests.Request(
            method, url, headers=headers, data=data, json=json, params=params, 
        )

        prepped: requests.PreparedRequest = self.session.prepare_request(request)
        response: request.Response = self.session.send(prepped)

        if 200 <= response.status_code < 300:
            return response

        error_message = response.content
        try:
            error_json = result.json()
            if "error" in error_json:
                error_message = error_json["error"]
        except (KeyError, ValueError, TypeError):
            pass

        raise TransIPHTTPError(
            message=error_message,
            response_code=response.status_code
        )

    def get(self, path: str) -> requests.Response:
        return self.request(
            "GET", path
        )

    def post(self):
        pass

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass