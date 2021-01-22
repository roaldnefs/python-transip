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

from typing import Optional, Type, Any, Union

from transip import TransIP


class ApiObject:
    """Represents a TransIP API object."""

    _id_attr: Optional[str] = "id"

    def __init__(self, service, attrs) -> None:
        self.__dict__.update(
            {
                "service": service,
                "_attrs": attrs,
                "_updated_attrs": {}
            }
        )

    def __getattr__(self, name: str) -> Any:
        try:
            return self.__dict__["_updated_attrs"][name]
        except KeyError:
            try:
                return self.__dict__["_attrs"][name]
            except KeyError:
                raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__["_updated_attrs"][name] = value

    def __str__(self) -> str:
        return f"{type(self)} => {self._attrs}"

    def __repr__(self) -> str:
        name = self.__class__.__name__
        if self._id_attr:
            return f"<{name} {self._id_attr}:{self.get_id()}>"
        else:
            return f"<{name}>"

    def __dir__(self):
        return super().__dir__() + list(self.attrs)

    def get_id(self) -> Union[Optional[int], Optional[str]]:
        """Returns the ID of the object."""
        if self._id_attr and hasattr(self, self._id_attr):
            return getattr(self, self._id_attr)
        return None

    @property
    def attrs(self):
        """
        Returns a dictionary containing all the attributes.
        """
        attrs = self.__dict__["_updated_attrs"].copy()
        attrs.update(self.__dict__["_attrs"])
        return attrs


class ApiService:
    """Represents a TransIP API service."""

    _path: Optional[str] = None
    _obj_cls: Optional[Type[ApiObject]] = None

    def __init__(
        self,
        client: TransIP,
        parent: Optional[Type[ApiObject]] = None
    ) -> None:
        self.client: TransIP = client
        self._parent: Optional[Type[ApiObject]] = parent

    @property
    def path(self) -> Optional[str]:
        if self._path and self._parent:
            return self._path.format(
                parent_id=self._parent.get_id()  # type: ignore
            )
        return self._path
