# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Roald Nefs <info@roaldnefs.com>
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

from typing import Any
import json
import os
import responses  # type: ignore


def load_fixture(path) -> Any:
    """Load a JSON fixture from the fixtures directory."""
    fixtures: str = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures"
    )
    with open(os.path.join(fixtures, path)) as fixture:
        return json.load(fixture)


def load_responses_fixture(path) -> None:
    """Load a JSON fixture containing all the API response examples."""

    def get_responses_method(method: str) -> str:
        """
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
    
    fixture = load_fixture(path)
    for response in fixture:
        match = []
        if response.get("match_json"):
            match.append(responses.json_params_matcher(response["match_json"]))

        responses.add(
            get_responses_method(response["method"]),
            url=response["url"],
            json=response.get("json"),
            status=response["status"],
            content_type=response.get("content_type", "application/json"),
            match=match
        )