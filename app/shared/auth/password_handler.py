"""
@author: Kuro
"""
from typing import Union

from passlib.context import CryptContext
from app.shared.schemas.ResponseSchemas import BaseResponse

pwd_context = CryptContext(schemes=["hex_md5"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    It takes a plain text password and a hashed password and returns True if the plain text password matches the hashed password

    :param plain_password: The password that the user entered
    :type plain_password: str
    :param hashed_password: The hashed password that you want to verify
    :type hashed_password: str
    :return: A boolean value.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    It takes a string and returns a string

    :param password: The password to hash
    :type password: str
    :return: A string
    """
    return pwd_context.hash(password)

