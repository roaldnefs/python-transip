# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Roald Nefs <info@roaldnefs.com>
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

from typing import Type, List
import responses  # type: ignore

from transip import TransIP
from transip.v6.services.invoice import Invoice


@responses.activate
def test_invoices_list(transip_minimal_client: Type[TransIP]) -> None:
    responses.add(
        responses.GET,
        "https://api.transip.nl/v6/invoices",
        json={
            "invoices": [
                {
                    "invoiceNumber": "F0000.1911.0000.0004",
                    "creationDate": "2020-01-01",
                    "payDate": "2020-01-01",
                    "dueDate": "2020-02-01",
                    "invoiceStatus": "waitsforpayment",
                    "currency": "EUR",
                    "totalAmount": 1000,
                    "totalAmountInclVat": 1240
                }
            ]
        },
        status=200,
    )
    
    invoices: List[Type[Invoice]] = transip_minimal_client.invoices.list()
    invoice: Type[Invoice] = invoices[0] 
    assert len(invoices) == 1
    assert invoice.get_id() == "F0000.1911.0000.0004"  # type: ignore


@responses.activate
def test_invoices_get(transip_minimal_client: Type[TransIP]) -> None:
    responses.add(
        responses.GET,
        "https://api.transip.nl/v6/invoices/F0000.1911.0000.0004",
        json={
            "invoice": {
                "invoiceNumber": "F0000.1911.0000.0004",
                "creationDate": "2020-01-01",
                "payDate": "2020-01-01",
                "dueDate": "2020-02-01",
                "invoiceStatus": "waitsforpayment",
                "currency": "EUR",
                "totalAmount": 1000,
                "totalAmountInclVat": 1240
            }
        },
        status=200,
    )
    
    invoice_id: str = "F0000.1911.0000.0004"
    invoice: Type[Invoice] = transip_minimal_client.invoices.get(invoice_id)
    assert invoice.get_id() == "F0000.1911.0000.0004"  # type: ignore
