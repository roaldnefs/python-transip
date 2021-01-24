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

import responses  # type: ignore
import unittest

from typing import List, Dict, Any, Union

from transip import TransIP
from transip.v6.objects import Domain, WhoisContact, Nameserver, DnsEntry
from tests.utils import load_responses_fixtures


class DomainsTest(unittest.TestCase):
    """Test the DomainService."""

    client: TransIP

    @classmethod
    def setUpClass(cls) -> None:
        """Set up a minimal TransIP client for using the domain services."""
        cls.client = TransIP(access_token='ACCESS_TOKEN')

    def setUp(self) -> None:
        """Setup mocked responses for the '/domains' endpoint."""
        load_responses_fixtures("domains.json")

    @responses.activate
    def test_get(self) -> None:
        domain: Domain = self.client.domains.get("example.com")  # type: ignore

        assert domain.get_id() == "example.com"  # type: ignore

    @responses.activate
    def test_contacts_list(self) -> None:
        domain: Domain = self.client.domains.get("example.com")  # type: ignore
        contacts: List[Domain] = domain.contacts.list()  # type: ignore
        contact: Domain = contacts[0]

        assert len(contacts) == 1
        assert contact.companyName == "Example B.V."  # type: ignore

    @responses.activate
    def test_nameservers_list(self) -> None:
        domain: Domain = self.client.domains.get("example.com")  # type: ignore
        nameservers: List[Nameserver] = domain.nameservers.list()  # type: ignore
        nameserver: Nameserver = nameservers[0]

        assert len(nameservers) == 1
        assert nameserver.get_id() == "ns0.transip.nl"  # type: ignore

    @responses.activate
    def test_dns_list(self) -> None:
        """
        Check if the DNS records for a single domain can be listed.
        """
        domain: Domain = self.client.domains.get("example.com")  # type: ignore
        entries: List[DnsEntry] = domain.dns.list()  # type: ignore

        self.assertEqual(len(entries), 1)
        entry: DnsEntry = entries[0]
        self.assertEqual(entry.content, "127.0.0.1")  # type: ignore

    @responses.activate
    def test_dns_replace(self) -> None:
        """
        Check if the existing DNS records for a single domain can be replaced
        at once.
        """
        domain: Domain = self.client.domains.get("example.com")  # type: ignore
        records: List[DnsEntry] = domain.dns.list()  # type: ignore

        # Ensure we have a single DNS record
        self.assertEqual(len(records), 1)
        # Update the content of the first DNS record in the list of existing
        # records.
        records[0].content = '127.0.0.2'

        # Replace all existing records.
        try:
            domain.dns.replace(records)  # type: ignore
        except Exception as exc:
            assert False, f"'transip.v6.objects.Domain.dns.replace' raised an exception {exc}"


    @responses.activate
    def test_dns_create(self) -> None:
        dns_entry_data: Dict[str, Union[str, int]] = {
            "name": "www",
            "expire": 86400,
            "type": "A",
            "content": "127.0.0.1"
        }
        domain: Domain = self.client.domains.get("example.com")  # type: ignore
        domain.dns.create(dns_entry_data)  # type: ignore

        assert len(responses.calls) == 2

    @responses.activate
    def test_dns_update(self) -> None:
        """
        Check if a single DNS entry can be updated.
        """
        dns_entry_data: Dict[str, Union[str, int]] = {
            "name": "www",
            "expire": 86400,
            "type": "A",
            "content": "127.0.0.2"  # original content is 127.0.0.1
        }
        domain: Domain = self.client.domains.get("example.com")  # type: ignore

        try:
            domain.dns.update(dns_entry_data)
        except Exception as exc:
            assert False, f"'transip.v6.objects.Domain.dns.update' raised an exception {exc}"

    @responses.activate
    def test_dns_update_object(self) -> None:
        """
        Check if a single DNS entry can be updated from the ApiObject itself.
        """
        domain: Domain = self.client.domains.get("example.com")  # type: ignore
        entries: List[DnsEntry] = domain.dns.list()  # type: ignore

        self.assertEqual(len(entries), 1)
        entry: DnsEntry = entries[0]
        self.assertEqual(entry.content, "127.0.0.1")  # type: ignore

        entry.content = '127.0.0.2'
        try:
            entry.update()
        except Exception as exc:
            assert False, f"'transip.v6.objects.DnsEntry.update' raised an exception {exc}"

        self.assertEqual(entry.content, "127.0.0.2")  # type: ignore

    @responses.activate
    def test_dns_delete(self) -> None:
        """Check if a single DNS entry can be deleted."""
        dns_entry_data: Dict[str, Union[str, int]] = {
            "name": "www",
            "expire": 86400,
            "type": "A",
            "content": "127.0.0.1"
        }
        domain: Domain = self.client.domains.get("example.com")  # type: ignore

        try:
            domain.dns.delete(dns_entry_data)  # type: ignore
        except Exception as exc:
            assert False, (
                "'transip.v6.objects.Domain.dns.delete' raised an exception "
                f"{exc}"
            )
        # Ensure only two calls are being made: the retrieval of the domain and
        # the deletion of the DNS entry
        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    def test_dns_delete_object(self) -> None:
        """Check if a DNS entry can be deleted from the object itself."""
        domain: Domain = self.client.domains.get("example.com")  # type: ignore
        entries = domain.dns.list()

        self.assertEqual(len(entries), 1)

        entry: DnsEntry = entries[0]  # type: ignore
        try:
            # Delete the first DNS entry
            entry.delete()
        except Exception as exc:
            assert False, (
                "'transip.v6.objects.DnsEntry.delete' raised an exception "
                f"{exc}"
            )
        # Ensure only three calls are being made; the retrieval of the domain,
        # the listing of the DNS entries and the deletion of a single DNS
        # entry.
        self.assertEqual(len(responses.calls), 3)
