# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Roald Nefs <info@roaldnefs.com>
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

from typing import Optional


class TransIPError(Exception):

    def __init__(self, message: str = "") -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


class TransIPHTTPError(TransIPError):

    def __init__(
        self,
        message: str = "",
        response_code: Optional[int] = None
    ) -> None:

        super().__init__(message)
        self.response_code = response_code

    def __str__(self) -> str:
        if self.response_code:
            return f"{self.response_code}: {self.message}"
        else:
            return self.message


class TransIPParsingError(TransIPError):
    pass


class TransIPIOError(TransIPError):
    pass
