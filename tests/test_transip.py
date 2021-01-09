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

import unittest

from transip import TransIP


class TransIPTest(unittest.TestCase):
    """Test the TransIP client class."""

    client: TransIP

    @classmethod
    def setUpClass(self) -> None:
        """Set up a minimal TransIP client."""
        self.client = TransIP(access_token='ACCESS_TOKEN')

    def test_base_url(self) -> None:
        """Test the base URL of the API."""
        url: str = self.client.url

        assert url == "https://api.transip.nl/v6"

    def test_authorization_header(self) -> None:
        """Test if the Authorization header is set correctly."""
        auth_header: str = self.client.headers["Authorization"]

        assert auth_header == "Bearer ACCESS_TOKEN"
