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

from typing import List, Tuple, Any, Dict, Optional
import responses  # type: ignore
import unittest
import tempfile
import os

from transip import TransIP
from transip.v6.objects import Invoice, InvoiceItem
from tests.utils import load_responses_fixtures

class InvoicesTest(unittest.TestCase):
    """Test the InvoiceService."""

    client: TransIP
    tmp_dir: Optional[tempfile.TemporaryDirectory]

    @classmethod
    def setUpClass(cls) -> None:
        """Set up a minimal TransIP client for using the invoice services."""
        cls.client = TransIP(access_token='ACCESS_TOKEN')

    def setUp(self) -> None:
        """Setup mocked responses for the '/invoices' endpoint."""
        load_responses_fixtures("account.json")

    @responses.activate
    def test_list(self) -> None:
        invoices: List[Invoice] = self.client.invoices.list()  # type: ignore
        invoice: Invoice = invoices[0]
    
        self.assertEqual(len(invoices), 1)
        self.assertEqual(invoice.get_id(), "F0000.1911.0000.0004")  # type: ignore

    @responses.activate
    def test_get(self) -> None:
        invoice_id: str = "F0000.1911.0000.0004"
        invoice: Invoice = self.client.invoices.get(invoice_id)  # type: ignore

        self.assertEqual(invoice.get_id(), "F0000.1911.0000.0004")  # type: ignore

    @responses.activate
    def test_items_list(self) -> None:
        invoice: Invoice = self.client.invoices.get("F0000.1911.0000.0004")  # type: ignore
        items: List[InvoiceItem] = invoice.items.list()  # type: ignore

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].product, "Big Storage Disk 2000 GB")  # type: ignore

        # Expect the get_id() method to return None as the invoice items don't
        # have a specific ID attribute.
        self.assertIsNone(items[0].get_id())  # type: ignore

    @responses.activate
    def test_pdf(self) -> None:
        """
        Check if the invoice can be written to a PDF file.
        """
        invoice_id = "F0000.1911.0000.0004"
        invoice: Invoice = self.client.invoices.get(invoice_id)  # type: ignore

        # Write the invoice to a PDF file in a temporary directory.
        with tempfile.TemporaryDirectory() as tmp_dir:
            expected = os.path.join(tmp_dir, f"{invoice_id}.pdf")
            actual = invoice.pdf(tmp_dir)
            self.assertEqual(actual, expected)
