from typing import Union

from passlib.context import CryptContext

from app.api.admin.models import AdminUser
from app.api.user.models import User
from app.shared.schemas.ResponseSchemas import BaseResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def authenticate_user(email: str, password: str, admin=False) -> User:
    """
    "If the user exists and the password is correct, return the user, otherwise return False."

    The first thing we do is check if the user exists. If the user exists, we check if the password is correct. If the password is correct, we return the user. If the password is
    incorrect, we return False. If the user doesn't exist, we return False

    :param email: The email address of the user
    :type email: str
    :param password: The password to be hashed
    :type password: str
    :param admin: bool - If True, the user will be authenticated as an admin user, defaults to False (optional)
    :return: A NoneType or a User object
    """
    model = AdminUser if admin else User
    return model.where(
        email=email,
        password=get_password_hash(password),
        admin=admin
    ).first()

