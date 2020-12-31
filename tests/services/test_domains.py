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
from transip.v6.services.domain import (
    Domain, WhoisContact, Nameserver, DnsEntry
)


@responses.activate
def test_domains_get(transip_minimal_client: Type[TransIP]) -> None:
    responses.add(
        responses.GET,
        "https://api.transip.nl/v6/domains/example.com",
        json={
            "domain": {
                "name": "example.com",
                "authCode": "kJqfuOXNOYQKqh/jO4bYSn54YDqgAt1ksCe+ZG4Ud4nfpzw8qBsfR2JqAj7Ce12SxKcGD09v+yXd6lrm",
                "isTransferLocked": False,
                "registrationDate": "2016-01-01",
                "renewalDate": "2020-01-01",
                "isWhitelabel": False,
                "cancellationDate": "2020-01-01 12:00:00",
                "cancellationStatus": "signed",
                "isDnsOnly": False,
                "tags": [
                    "customTag",
                    "anotherTag"
                ]
            }
        },
        status=200,
    )

    domain: Type[Domain] = transip_minimal_client.domains.get("example.com")
    assert domain.get_id() == "example.com"  # type: ignore

@responses.activate
def test_domains_contacts_list(transip_minimal_client: Type[TransIP]) -> None:
    responses.add(
        responses.GET,
        "https://api.transip.nl/v6/domains/example.com",
        json={
            "domain": {
                "name": "example.com",
                "authCode": "kJqfuOXNOYQKqh/jO4bYSn54YDqgAt1ksCe+ZG4Ud4nfpzw8qBsfR2JqAj7Ce12SxKcGD09v+yXd6lrm",
                "isTransferLocked": False,
                "registrationDate": "2016-01-01",
                "renewalDate": "2020-01-01",
                "isWhitelabel": False,
                "cancellationDate": "2020-01-01 12:00:00",
                "cancellationStatus": "signed",
                "isDnsOnly": False,
                "tags": [
                    "customTag",
                    "anotherTag"
                ]
            }
        },
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api.transip.nl/v6/domains/example.com/contacts",
        json={
            "contacts": [
                {
                "type": "registrant",
                "firstName": "John",
                "lastName": "Doe",
                "companyName": "Example B.V.",
                "companyKvk": "83057825",
                "companyType": "BV",
                "street": "Easy street",
                "number": "12",
                "postalCode": "1337 XD",
                "city": "Leiden",
                "phoneNumber": "+31 715241919",
                "faxNumber": "+31 715241919",
                "email": "example@example.com",
                "country": "nl"
                }
            ]
        },
        status=200,
    )

    domain: Type[Domain] = transip_minimal_client.domains.get("example.com")
    contacts: List[Type[Domain]] = domain.contacts.list()  # type: ignore
    contact: Type[Domain] = contacts[0]
    assert len(contacts) == 1
    assert contact.companyName == "Example B.V."  # type: ignore


@responses.activate
def test_domains_nameservers_list(transip_minimal_client: Type[TransIP]) -> None:
    responses.add(
        responses.GET,
        "https://api.transip.nl/v6/domains/example.com",
        json={
            "domain": {
                "name": "example.com",
                "authCode": "kJqfuOXNOYQKqh/jO4bYSn54YDqgAt1ksCe+ZG4Ud4nfpzw8qBsfR2JqAj7Ce12SxKcGD09v+yXd6lrm",
                "isTransferLocked": False,
                "registrationDate": "2016-01-01",
                "renewalDate": "2020-01-01",
                "isWhitelabel": False,
                "cancellationDate": "2020-01-01 12:00:00",
                "cancellationStatus": "signed",
                "isDnsOnly": False,
                "tags": [
                    "customTag",
                    "anotherTag"
                ]
            }
        },
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api.transip.nl/v6/domains/example.com/nameservers",
        json={
            "nameservers": [
                {
                    "hostname": "ns0.transip.nl",
                    "ipv4": "",
                    "ipv6": ""
                }
            ]
        },
        status=200,
    )

    domain: Type[Domain] = transip_minimal_client.domains.get("example.com")
    nameservers: List[Type[Nameserver]] = domain.nameservers.list()  # type: ignore
    nameserver: Type[Nameserver] = nameservers[0]
    assert len(nameservers) == 1
    assert nameserver.get_id() == "ns0.transip.nl"  # type: ignore


@responses.activate
def test_domains_dns_list(transip_minimal_client: Type[TransIP]) -> None:
    responses.add(
        responses.GET,
        "https://api.transip.nl/v6/domains/example.com",
        json={
            "domain": {
                "name": "example.com",
                "authCode": "kJqfuOXNOYQKqh/jO4bYSn54YDqgAt1ksCe+ZG4Ud4nfpzw8qBsfR2JqAj7Ce12SxKcGD09v+yXd6lrm",
                "isTransferLocked": False,
                "registrationDate": "2016-01-01",
                "renewalDate": "2020-01-01",
                "isWhitelabel": False,
                "cancellationDate": "2020-01-01 12:00:00",
                "cancellationStatus": "signed",
                "isDnsOnly": False,
                "tags": [
                    "customTag",
                    "anotherTag"
                ]
            }
        },
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api.transip.nl/v6/domains/example.com/dns",
        json={
            "dnsEntries": [
                {
                    "name": "www",
                    "expire": 86400,
                    "type": "A",
                    "content": "127.0.0.1"
                }
            ]
        },
        status=200,
    )

    domain: Type[Domain] = transip_minimal_client.domains.get("example.com")
    entries: List[Type[DnsEntry]] = domain.dns.list()  # type: ignore
    entry: Type[DnsEntry] = entries[0]
    assert len(entries) == 1
    assert entry.name == "www"  # type: ignore
