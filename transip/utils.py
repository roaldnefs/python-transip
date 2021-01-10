# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Roald Nefs <info@roaldnefs.com>
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

from typing import Union

import base64
import secrets
import string

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15


def load_rsa_private_key(key: Union[bytes, str]) -> RSAPrivateKey:
    """
    Convert the private key string to RSAPrivateKey object.

    Returns:
        RSAPrivateKey: The private RSA key.
    """
    # Convert the key string to bytes
    if isinstance(key, str):
        key = key.encode()

    return serialization.load_pem_private_key(
        key, password=None, backend=default_backend()
    )


def generate_message_signature(
    message: Union[str, bytes],
    private_key: Union[RSAPrivateKey, str]
) -> str:
    """Return the BASE64 encoded SHA514 signature of a message.

    Args:
        message (str): The message to sign.
        private_key (str): The private key content used to sign the message.

    Returns:
        str: The BASE64 encoded SHA514 signature of a message.
    """
    # Convert the message string to bytes
    if isinstance(message, str):
        message = message.encode()

    # Convert the private key content to a RSAPrivateKey object
    if isinstance(private_key, str):
        private_key = load_rsa_private_key(private_key)

    # Sign the message using the RSAPrivateKey object
    signature: bytes = private_key.sign(message, PKCS1v15(), SHA512())

    # Return the BASE64 encoded SHA512 signature
    b64_bytes: bytes = base64.b64encode(signature)
    return b64_bytes.decode('ascii')


def generate_nonce(length: int, alphabet: str = None) -> str:
    """
    Generate a nonce.

    Args:
        length (int): The number of characters to return.
        alphabet (str): The alphabet to choose characters from, defaults to
            ascii leters and digits.

    Returns:
        str: The nonce of specified characters.
    """
    if not length >= 1:
        raise ValueError(
            "The specified nonce length must greater or equal to 1"
        )

    alphabet = alphabet or (string.ascii_letters + string.digits)
    return ''.join(secrets.choice(alphabet) for i in range(length))
