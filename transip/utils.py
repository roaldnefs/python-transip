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

import base64
import os
import secrets
import string

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15


def load_rsa_private_key(key: str) -> RSAPrivateKey:
    """
    Convert the private key string to RSAPrivateKey object.
    
    Returns:
        RSAPrivateKey: The private RSA key.
    """
    # Convert the key string to bytes
    if isinstance(key, str):
        key: bytes = key.encode()
    
    return serialization.load_pem_private_key(
        key, password=None, backend=default_backend()
    )


def generate_message_signature(message: str, private_key: str) -> str:
    """Return the BASE64 encoded SHA514 signature of a message.
    
    Args:
        message (str): The message to sign.
        private_key (str): The private key content used to sign the message.
    
    Returns:
        str: The BASE64 encoded SHA514 signature of a message.
    """
    # Convert the message string to bytes
    if isinstance(message, str):
        message: bytes = message.encode()

    # Convert the private key content to a RSAPrivateKey object
    if isinstance(private_key, str):
        private_key: RSAPrivateKey = load_rsa_private_key(private_key)

    # Sign the message using the RSAPrivateKey object
    signature: str = private_key.sign(message, PKCS1v15(), SHA512())

    # Return the BASE64 encoded SHA512 signature
    return base64.b64encode(signature)


def generate_nonce(length: int) -> str:
    """
    Generate a nonce.

    Args:
        length (int): The number of characters to return.

    Returns:
        str: The nonce of specified characters.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))
