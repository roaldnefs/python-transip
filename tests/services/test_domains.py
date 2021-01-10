# -*- coding: utf-8 -*-
#
# Copyright (C) 2020, 2012 Roald Nefs <info@roaldnefs.com>
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
        domain: Domain = self.client.domains.get("example.com")

        assert domain.get_id() == "example.com"  # type: ignore

    @responses.activate
    def test_contacts_list(self) -> None:
        domain: Domain = self.client.domains.get("example.com")
        contacts: List[Domain] = domain.contacts.list()  # type: ignore
        contact: Domain = contacts[0]

        assert len(contacts) == 1
        assert contact.companyName == "Example B.V."  # type: ignore

    @responses.activate
    def test_nameservers_list(self) -> None:
        domain: Domain = self.client.domains.get("example.com")
        nameservers: List[Nameserver] = domain.nameservers.list()  # type: ignore
        nameserver: Nameserver = nameservers[0]

        assert len(nameservers) == 1
        assert nameserver.get_id() == "ns0.transip.nl"  # type: ignore

    @responses.activate
    def test_dns_list(self) -> None:
        domain: Domain = self.client.domains.get("example.com")
        entries: List[DnsEntry] = domain.dns.list()  # type: ignore
        entry: DnsEntry = entries[0]

        assert len(entries) == 1
        assert entry.name == "www"  # type: ignore

    @responses.activate
    def test_dns_create(self) -> None:
        dns_entry_data: Dict[str, Union[str, int]] = {
            "name": "www",
            "expire": 86400,
            "type": "A",
            "content": "127.0.0.1"
        }
        domain: Domain = self.client.domains.get("example.com")
        domain.dns.create(dns_entry_data)  # type: ignore

        assert len(responses.calls) == 2
