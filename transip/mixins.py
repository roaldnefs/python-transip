# -*- coding: utf-8 -*-
#
# Copyright (C) 2020, 2021 Roald Nefs <info@roaldnefs.com>
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

from typing import Optional, List, Type, Dict, Any, Tuple, Union

from transip import TransIP
from transip.base import ApiObject, ApiService


# Typing alias for the _create_attrs attribute in the CreateMixin
CreateAttrsTuple = Tuple[
    Union[Tuple[()], Tuple[str, ...]],
    Union[Tuple[()], Tuple[str, ...]]
]
# Typing alias for the _update_attrs attribute in the UpdateMixin
UpdateAttrsTuple = CreateAttrsTuple


class GetMixin:
    """Retrieve an single ApiObject.

    Derived class must define ``_resp_get_attr``.

    ``_resp_get_attr``: The response attribute which contains the object
    """
    client: TransIP
    _obj_cls: Optional[Type[ApiObject]]
    path: str

    _resp_get_attr: Optional[str] = None

    def get(self, id: str, **kwargs) -> Optional[Type[ApiObject]]:
        if self._obj_cls or self.path or self._resp_get_attr:
            obj: Type[ApiObject] = self._obj_cls(  # type: ignore
                self,
                self.client.get(f"{self.path}/{id}")[self._resp_get_attr]
            )
            return obj
        return None


class DeleteMixin:
    """Delete a single ApiObject."""

    client: TransIP
    path: str

    def delete(self, id: str, **kwargs) -> None:
        if self.path:
            self.client.delete(f"{self.path}/{id}")


class ObjectDeleteMixin:
    """Delete a single ApiObject."""

    service: ApiService

    def delete(self) -> None:
        if self.get_id():  # type: ignore
            self.service.delete(self.get_id())  # type: ignore


class ListMixin:
    """Retrieve a list of ApiObjects.

    Derived class must define ``_resp_list_attr``.

    ``_resp_list_attr``: The response attribute which lists all objects
    """
    client: TransIP
    path: str
    _obj_cls: Optional[Type[ApiObject]]

    _resp_list_attr: Optional[str] = None

    def list(self, **kwargs) -> List[Type[ApiObject]]:
        objs: List[Type[ApiObject]] = []
        if self._obj_cls and self.path and self._resp_list_attr:
            for obj in self.client.get(self.path)[self._resp_list_attr]:
                objs.append(self._obj_cls(self, obj))  # type: ignore
        return objs


class UpdateMixin:
    """Update an ApiObject.
    """

    client: TransIP
    path: str

    _req_update_attr: Optional[str] = None
    _update_attrs: Optional[CreateAttrsTuple] = None

    def get_update_attrs(self) -> Tuple[
        Union[Tuple[()], Tuple[str, ...]],
        Union[Tuple[()], Tuple[str, ...]]
    ]:
        """Return the required and optional attributes for updating a new
        object.

        Returns:
            tuple: a tuple containing a tuple of required and optional
                attributes.
        """
        if not self._update_attrs:
            return (tuple(), tuple())
        else:
            return self._update_attrs

    def _check_update_attrs(self, attrs) -> None:
        """Check required attributes.

        Raises:
            AttributeError: If any of the required attributes is missing.
        """
        required, optional = self.get_update_attrs()
        missing = [attr for attr in required if attr not in attrs]

        if missing:
            attrs_str = "', '".join(missing)
            raise AttributeError((
                f"'{self.__class__.__name__}' object has no "
                f"attribute{'s'[:len(missing)!=1]} '{attrs_str}'"
            ))

    def update(
        self,
        id: Any,
        data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> None:
        if data is None:
            data = {}

        # Check if all required attributes are supplied
        self._check_update_attrs(data)

        # Some endpoints require the attributes to be packed in dictionary with
        # a specific key while others endpoint do not
        if self._req_update_attr:
            data = {self._req_update_attr: data}

        if self.path:
            self.client.put(f"{self.path}/{id}", json=data)


class CreateMixin:
    """
    Create a new ApiObject.
    """
    client: TransIP
    path: str

    _req_create_attr: Optional[str] = None
    _create_attrs: Optional[CreateAttrsTuple] = None

    def _check_create_attrs(self, attrs) -> None:
        """Check required attributes.

        Raises:
            AttributeError: If any of the required attributes is missing.
        """
        required, optional = self.get_create_attrs()
        missing = [attr for attr in required if attr not in attrs]

        if missing:
            attrs_str = "', '".join(missing)
            raise AttributeError((
                f"'{self.__class__.__name__}' object has no "
                f"attribute{'s'[:len(missing)!=1]} '{attrs_str}'"
            ))

    def get_create_attrs(self) -> Tuple[
        Union[Tuple[()], Tuple[str, ...]],
        Union[Tuple[()], Tuple[str, ...]]
    ]:
        """Return the required and optional attributes for creating a new
        object.

        Returns:
            tuple: a tuple containing a tuple of required and optional
                attributes.
        """
        if not self._create_attrs:
            return (tuple(), tuple())
        else:
            return self._create_attrs

    def create(self, data: Optional[Dict[str, Any]] = None, **kwargs):
        if data is None:
            data = {}

        # Check if all required attributes are supplied
        self._check_create_attrs(data)

        # Some endpoints require the attributes to be packed in dictionary with
        # a specific key while others endpoint do not
        if self._req_create_attr:
            data = {self._req_create_attr: data}

        if self.path:
            self.client.post(self.path, json=data)
