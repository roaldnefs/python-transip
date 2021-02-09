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
#
# python-transip is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-transip.  If not, see <https://www.gnu.org/licenses/>.

from typing import List, Tuple, Any, Dict, Optional
import responses  # type: ignore
import unittest
import tempfile
import os

from transip import TransIP
from transip.v6.objects import Colocation
from tests.utils import load_responses_fixtures


class ColocationsTest(unittest.TestCase):
    """Test the ColocationService."""

    client: TransIP

    @classmethod
    def setUpClass(cls) -> None:
        """Set up a minimal TransIP client for using the colocation services."""
        cls.client = TransIP(access_token='ACCESS_TOKEN')

    def setUp(self) -> None:
        """Setup mocked responses for the '/colocations' endpoint."""
        load_responses_fixtures("colocations.json")

    @responses.activate
    def test_list(self) -> None:
        colocations: List[Colocation] = self.client.colocations.list()  # type: ignore
        self.assertEqual(len(colocations), 1)
        self.assertEqual(colocations[0].get_id(), "example2")  # type: ignore

    @responses.activate
    def test_get(self) -> None:
        colocation_name: str = "example2"
        colocation: Colocation = self.client.colocations.get(colocation_name)  # type: ignore
        self.assertEqual(colocation.get_id(), colocation_name)  # type: ignore
