"""
@author: Kuro
"""
import uuid
from datetime import datetime
from typing import List, Type, Union, Optional

import pytz
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref, defer

from app.api.agent.schema import RemoveUser
from app.api.user.schema import GetUserListItems
from app.shared.bases.base_model import ModelMixin, ModelType, Page
from app.shared.bases.base_model import paginate
from app.shared.schemas.page_schema import PagedResponse


# from app.shared.helper.logger import StandardizedLogger


class Nullable(Type):
    """
    Nullable is a class that is used to define the nullable type of a variable.
    """
    __self__: Optional[Union[bool, None]]


class User(ModelMixin):
    """
    User is a table that stores the user information.
    """

    __tablename__ = "User"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    headImage = Column(String(255), nullable=True, unique=False)
    active = Column(Boolean, default=True)
    createdAt = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    updatedAt = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    token = Column(String(255), nullable=True)
    accessToken = Column(String(255), nullable=True)
    agentId = Column(
        UUID(as_uuid=True),
        ForeignKey("Agent.id", ondelete="CASCADE", link_to_name=True),
        index=True,
        nullable=True
    )
    createdByAgent = relationship(
        "Agent",
        foreign_keys="User.agentId",
        backref=backref("users", single_parent=True),
    )

    @classmethod
    def get(cls, *_, **kwargs) -> ModelType:
        """
        The get function returns a list of all the items in the database.

        :param *_: Used to Catch all the extra arguments passed into a function.
        :param **kwargs: Used to Pass a keyworded, variable-length argument list.
        :return: The value of the key in the kwargs dictionary.

        """
        return cls.where(**kwargs).first()

    @classmethod
    def get_list_of_users(
        cls, list_of_ids: list, page: int, items: int
    ) -> PagedResponse:
        """
        The get_list_of_users function accepts a list of user ids and returns a list of users.

        :param list_of_ids:list: Used to Pass in a list of user ids.
        :param page:int: Used to Determine which page of results to return.
        :param items:int: Used to Determine how many items to display per page.
        :param user_id:str: Used to Filter the users by their ownerId.
        :return: A list of user objects.

        """
        users = cls.where(user_id__in=list_of_ids)
        return paginate(users, page, items)

    @classmethod
    def get_all_users(cls, page_cursor: int, num_items: int) -> GetUserListItems:
        """
        > This function returns a list of users, paginated by the `pages_cursor` and `num_items` parameters

        :param cls: The class of the model you want to paginate
        :param page_cursor: The page number to start from
        :param num_items: The number of items to return per page
        :return: A dictionary of the paginated results.
        """
        query = cls.where().options(defer("password"))
        return paginate(query, page_cursor, num_items)

    @classmethod
    def remove_user(cls, *_, **kwargs) -> Optional[RemoveUser]:
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
        try:
            if user := cls.where(**kwargs):
                user.delete()
                cls.session.commit()
                return RemoveUser(**kwargs)

        except Exception as e:
            cls.session.rollback()
            print(e)
            return

    @classmethod
    def update_user(cls, *_, **kwargs) -> ModelType:
        """
        The update_user function updates a user's information.

        :param cls: Used to Refer to the class itself, which is user in this case.
        :param *_: Used to Pass a variable number of arguments to a function.
        :param **kwargs: Used to Allow the user to specify any number of key-value pairs in the function call.
        :return: A dictionary containing the user data.
        """
        try:
            user_id = kwargs.pop("id")
            user = cls.where(id=user_id)
            user.update(kwargs)
            cls.session.commit()
            return user.first()
        except Exception as e:
            cls.session.rollback()
            print(e)
            return

