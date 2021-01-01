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
from transip.v6.services.ssh_key import SshKey


@responses.activate
def test_ssh_keys_list(transip_minimal_client: Type[TransIP]) -> None:
    responses.add(
        responses.GET,
        "https://api.transip.nl/v6/ssh-keys",
        json={
            "sshKeys": [{
                "id": 123,
                "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDf2pxWX/yhUBDyk2LPhvRtI0LnVO8PyR5Zt6AHrnhtLGqK+8YG9EMlWbCCWrASR+Q1hFQG example",
                "description": "Jim key",
                "creationDate": "2020-12-01 15:25:01",
                "fingerprint": "bb:22:43:69:2b:0d:3e:16:58:91:27:8a:62:29:97:d1"
            }]
        },
        status=200,
    )
    
    ssh_keys: List[Type[SshKey]] = transip_minimal_client.ssh_keys.list()
    ssh_key: Type[SshKey] = ssh_keys[0] 
    assert len(ssh_keys) == 1
    assert ssh_key.get_id() == 123  # type: ignore


@responses.activate
def test_ssh_keys_get(transip_minimal_client: Type[TransIP]) -> None:
    responses.add(
        responses.GET,
        "https://api.transip.nl/v6/ssh-keys/123",
        json={
            "sshKey": {
                "id": 123,
                "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDf2pxWX/yhUBDyk2LPhvRtI0LnVO8PyR5Zt6AHrnhtLGqK+8YG9EMlWbCCWrASR+Q1hFQG example",
                "description": "Jim key",
                "creationDate": "2020-12-01 15:25:01",
                "fingerprint": "bb:22:43:69:2b:0d:3e:16:58:91:27:8a:62:29:97:d1"
            }
        },
        status=200,
    )
    
    ssh_key_id: int = 123
    ssh_key: Type[SshKey] = transip_minimal_client.ssh_keys.get(ssh_key_id)
    assert ssh_key.get_id() == 123  # type: ignore


@responses.activate
def test_ssh_keys_delete(transip_minimal_client: Type[TransIP]) -> None:
    responses.add(
        responses.DELETE,
        "https://api.transip.nl/v6/ssh-keys/123",
        status=204,
    )
    
    ssh_key_id: int = 123
    try:
        transip_minimal_client.ssh_keys.delete(ssh_key_id)
    except Exception as exc:
        assert False, f"'transip.TransIP.ssh_keys.delete' raised an exception {exc}"
