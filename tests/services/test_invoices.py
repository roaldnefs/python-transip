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

from typing import List, Tuple, Any, Dict
import responses  # type: ignore
import unittest

from transip import TransIP
from transip.v6.objects import Invoice
from tests.utils import load_responses_fixtures

class InvoicesTest(unittest.TestCase):
    """Test the InvoiceService."""

    client: TransIP

    @classmethod
    def setUpClass(cls) -> None:
        """Set up a minimal TransIP client for using the invoice services."""
        cls.client = TransIP(access_token='ACCESS_TOKEN')

    def setUp(self) -> None:
        """Setup mocked responses for the '/invoices' endpoint."""
        load_responses_fixtures("account.json")

    @responses.activate
    def test_list(self) -> None:
        invoices: List[Invoice] = self.client.invoices.list()
        invoice: Invoice = invoices[0]
    
        assert len(invoices) == 1
        assert invoice.get_id() == "F0000.1911.0000.0004"  # type: ignore

    @responses.activate
    def test_get(self) -> None:
        invoice_id: str = "F0000.1911.0000.0004"
        invoice: Invoice = self.client.invoices.get(invoice_id)

        assert invoice.get_id() == "F0000.1911.0000.0004"  # type: ignore
