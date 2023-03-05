import datetime

import pytz
from fastapi_sqlalchemy import db
from sqlalchemy import Column, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.shared.bases.base_model import ModelMixin
from fastapi.logger import logger


class AdminRole(ModelMixin):
    """
    Is's a table that holds the roles of the admin users.
    """

    __tablename__ = "admin_role"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(Text, unique=True)
    can_list_users = Column(Boolean)
    can_get_user = Column(Boolean)
    can_create_user = Column(Boolean)
    can_create_admin = Column(Boolean)
    can_delete_user = Column(Boolean)
    can_alter_user = Column(Boolean)
    can_search_users = Column(Boolean)
    can_batch_alter_users = Column(Boolean)
    can_set_perms = Column(Boolean, default=False)
    bypass_auth = Column(Boolean)
    active = Column(Boolean, default=True)
    superuser = Column(Boolean, default=False)
    updated_at = Column(DateTime, nullable=True)

    @classmethod
    def get_all_roles(
        cls,
    ) -> dict:
        """
        The get_all_roles function returns a dictionary of all roles in the database.

        :returns: A dictionary containing all roles in the database.

        :param cls: Used to Call the class itself.
        :param : Used to Define the class that is used to get all roles.
        :return: A dictionary of all the roles in the class.


        """
        return cls.build_response(cls.all())

    @classmethod
    def get_user_role(cls, user_id) -> dict:
        """
        The get_user_role function returns a dictionary containing the role of the user
        with id = user_id. If no such user exists, it returns None.

        :param cls: Used to Access the adminrole class.
        :param user_id: Used to Find the user in the database.
        :return: A dictionary containing the user's role.
        """
        role = cls.where(AdminRole___admin__id=user_id).first()
        return cls.build_response(role)

    @classmethod
    def set_user_role(cls, *_, **kwargs) -> dict:
        """
        The set_user_role function is used to set the role of a user.
        It takes in a user_id and role as arguments, and returns the updated User object.

        :param cls: Used to Call the class method of the user model.
        :param *_: Used to Ignore all additional keyword arguments.
        :param **kwargs: Used to Pass keyworded variable length of arguments to a function.
        :return: A dictionary containing the user_id and role.


        """
        user_id = kwargs.pop("user_id", None)
        role = cls.where(id=user_id).update(**kwargs)
        return cls.build_response(role)

    @classmethod
    def alter_role_perms(cls, *_, **kwargs):
        """
        The alter_role_perms function is used to alter the permissions of a role.
        It takes in a list of permission names and removes them from the role,
        if they exist. If they don't exist, it adds them to the role.

        :param cls: Used to Access the class of the object that is being altered.
        :param *_: Used to Pass a variable number of arguments to a function.
        :param **kwargs: Used to Pass a variable number of keyword arguments to a function.
        :return: The update_at column of the role table.


        """
        kwargs["update_at"] = datetime.datetime.now(pytz.utc)
        role = cls.where(id=kwargs.get("role_id")).update(**kwargs)
        return cls.build_response(role)


#
class AdminUser(ModelMixin):
    """
    `AdminUser` is a class that is used to represent an admin user.
    """

    __tablename__ = "admin_user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(Text, unique=True)
    password = Column(Text)
    name: Column = Column(Text)
    role_id = Column(
        UUID(as_uuid=True), ForeignKey(AdminRole.id, ondelete="CASCADE"), index=True
    )
    active = Column(Boolean, default=True)
    token = Column(Text)
    role = relationship(
        "AdminRole",
        foreign_keys="AdminUser.role_id",
        backref=backref("admin", single_parent=True),
    )
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(pytz.utc))
    updated_at = Column(DateTime, nullable=True)
    access_token: Column = Column(Text, nullable=True)
    id_token: Column = Column(Text, nullable=True)

    @classmethod
    def add_admin(cls, *_, **kwargs):
        """
        The add_admin function creates a new admin object.
        It takes in the following parameters:
            * _ - A list of objects that will be ignored by the function. These are usually objects passed into a function automatically, like HTTP request or database connections.
            * kwargs - Keyword arguments corresponding to fields in an admin object.

        :param cls: Used to Call the class itself.
        :param *_: Used to Catch any additional parameters that may be passed in.
        :param **kwargs: Used to Pass keyworded variable length of arguments to a function.
        :return: The admin instance.

        """
        admin_data = cls.rebuild(kwargs)
        admin = cls.create(**admin_data)
        return cls.build_response(admin)

    @classmethod
    def update_admin_user(cls, *_, **kwargs) -> dict:
        """
        The update_admin_user function updates the admin user with the given id.
        It takes in a dictionary of key value pairs to update and returns a dictionary of updated values.

        :param cls: Used to Refer to the class itself.
        :param *_: Used to Catch all the extra parameters that are passed in to the function.
        :param **kwargs: Used to Allow for any number of additional arguments to be passed into the function.
        :return: A dictionary of the updated admin user.

        """
        admin_user_id = kwargs.get("id")
        kwargs["updated_at"] = datetime.datetime.now(pytz.utc)
        admin = cls.where(id=admin_user_id).update(**kwargs)
        return cls.build_response(admin.id)

    @classmethod
    def list_all_admin_users(cls) -> dict:
        """
        The list_all_admin_users function returns a list of all admin users in the database.

        :param cls: Used to Refer to the class itself, rather than an instance of the class.
        :return: A dictionary of all the admin users in a class.

        """
        return cls.build_response(cls.all())

    @classmethod
    def get_admins_by_role(cls, role_id: str) -> dict:
        """
        The get_admins_by_role function returns a list of all admins with the specified role.

        :param cls: Used to Access the class object.
        :param role_id:str: Used to Specify which role to return the admins for.
        :return: A dictionary of all the admins.

        """
        return cls.build_response(cls.where(role_id=role_id).all())

    @classmethod
    def search_admins(cls, *_, **kwargs) -> dict:
        """
        The search_admins function searches for admins based on the given filters.

        :param cls: Used to Indicate the class that is being used to query the database.
        :param *_: Used to Catch any additional positional arguments that are passed in.
        :param **kwargs: Used to Pass a variable number of keyword arguments to a function.
        :return: A dictionary.

        """
        filters = AdminUser.build_filters(kwargs)
        return cls.build_response(cls.where(**filters).all())

    @classmethod
    def get_admin_by_email(cls, email: str) -> dict:
        """
        The get_admin_by_email function accepts an email address as a string and returns the admin that is associated with that email address.

        :param cls: Used to Reference the class that is being called.
        :param email:str: Used to Specify the email of the admin that is being searched for.
        :return: A dictionary containing the admin's information.

        """
        return cls.build_response(cls.where(email=email).first())

    @classmethod
    def get_admin_by_id(cls, user_id: UUID) -> dict:
        """
        The get_admin_by_id function accepts a user_id and returns the admin associated with that id.

        :param cls: Used to Reference the class that is being called.
        :param user_id:UUID: Used to Specify the user_id of the admin that is being searched for.
        :return: The admin details for the user with the given id.

        """
        return cls.build_response(cls.where(id=user_id).first())
