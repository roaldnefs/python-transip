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

import os
import base64

from typing import Optional, Type, List, Dict, Any

from transip.base import ApiService, ApiObject
from transip.mixins import (
    GetMixin, DeleteMixin, ListMixin, CreateMixin, UpdateMixin,
    ObjectDeleteMixin, ObjectUpdateMixin,
    CreateAttrsTuple, UpdateAttrsTuple
)
from transip.exceptions import TransIPIOError

# Typing alias for the _delete_attrs attributes in the DeleteMixin
DeleteAttrsTuple = CreateAttrsTuple


class ApiTestService(ApiService):

    _path: str = "/api-test"

    def test(self):
        """
        A simple test to make sure everything is working.

        Returns:
            bool: True if everything is working, False otherwise.
        """
        response = self.client.get(f"{self.path}")
        if response.get('ping') == 'pong':
            return True
        return False


class ProductElement(ApiObject):

    _id_attr: str = "name"


class ProductElementService(ListMixin, ApiService):
    """Service to manage elements of a product."""

    _path: str = "/products/{parent_id}/elements"
    _obj_cls: Optional[Type[ApiObject]] = ProductElement

    _resp_list_attr: str = "productElements"


class Product(ApiObject):

    _id_attr: Optional[str] = "name"

    @property
    def elements(self) -> ProductElementService:
        """Return the service to manage the elements of the product."""
        return ProductElementService(
            self.service.client,
            parent=self  # type: ignore
        )


class ProductService(ListMixin, ApiService):
    """Service to manage products."""

    _path: str = "/products"
    _obj_cls: Optional[Type[ApiObject]] = Product

    _resp_list_attr: str = "products"

    def list(self) -> List[Type[ApiObject]]:
        """
        Retrieve a list of products.

        Overwrites the default list() method of the ListMixin as the products
        are stored in further down in the result dictionary.
        """
        objs: List[Type[ApiObject]] = []
        data = self.client.get(self.path)[self._resp_list_attr]
        # Loop over the individual product lists of all product categories,
        # e.g. vps, haip
        for obj_list in data.values():
            for obj in obj_list:
                objs.append(self._obj_cls(self, obj))  # type: ignore
        return objs


class AvailabilityZone(ApiObject):

    _id_attr: str = "name"


class AvailabilityZoneService(ListMixin, ApiService):

    _path: str = "/availability-zones"
    _obj_cls: Optional[Type[ApiObject]] = AvailabilityZone

    _resp_list_attr: str = "availabilityZones"


class SshKey(ObjectDeleteMixin, ObjectUpdateMixin, ApiObject):

    _id_attr: str = "id"


class SshKeyService(GetMixin, CreateMixin, UpdateMixin, DeleteMixin, ListMixin,
                    ApiService):

    _path: str = "/ssh-keys"
    _obj_cls: Optional[Type[ApiObject]] = SshKey

    _resp_list_attr: str = "sshKeys"
    _resp_get_attr: str = "sshKey"

    _create_attrs: Optional[CreateAttrsTuple] = (
        ("sshKey",),  # required
        ("description",)  # optional
    )
    _update_attrs: Optional[UpdateAttrsTuple] = (
        ("description",),  # required
        tuple()  # optional
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

    def delete(self) -> None:
        """
        Delete a single DNS entry by calling the delete() method on its service
        and providing all the DNS entry attributes.

        This is different from the delete() method from the ObjectDeleteMixin
        as the deletion of a DNS entry requires all attributes of a single DNS
        entry and the DNS entries do not have an ID.
        """
        self.service.delete(self.attrs)


class DnsEntryService(CreateMixin, ListMixin, ApiService):
    """Service to manage DNS entries of a domain."""

    _path: str = "/domains/{parent_id}/dns"
    _obj_cls: Optional[Type[ApiObject]] = DnsEntry

    _resp_list_attr: str = "dnsEntries"
    _req_create_attr: str = "dnsEntry"
    _create_attrs: CreateAttrsTuple = (
        ("name", "expire", "type", "content"),  # required
        tuple()  # optional
    )

    # Additional data required to delete a single DNS entry, the DeleteMixin
    # can't be used as DNS entries don't have an ID.
    _req_delete_attr: str = "dnsEntry"
    _delete_attrs: DeleteAttrsTuple = (
        ("name", "expire", "type", "content"),  # required
        tuple()  # optional
    )

    def get_delete_attrs(self) -> DeleteAttrsTuple:
        """
        Return the required and optional attributes for deleting a DNS entry.

        Returns:
            tuple: a tuple containing a tuple of required and optional
                attributes.
        """
        return self._delete_attrs

    def _check_delete_attrs(self, attrs) -> None:
        """
        Check required attributes.

        Raises:
            AttributeError: If any of the required attributes is missing.
        """
        required, optional = self.get_delete_attrs()
        missing = [attr for attr in required if attr not in attrs]

        if missing:
            attrs_str = "', '".join(missing)
            raise AttributeError((
                f"'{self.__class__.__name__}' object has no "
                f"attribute{'s'[:len(missing)!=1]} '{attrs_str}'"
            ))

    def delete(self, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Delete a DNS entry.

        This is different from the delete() method from the DeleteMixin as the
        deletion of a DNS entry requires all attributes of a single DNS entry
        and the DNS entries do not have an ID.
        """
        if data is None:
            data = {}

        # Check if all required attributes are supplied
        self._check_delete_attrs(data)

        # Requires the endpoint to be packed in dictionary with a specific key
        data = {self._req_delete_attr: data}

        if self.path:
            self.client.delete(f"{self.path}", json=data)


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


class InvoiceItem(ApiObject):
    pass


class InvoiceItemService(ListMixin, ApiService):
    """Service to items of an invoice."""

    _path: str = "/invoices/{parent_id}/invoice-items"
    _obj_cls: Optional[Type[ApiObject]] = InvoiceItem

    _resp_list_attr: str = "invoiceItems"


class Invoice(ApiObject):

    _id_attr: str = "invoiceNumber"

    @property
    def items(self) -> InvoiceItemService:
        """Return the service to manage the items of an invoice"""
        return InvoiceItemService(
            self.service.client,
            parent=self  # type: ignore
        )

    def pdf(self, file_path: str) -> Optional[str]:
        """
        Write a invoice to a PDF file.

        Args:
            file_path (str): Path to PDF file, if the path is a directory to
                PDF is saved using its invoice number.

        Returns:
            str: The absolute path to the saved PDF file.

        Raises:
            TransIPIOError: If the PDF data couldn't be written to file.
        """
        invoice_id = self.get_id()
        if not invoice_id:
            return None

        # Retrieve the base64 encoded PDF data
        encoded = self.service.client.get(f"/invoices/{invoice_id}/pdf")["pdf"]
        data = base64.b64decode(encoded.encode('ascii'))

        file_path = os.path.abspath(file_path)
        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, f"{invoice_id}.pdf")
        if os.path.exists(file_path):
            raise TransIPIOError(f"File {file_path} already exists")

        try:
            with open(file_path, 'wb') as pdf_file:
                pdf_file.write(data)
        except OSError as exc:
            raise TransIPIOError(
                f"Unable to write PDF file {file_path}"
            ) from exc

        return file_path


class InvoiceService(GetMixin, ListMixin, ApiService):

    _path: str = "/invoices"
    _obj_cls: Optional[Type[ApiObject]] = Invoice

    _resp_list_attr: str = "invoices"
    _resp_get_attr: str = "invoice"


class Vps(ApiObject):

    _id_attr: str = "name"


class VpsService(GetMixin, DeleteMixin, ListMixin, ApiService):

    _path: str = "/vps"
    _obj_cls: Optional[Type[ApiObject]] = Vps

    _resp_list_attr: str = "vpss"
    _resp_get_attr: str = "vps"
