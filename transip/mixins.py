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

from typing import Optional, List, Type

from transip.base import ApiObject


class ListMixin:
    """Retrieve a list of ApiObjects.

    Derived class must define ``_resp_list_attr``.

    ``_resp_list_attr``: The response attribute which lists all objects
    """

    _resp_list_attr: Optional[str] = None

    def list(self, **kwargs) -> List[Type[ApiObject]]:
        objs: List[Type[ApiObject]] = []
        for obj in self.client.get(self._path)[self._resp_list_attr]:
            objs.append(self._obj_cls(obj))
        return objs
