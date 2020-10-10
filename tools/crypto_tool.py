import os

import bcrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from errors.error_handler import InvalidUsageException
import hashlib


def sha512(data, salt=""):
    return hashlib.sha512((data + salt).encode("utf-8")).hexdigest()


def sha256(data, salt=""):
    return hashlib.sha256((data + salt).encode("utf-8")).digest()


def sha256_hex(data, salt=""):
    return hashlib.sha256((data+salt).encode("utf-8")).hexdigest()


# constant-time algorithms
def slow_is_equal(a, b):
    if len(a) != len(b):
        return False
    if isinstance(a, str):
        a = a.encode()
    if isinstance(b, str):
        b = b.encode()
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0


def urandom(size=64):
    return os.urandom(size).hex()


def AES(data, key, nonce, entype="AES_GCM", associated_data=None):
    if isinstance(data, str):
        data = data.encode("utf-8")
    if entype == "AES_GCM":

        aesgcm = AESGCM(key)
        if nonce is None:
            nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, data, associated_data)
        return ct
    else:
        raise InvalidUsageException(10005)


def deAES(data, key, nonce, entype="AES_GCM", associated_data=None):
    if entype == "AES_GCM":
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, data, associated_data)
    else:
        raise InvalidUsageException(10006)


def get_bcrypt_salt():
    return bcrypt.gensalt(prefix=b"2a")
