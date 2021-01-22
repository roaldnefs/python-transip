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
from transip.v6.objects import Product, ProductElement
from tests.utils import load_responses_fixtures


class ProductsTest(unittest.TestCase):
    """Test the ProductsService."""

    client: TransIP

    @classmethod
    def setUpClass(cls) -> None:
        """Set up a minimal TransIP client for using the invoice services."""
        cls.client = TransIP(access_token='ACCESS_TOKEN')

    def setUp(self) -> None:
        """Setup mocked responses for the '/products' endpoint."""
        load_responses_fixtures("general.json")

    @responses.activate
    def test_list(self) -> None:
        """Check if the products can be listed."""
        products: List[Product] = self.client.products.list()  # type: ignore
    
        self.assertEqual(len(products), 5)

    @responses.activate
    def test_elements_list(self) -> None:
        """Check if the elements of a product can be listed."""
        products: List[Product] = self.client.products.list()  # type: ignore
        product: Optional[Product] = None

        # Find the correct product as the API doesn't provide an option to
        # retrieve a single product
        for entry in products:
            if entry.get_id() == 'vps-bladevps-x4':
                product = entry
                break
        
        self.assertIsNotNone(product)

        elements = product.elements.list()  # type: ignore
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0].get_id(), 'ipv4Addresses')  # type: ignore
