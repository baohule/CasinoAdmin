"""
@author: Kuro
"""
import uuid
from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from app.shared.bases.base_model import ModelMixin, paginate, ModelType
from app.shared.schemas.ResponseSchemas import BaseResponse
from app.shared.schemas.page_schema import PagedResponse


class Admin(ModelMixin):
    """
    Admin is a table that stores the admin information.
    """

    __tablename__ = "Admin"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    firstName = Column(String(255), nullable=True)
    lastName = Column(String(255), nullable=True)
    token = Column(String(255), nullable=True)
    createdAt = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    updatedAt = Column(DateTime, nullable=True)
    accessToken = Column(String(255), nullable=True)

    @classmethod
    def add_admin(cls, *_, **kwargs):
        """
        The add_admin function creates a new admin object.
        It takes in the following parameters:
            * _ - A list of objects that will be ignored by the
            function. These are usually objects passed into a function
            automatically, like HTTP request or database connections.
            * kwargs - Keyword arguments corresponding to fields in an admin object.

        :param cls: Used to Call the class itself.
        :param *_: Used to Catch any additional parameters that may be passed in.
        :param **kwargs: Used to Pass keyworded variable length of arguments to a function.
        :return: The admin instance.

        """
        try:
            admin_data = cls.rebuild(kwargs)
            if cls.where(email=admin_data["email"]).first():
                return
            admin = cls(**admin_data)
            cls.session.add(admin)
            cls.session.commit()
            return admin
        except Exception as e:
            cls.session.rollback()
            print(e)
            return

    @classmethod
    def update_admin_user(cls, *_, **kwargs) -> ModelType:
        """
        The update_admin_user function updates the admin user with the given id.
        It takes in a dictionary of key value pairs to update and returns a dictionary of updated values.

        :param cls: Used to Refer to the class itself.
        :param *_: Used to Catch all the extra parameters that are passed in to the function.
        :param **kwargs: Used to Allow for any number of additional arguments to be passed into the function.
        :return: A dictionary of the updated admin user.

        """
        try:
            admin_user_id = kwargs.get("id")
            kwargs["updatedAt"] = datetime.now(pytz.utc)
            return cls.where(id=admin_user_id).update(**kwargs)
        except Exception as e:
            cls.session.rollback()
            print(e)
            return

    @classmethod
    def list_all_admin_users(cls, page, num_items) -> PagedResponse:
        """
        The list_all_admin_users function returns a list of all admin users in the database.

        :param cls: Used to Refer to the class itself, rather than an instance of the class.
        :return: A dictionary of all the admin users in a class.
        """
        users = cls.where()
        return paginate(users, page, num_items)

    @classmethod
    def search_admins(cls, *_, **kwargs) -> BaseResponse:
        """
        The search_admins function searches for admins based on the given filters.

        :param cls: Used to Indicate the class that is being used to query the database.
        :param *_: Used to Catch any additional positional arguments that are passed in.
        :param **kwargs: Used to Pass a variable number of keyword arguments to a function.
        :return: A dictionary.

        """
        filters = cls.build_filters(kwargs)
        return cls.where(**filters).all()

    @classmethod
    def get_admin_by_email(cls, email: str) -> ModelType:
        """
        The get_admin_by_email function accepts an email address as a string and returns the admin that
        is associated with that email address.

        :param cls: Used to Reference the class that is being called.
        :param email:str: Used to Specify the email of the admin that is being searched for.
        :return: A dictionary containing the admin's information.

        """
        return cls.where(email=email).first()

    @classmethod
    def get_admin_by_id(cls, user_id: UUID) -> ModelType:
        """
        The get_admin_by_id function accepts a user_id and returns the admin associated with that id.

        :param cls: Used to Reference the class that is being called.
        :param user_id:UUID: Used to Specify the user_id of the admin that is being searched for.
        :return: The admin details for the user with the given id.

        """
        return cls.where(id=user_id).first()
