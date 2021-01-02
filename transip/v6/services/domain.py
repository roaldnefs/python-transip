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
from transip.mixins import (
    CreateMixin, GetMixin, DeleteMixin, ListMixin, CreateAttrsTuple
)


class WhoisContact(ApiObject):

    _id_attr: Optional[str] = None


class WhoisContactService(ListMixin, ApiService):
    """Service to manage domain contacts of a domain."""

    _path: str = "/domains/{parent_id}/contacts"
    _obj_cls: Optional[Type[ApiObject]] = WhoisContact

    _resp_list_attr: str = "contacts"


class DnsEntry(ApiObject):

    _id_attr: Optional[str] = None


class DnsEntryService(CreateMixin, ListMixin, ApiService):
    """Service to manage DNS entries of a domain."""

    _path: str = "/domains/{parent_id}/dns"
    _obj_cls: Optional[Type[ApiObject]] = DnsEntry

    _resp_list_attr: str = "dnsEntries"
    _req_create_attr: str = "dnsEntry"
    _create_attrs: Optional[CreateAttrsTuple] = (
        ("name", "expire", "type", "content"),  # required
        tuple()  # optional
    )


class Nameserver(ApiObject):

    _id_attr: Optional[str] = "hostname"


class NameserverService(ListMixin, ApiService):
    """Service to nameservers of a domain."""

    _path: str = "/domains/{parent_id}/nameservers"
    _obj_cls: Optional[Type[ApiObject]] = Nameserver

    _resp_list_attr: str = "nameservers"


class Domain(ApiObject):

    _id_attr: str = "name"

    @property
    def contacts(self) -> WhoisContactService:
        """Return the service to manage the WHOIS contacts of the domain."""
        return WhoisContactService(
            self.service.client,
            parent=self  # type: ignore
        )

    @property
    def dns(self) -> DnsEntryService:
        """Return the service to manage the DNS entries of the domain."""
        return DnsEntryService(
            self.service.client,
            parent=self  # type: ignore
        )

    @property
    def nameservers(self) -> NameserverService:
        """Return the service to manage the nameservers of the domain."""
        return NameserverService(
            self.service.client,
            parent=self  # type: ignore
        )


class DomainService(CreateMixin, GetMixin, DeleteMixin, ListMixin, ApiService):
    """Service to manage domains."""

    _path: str = "/domains"
    _obj_cls: Optional[Type[ApiObject]] = Domain

    _resp_list_attr: str = "domains"
    _resp_get_attr: str = "domain"

    _create_attrs: Optional[CreateAttrsTuple] = (
        ("domainName",),  # required
        ("contacts", "nameservers", "dnsEntries")  # optional
    )
