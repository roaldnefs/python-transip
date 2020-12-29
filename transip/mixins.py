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

from transip import TransIP
from transip.base import ApiObject


class GetMixin:
    """Retrieve an single ApiObject.

    Derived class must define ``_resp_get_attr``.

    ``_resp_get_attr``: The response attribute which contains the object
    """
    client: TransIP
    _obj_cls: Optional[Type[ApiObject]]
    _path: str

    _resp_get_attr: Optional[str] = None

    def get(self, id: str, **kwargs) -> Optional[Type[ApiObject]]:
        if self._obj_cls or self._path or self._resp_get_attr:
            path: str = "{path}/{id}".format(
                path=self._path,
                id=id
            )
            obj: Type[ApiObject] = self.client.get(path)[self._resp_get_attr]
            return obj
        return None


class ListMixin:
    """Retrieve a list of ApiObjects.

    Derived class must define ``_resp_list_attr``.

    ``_resp_list_attr``: The response attribute which lists all objects
    """
    client: TransIP
    _obj_cls: Optional[Type[ApiObject]]
    _path: str

    _resp_list_attr: Optional[str] = None

    def list(self, **kwargs) -> List[Type[ApiObject]]:
        objs: List[Type[ApiObject]] = []
        if self._obj_cls and self._path and self._resp_list_attr:
            for obj in self.client.get(self._path)[self._resp_list_attr]:
                objs.append(self._obj_cls(obj))  # type: ignore
        return objs
