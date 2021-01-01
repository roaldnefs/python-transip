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
from transip.mixins import GetMixin, DeleteMixin, ListMixin
from transip.v6.objects.ssh_key import SshKey


class SshKey(ApiObject):

    _id_attr: str = "id"


class SshKeyService(GetMixin, DeleteMixin, ListMixin, ApiService):

    _path: str = "/ssh-keys"
    _obj_cls: Optional[Type[ApiObject]] = SshKey

    _resp_list_attr: str = "sshKeys"
    _resp_get_attr: str = "sshKey"
