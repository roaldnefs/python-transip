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

from typing import Optional, Type

from transip.base import ApiService, ApiObject
from transip.mixins import GetMixin, ListMixin
from transip.v6.objects.invoice import Invoice


class Invoice(ApiObject):

    _id_attr: str = "invoiceNumber"


class InvoiceService(GetMixin, ListMixin, ApiService):

    _path: str = "/invoices"
    _obj_cls: Optional[Type[ApiObject]] = Invoice

    _resp_list_attr: str = "invoices"
    _resp_get_attr: str = "invoice"
