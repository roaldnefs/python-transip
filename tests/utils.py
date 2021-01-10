# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Roald Nefs <info@roaldnefs.com>
#
# This file is part of python-transip.
#
# python-transip is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# python-transip is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-transip.  If not, see <https://www.gnu.org/licenses/>.

from typing import Any, List, Dict
import json
import os
import responses  # type: ignore


def load_responses_fixtures(path) -> None:
    """Load a JSON fixture containing all the API response examples."""

    def _load_json_fixtures(path: str) -> List[Dict[str, Any]]:
        """Load JSON fixtures from file."""
        cwd: str = os.path.dirname(os.path.realpath(__file__))
        fixtures: str = os.path.join(os.path.join(cwd, 'fixtures'), path)
        with open(fixtures) as fixture:
            return json.load(fixture)

    def _get_responses_method(method: str) -> str:
        """Returns the responses method based upon the supplied method.

        Args:
            method (str): The response method.

        Raises:
            ValueError: if the specified method is invalid.
        """
        method = method.upper()
        if method == "GET":
            return responses.GET
        elif method == "POST":
            return responses.POST
        elif method == "DELETE":
            return responses.DELETE
        elif method == "PUT":
            return responses.PUT
        elif method == "PATCH":
            return responses.PATCH
        raise ValueError(f"Unable to find method '{method}' in responses")
    
    fixtures: List[Dict[str, Any]] = _load_json_fixtures(path)
    for fixture in fixtures:
        # Add the matchers for the request parameters or JSON body
        matchers: List[Any] = []
        if fixture.get('match_json_params'):
            matchers.append(
                responses.json_params_matcher(fixture['match_json_params'])
            )
        if fixture.get('match_urlencoded_params'):
            matchers.append(
                responses.urlencoded_params_matcher(
                    fixture['match_urlencoded_params']
                )
            )

        # Register the mocked response
        responses.add(
            _get_responses_method(fixture["method"]),
            url=fixture["url"],
            json=fixture.get("json"),
            status=fixture["status"],
            content_type=fixture.get("content_type", "application/json"),
            match=matchers
        )
