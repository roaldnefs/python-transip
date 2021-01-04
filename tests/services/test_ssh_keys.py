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

from typing import Type, List, Tuple, Any, Dict
import responses  # type: ignore
import json
import pytest
import unittest

from transip import TransIP
from transip.v6.services.ssh_key import SshKey
from tests.utils import load_responses_fixture


@pytest.mark.usefixtures("minimal_client_class")
class SshKeysTest(unittest.TestCase):
    """Test the SshKeyService."""

    client: Type[TransIP]

    def setUp(self):
        # Setup mocked responses for the /ssh-keys endpoint
        load_responses_fixture("ssh-keys.json")

    @responses.activate
    def test_list(self) -> None:
        ssh_keys: List[Type[SshKey]] = self.client.ssh_keys.list()
        ssh_key: Type[SshKey] = ssh_keys[0]

        assert len(ssh_keys) == 1
        assert ssh_key.get_id() == 123  # type: ignore

    @responses.activate
    def test_get(self) -> None:
        ssh_key_id: int = 123
        ssh_key: Type[SshKey] = self.client.ssh_keys.get(ssh_key_id)

        assert ssh_key.get_id() == 123  # type: ignore

    @responses.activate
    def test_delete(self) -> None:
        ssh_key_id: int = 123
        try:
            self.client.ssh_keys.delete(ssh_key_id)
        except Exception as exc:
            assert False, f"'transip.TransIP.ssh_keys.delete' raised an exception {exc}"

    @responses.activate
    def test_create(self) -> None:
        ssh_key_data: Dict[str, str] = {
            "sshKey": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDf2pxWX/yhUBDyk2LPhvRtI0LnVO8PyR5Zt6AHrnhtLGqK+8YG9EMlWbCCWrASR+Q1hFQG example",
            "description": "Jim key"
        }
        self.client.ssh_keys.create(ssh_key_data)

        assert len(responses.calls) == 1

    @responses.activate
    def test_update(self) -> None:
        ssh_key_id: int = 123
        ssh_key_data: Dict[str, str] = {
            "description": "Jim key"
        }

        try:
            self.client.ssh_keys.update(ssh_key_id, ssh_key_data)
        except Exception as exc:
            assert False, f"'transip.TransIP.ssh_keys.update' raised an exception {exc}"
