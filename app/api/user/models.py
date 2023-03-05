import uuid
from datetime import datetime
from typing import Optional, Generator, Union

import pytz
from fastapi_sqlalchemy import db
from sqlalchemy import (
    Column,
    String,
    Date,
    Boolean,
    DateTime,
    Text,
    and_,
    or_,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.util import counter

from app.api.admin.models import AdminUser, AdminRole
from app.api.admin.schema import BaseUser
from app.shared.bases.base_model import ModelMixin, ModelType
from app.shared.bases.base_model import paginate
from app.shared.exception.utils import safe
from app.shared.schemas.ExceptionSchema import SafeException
from app.api.user import schema
from app.shared.helper.logger import StandardizedLogger

logger = StandardizedLogger(__name__)


class User(ModelMixin):
    """
    One Declarative Schema to rule them all and in the darkness bind them
    """

    __tablename__ = "user"
    id: Column = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Column = Column(String(80), unique=True, nullable=True)
    username: Column = Column(String(80), unique=True, nullable=True)
    password: Column = Column(String(256), unique=False, nullable=True)
    name: Column = Column(Text, nullable=False)
    access_token: Column = Column(Text, nullable=True)
    id_token: Column = Column(Text, nullable=True)
    active: Column = Column(Boolean, default=True)
    created_at: Column = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    updated_at = Column(DateTime, nullable=True)
    qa_bypass = Column(Boolean, default=False)
    error: Optional[str] = None
    created_by_id = Column(
        UUID(as_uuid=True), ForeignKey(AdminUser.id, ondelete="CASCADE"), index=True
    )
    created_by = relationship(
        "AdminUser",
        foreign_keys="User.created_by_id",
        backref=backref("admin", single_parent=True),
    )

    @classmethod
    def get(cls, *_, **kwargs):
        """
        The get function returns a list of all the items in the database.

        :param *_: Used to Catch all the extra arguments passed into a function.
        :param **kwargs: Used to Pass a keyworded, variable-length argument list.
        :return: The value of the key in the kwargs dictionary.

        """
        return cls.where(**kwargs).first()

    @classmethod
    def load_user(cls, user_id):
        """
        The load_user function is used to load a user from the database.
        It takes in an id as a parameter and returns a dictionary containing the user's information.

        :param user_id: Used to Query the database for a user with the given id.
        :return: A dictionary with the following keys:.
        """
        user = cls.where(id=user_id).first()
        return (
            {
                "success": True,
                "user_id": user.id,
                "email": user.email,
                "name": user.name,
                "created_at": user.created_at,
            }
            if user
            else {"success": False, "error": "no such user"}
        )

    @classmethod
    def get_list_of_users(cls, list_of_ids: list, page: int, items: int, user_id: str):
        """
        The get_list_of_users function accepts a list of user ids and returns a list of users.

        :param list_of_ids:list: Used to Pass in a list of user ids.
        :param page:int: Used to Determine which page of results to return.
        :param items:int: Used to Determine how many items to display per page.
        :param user_id:str: Used to Filter the users by their owner_id.
        :return: A list of user objects.

        """
        users = db.session.query(
            User.id,
            User.username,
            User.name,
        )
        user_pages = paginate(users, page, items)
        response = user_pages.as_dict()
        response["items"] = list(
            reversed([schema.User(**x) for x in user_pages.dict_items])
        )
        return response

    @classmethod
    def get_all_users(cls, page, items):
        """
        The get_all_users function returns all users in the database.

        :param page: Used to Determine which page of results to fetch.
        :param items: Used to Limit the number of users returned.
        :return: A list of all the users in the database.
        """
        users = db.session.query(User)
        return paginate(users, page, items).as_dict()

    @classmethod
    @safe
    def create_user(cls, *_, **kwargs) -> Union[dict, SafeException]:
        """
        The create_user function creates a new user in the database.
        It takes as input a dictionary of data, and returns an object with that data.
        The function also adds the user to the search index.

        :param cls: Used to Refer to the class itself, so that we can call methods of the class.
        :param *_: Used to Catch all the extra arguments passed in that are not explicitly defined.
        :param **kwargs: Used to Catch all the extra arguments passed in that are not explicitly defined.
        :return: The user object that was created.
        """
        user_data = cls.rebuild(kwargs)
        base_data = BaseUser(**user_data)
        constraints = [
            User.username == base_data.username,
            User.email == base_data.email,
        ]
        predicate = {"id_": "x"}
        user = cls.where(
            cls.filter_expr(or_=[or_(*constraints), and_(*constraints)])
        ).create(**user_data)
        return SafeException(**cls.build_response(user))

    @classmethod
    def remove_user(cls, *_, **kwargs) -> dict:
        """
        The remove_user function removes a user from the database.
        It takes one argument, which is the id of the user to be removed.
        The function then removes that user from all tables in the database
        and returns a dictionary with two keys: 'success' and 'message'.
        If successful, success will be True and message will contain an empty string.
        if unsuccessful, success will be False and message will contain an error message.

        :param cls: Used to Refer to the class itself, which is user in this case.
        :param *_: Used to Catch all the extra parameters that are passed into a function.
        :param **kwargs: Used to Pass keyworded variable length of arguments to a function.
        :return: A dictionary with the key 'success' and a boolean value of true.
        """
        user_id = kwargs.get("id")
        cls.where(**kwargs).delete().save()
        return cls.build_response(user_id)

    @classmethod
    def update_user(cls, *_, **kwargs) -> dict:
        """
        The update_user function updates a user's information.

        :param cls: Used to Refer to the class itself, which is user in this case.
        :param *_: Used to Pass a variable number of arguments to a function.
        :param **kwargs: Used to Allow the user to specify any number of key-value pairs in the function call.
        :return: A dictionary containing the user data.
        """
        filters = dict(
            user_id=kwargs.get("id"),
            user_name=kwargs.get("name"),
            user_username=kwargs.get("username"),
        )
        user = cls.where(**{k: v for k, v in filters.items() if v}).update(**kwargs)
        return cls.build_response(user.id)

    @classmethod
    def admin_search_users(cls, *_, **kwargs) -> list:
        """
        The admin_search_users function allows an admin user to search for users by various criteria.
        The function accepts a dictionary of key-value pairs as input, and returns a list of dictionaries
        of matching users. The keys in the input dictionary can be any field in the User model, and each value
        can be either a single string or an iterable containing strings.

        note: the filter will search by phone OR email if provided, and if not,
        ALL criteria so pass explicit fields to search by.

        :param *_: Used to Catch any additional arguments that are passed in, but not used by the function.
        :param **kwargs: Used to Allow the caller to pass in a dictionary of key/value pairs that will be used as filters for the query.
        :return: A list of users that match the filters in kwargs.
        """
        filters = cls.build_filters(kwargs)
        return cls.where(**filters).all()

    @classmethod
    def user_claims(cls, user_id):
        """
        It takes a user_id, checks if it's an email, phone, or id, and returns a payload with the user_id, user_phone, admin, and admin_role

        :param cls: The class of the resource
        :param user_id: The user_id is the unique identifier for the user. It can be a phone number, email address, or a unique identifier
        :return: A dictionary with the user_id, user_phone, admin, and admin_role.
        """
        user: ModelType = None
        admin = False
        if "+" in str(user_id):
            user = User.get(phone=user_id)
        if "@" in str(user_id):
            user = User.get(email=user_id)
        if len(str(user_id)) > 30:
            user = User.get(id=user_id)
        if not user:
            user = AdminUser.get_admin_by_email(email=user_id)
            admin = True
        if not user:
            return None
        admin_role = AdminRole.get_user_role(user_id=user.id)

        payload = schema.CLaimAuthPayload(**user.to_dict())
        if admin_role:
            payload["admin"] = admin
            payload["admin_role"] = admin_role
        return payload
