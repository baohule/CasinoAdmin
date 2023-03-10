import datetime

import pytz
from fastapi_sqlalchemy import db
from sqlalchemy import Column, Boolean, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.api.admin.schema import AdminSetRole, AdminRoleCreate
from app.shared.bases.base_model import ModelMixin, paginate
from fastapi.logger import logger


from typing import Optional, Dict
from pydantic import BaseModel



class AdminRole(ModelMixin):
    """
    Is's a table that holds the roles of the admin users.
    """

    __tablename__ = "admin_role"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(Text, unique=True)
    parameters = Column(JSON)

    @classmethod
    def set_admin_role(cls, role_data: AdminSetRole) -> dict:
        """

        :param cls: Used to Call the class method of the AdminRole model.
        :param role_data: An object of the AdminRoleCreate model.
        :return: A dictionary containing the created Admin Role.

        """
        role_data_dict = role_data.dict()
        if "parameters" in role_data_dict and role_data_dict["parameters"] is None:
            role_data_dict.pop("parameters")
        role_change = AdminUser.where(
            id=role_data_dict["owner_id"]
        ).update({"role_id": role_data_dict["role_name"]})
        return cls.build_response(role_change)


    @classmethod
    def create_role(cls, role_data: AdminRoleCreate) -> dict:
        """
        The create_role function is used to create a new Admin Role.
        It takes in a AdminRoleCreate object as an argument, and returns a dictionary containing the
        created Admin Role.

        :param cls: Used to Call the class method of the AdminRole model.
        :param role_data: An object of the AdminRoleCreate model.
        :return: A dictionary containing the created Admin Role.

        """
        role_data_dict = role_data.dict()
        if "parameters" in role_data_dict and role_data_dict["parameters"] is None:
            role_data_dict.pop("parameters")
        role = cls.create(**role_data_dict)
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
        role_id = kwargs.pop("role_id")
        admin_id = kwargs.pop("admin_id")
        role = cls.where(role=role_id).update(**kwargs)
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
        if cls.where(email=admin_data['email']).first():
            return cls.build_response(error="User already exists")
        admin = cls(**admin_data)
        cls.session.add(admin)
        cls.session.commit()
        return cls.build_response(admin.id)

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
    def list_all_admin_users(cls, page, num_items) -> dict:
        """
        The list_all_admin_users function returns a list of all admin users in the database.

        :param cls: Used to Refer to the class itself, rather than an instance of the class.
        :return: A dictionary of all the admin users in a class.

        """
        users = cls.session.query(
            cls.id,
            cls.email,
        )
        user_pages = paginate(users, page, num_items)
        response = user_pages.as_dict()
        response["items"] = list(
            reversed([cls(**x) for x in user_pages.dict_items])
        )
        return cls.build_response(response)



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


class AdminRolePermission(ModelMixin):
    """
    IIs's a table that holds the permissions of the admin roles.
    """

    __tablename__ = "admin_role_permission"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    role_id = Column(
        UUID(as_uuid=True), ForeignKey("admin_role.id", ondelete="CASCADE"), index=True
    )
    permission = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(pytz.utc))
    updated_at = Column(DateTime, nullable=True)

    role = relationship(
        "AdminRole", foreign_keys="AdminRolePermission.role_id", backref="permissions"
    )

    @classmethod
    def add_permission(cls, permission_data: dict):
        """
        The add_permission function creates a new Admin Role Permission.
        It takes in a dictionary as an argument, containing the following keys:
        * role_id
        * permission

        :param cls: Used to Call the class itself.
        :param permission_data: A dictionary containing the role_id and permission.
        :return: The new Admin Role Permission.

        """
        permission = cls.create(**permission_data)
        return cls.build_response(permission)

    @classmethod
    def update_permission(cls, *_, **kwargs):
        """
        The update_permission function updates an Admin Role Permission.
        It takes in a dictionary as an argument, containing the following keys:
        * id
        * permission

        :param cls: Used to Call the class itself.
        :param *_: Used to Catch all the extra parameters that are passed in to the function.
        :param **kwargs: A dictionary containing the id and permission.
        :return: The updated Admin Role Permission.

        """
        permission_id = kwargs.pop("id")
        kwargs["updated_at"] = datetime.datetime.now(pytz.utc)
        permission = cls.where(id=permission_id).update(**kwargs)
        return cls.build_response(permission)

    @classmethod
    def delete_permission(cls, permission_id: str):
        """
        The delete_permission function deletes an Admin Role Permission.
        It takes in an ID as an argument.

        :param cls: Used to Call the class itself.
        :param permission_id: The ID of the permission to delete.
        :return: None

        """
        cls.where(id=permission_id).delete()
