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

from typing import Optional, Type, Any

from transip import TransIP


class ApiObject:
    """Represents a TransIP API object."""

    _id_attr: str = "id"
    
    def __init__(self, attrs) -> None:
        self.__dict__["_attrs"] = attrs

    def __getattr__(self, name: str) -> Any:
        try:
            return self.__dict__["_attrs"][name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__["_attrs"][name] = value

    def __str__(self) -> str:
        return "{} => {}".format(type(self), self._attrs)

    def __repr__(self) -> str:
        name = self.__class__.__name__
        if self._id_attr:
            return "<{name} {id}:{value}>".format(
                name=name,
                id=self._id_attr,
                value=self.get_id()
            )
        else:
            return "<{name}>".format(name=name)

    def __dir__(self):
        return super().__dir__() + list(self.attrs)

    def get_id(self) -> Any:
        """Returns the id of the object."""
        if not hasattr(self, self._id_attr):
            None
        return getattr(self, self._id_attr)

    @property
    def attrs(self):
        return self.__dict__["_attrs"]


class ApiService:
    """Represents a TransIP API service."""

    _path: Optional[str] = None
    _obj_cls: Optional[ApiObject] = None

    def __init__(self, client: TransIP) -> None:
        self.client: TransIP = client
