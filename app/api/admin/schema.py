from typing import Optional, List, Dict, Union
from uuid import UUID

from fastapi_camelcase import CamelModel
from pydantic import BaseModel, EmailStr

from app.shared.schemas.ResponseSchemas import BaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel
from app.shared.schemas.page_schema import GetOptionalContextPages, PagedResponse, Any


class UpdateUser(CamelModel):
    """
    It's a model that represents a user that is being updated.
    """

    id: UUID
    password: Optional[str]
    username: Optional[str]
    phone: Optional[str]
    name: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zipcode: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "id": "c1411cf2-ffcb-44dd-8202-8b00fc6dca93",
                "password": "password12",
                "username": "someusernam4",
                "phone": "+14801234567",
                "name": "some name",
                "addressLine1": "some address 123 way",
                "addressLine2": "some other address 123 wey",
                "city": "Scottsdale",
                "state": "AZ",
                "zipcode": "85251",
            }
        }


class RemoveUser(CamelModel):
    """
    It's a model that is used to remove a user from the database.
    """

    id: UUID


class User(CamelModel):
    # It's a user.
    id: UUID


class BaseUser(CamelModel):
    """
    # `BaseUser` is a base class for the `User` class.
    It is used to represent the base fields that are common
    to all users.  This is used to reduce the amount of code
    that needs to be written in the `User` class.
    """

    id: UUID
    email: Optional[str]
    username: Optional[str]
    password: Optional[str]
    name: Optional[str]
    qa_bypass: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "id": "eb773795-b3a2-4d0e-af1d-4b1c9d90ae26",
                "email": "test@test.com",
                "phone": "+14801234567",
                "name": "some name",
                "username": "newuser27",
                "qaBypass": True,
            }
            # It's a model that is used to represent a user that is being returned from the database.
        }


class BaseUserResponse(ORMCamelModel):
    """
    It's a model that is used to return a list of users.
    """

    id: UUID
    email: Optional[str]
    phone: Optional[str]
    username: Optional[str]
    name: Optional[str]


class AdminPagedResponse(ORMCamelModel):
    """
    The AdminPagedResponse class is a PagedResponse class that is
    used to return a list of users
    """





class ListAdminUserResponse(BaseResponse):
    """
    The ListUserResponse class is a PagedResponse class that is
    used to return a list of users
    """

    response: List[BaseUserResponse]

class ListUserResponse(PagedResponse):
    """
    The ListUserResponse class is a PagedResponse class that is
    used to return a list of users
    """

    items: List[BaseUserResponse]


class GetUserList(GetOptionalContextPages):
    """
    GetUserList is a model that is used to get a list of users.
    that is used in the `/list` endpoint.
    """

    __self__: GetOptionalContextPages


class BatchUsers(CamelModel):
    """
    BatchUsers is a model that is used to update multiple users at once.
    It is used in the `/batch` endpoint.
    """

    __root__: List[UpdateUser]


class AdminRoleCreate(BaseModel):
    """
    It's a model that represents the data required to create an Admin Role.
    """

    name: str
    parameters: Optional[Dict]


class AdminSetRole(BaseModel):
    """
    It's a model that represents the data required to create an Admin Role.
    """

    role_id: UUID
    owner_id: UUID
    parameters: Optional[Dict]


class SetUserRoleResponse(BaseResponse):
    """
    SetUserRoleResponse is a model that is used to return a
    response from setting a user's role.
    """

    success: bool
    error: Optional[str]


class SetPerms(CamelModel):
    """
    It's a model that is used to set a user's permissions.
    """

    id: UUID
    can_list_users: Optional[bool]
    can_get_user: Optional[bool]
    can_create_user: Optional[bool]
    can_create_admin: Optional[bool]
    can_delete_user: Optional[bool]
    can_alter_user: Optional[bool]
    can_search_users: Optional[bool]
    can_batch_alter_users: Optional[bool]
    can_set_perms: Optional[bool]
    bypass_auth: Optional[bool]


class SetPermsResponse(BaseResponse):
    """
    SetPermsResponse is a model that is used to return a
    response from setting a user's permissions.
    """

    success: bool
    error: Optional[str]


class SearchUsers(CamelModel):
    """
    `SearchUsers` is a model that is used to search for users.
    It is used in the `/search` endpoint.
    """

    users: List[BaseUser]


class SearchResults(BaseModel):
    """
    `SearchResults` is a model that is used to return a list of users that match a search query.  It is used in the `/search` endpoint.

    """

    __root__: Dict[int, List[BaseUser]]


class Response(ORMCamelModel):
    # This is a model that is used to return a response from the database.  It is used in the `/batch` endpoint.
    success: Optional[str]
    error: Optional[str]
    response: Optional[Optional[Union[str, UUID]]]


# It's a model that is used to update a user's name.


class AdminUserUpdateName(CamelModel):
    name: str


# It's a model that is used to return a response from updating a user's name.  It is used in the `/admin` endpoint.


class AdminUserUpdateNameResponse(BaseResponse):
    success: bool
    error: Optional[str]


class AdminSetPassword(CamelModel):
    id: UUID
    password: str


class AdminSetPasswordResponse(BaseResponse):
    success: bool
    error: Optional[str]



