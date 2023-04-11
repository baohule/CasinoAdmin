"""
@author: Kuro
"""
from datetime import datetime
from typing import Optional, List, Dict, Union
from uuid import UUID

from fastapi_camelcase import CamelModel
from pydantic import BaseModel, EmailStr, Field

from app.api.agent.schema import AgentUser
from app.api.credit.schema import UserCredit
from app.shared.schemas.ResponseSchemas import BaseResponse, PagedBaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel
from app.shared.schemas.page_schema import GetOptionalContextPages, PagedResponse, Any


class UpdateUser(CamelModel):
    """
    It's a model that represents a user that is being updated.
    """

    id: UUID
    password: Optional[str]
    username: Optional[str]


class RemoveUser(CamelModel):
    """
    It's a model that is used to remove a user from the database.
    """

    id: UUID


class GetAgent(CamelModel):
    # It's a user.
    id: UUID


class BaseUser(ORMCamelModel):
    """
    # `BaseUser` is a base class for the `User` class.
    It is used to represent the base fields that are common
    to all users.  This is used to reduce the amount of code
    that needs to be written in the `User` class.
    """

    id: UUID
    email: Optional[str]
    password: Optional[str]
    creditAccount: Optional[UserCredit]


class Admin(ORMCamelModel):
    id: UUID
    email: Optional[str]
    name: Optional[str]


class BaseUserResponse(ORMCamelModel):
    """
    It's a model that is used to return a list of users.
    """

    id: UUID
    email: Optional[str]
    username: Optional[str]
    name: Optional[str]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    quota: Optional[int]
    creditAccount: Optional[UserCredit]
    active: Optional[bool]
    createdByAdmin: Optional[AgentUser]
    createdByAgent: Optional[Admin]



class AdminPagedResponse(PagedResponse):
    """
    The AdminPagedResponse class is a PagedResponse class that is
    used to return a list of users
    """

    items: List[BaseUserResponse]


class ListAdminUserResponse(PagedBaseResponse):
    """
    The ListUserResponse class is a PagedResponse class that is
    used to return a list of users
    """

    response: AdminPagedResponse


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

    username: str
    parameters: Optional[Dict]


class AdminSetRole(BaseModel):
    """
    It's a model that represents the data required to create an Admin Role.
    """

    role_id: UUID
    ownerId: UUID
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


class SearchUser(CamelModel):
    """
    `SearchUser` is a model that is used to search for users.
    It is used in the `/search` endpoint.
    """

    email: Optional[str]
    name: Optional[str]
    type: str = Field(..., example="agent | admin | user")




class SearchResults(BaseResponse):
    """
    `SearchResults` is a model that is used to return a list of users
    that match a search query.  It is used in the `/search` endpoint.

    """
    response: Optional[List[BaseUserResponse]]





class AgentCreateResponse(BaseResponse):
    # This is a model that is used to return a response from the database.  It is used in the `/batch` endpoint.
    success: bool
    error: Optional[str]
    response: Optional[AgentUser]


class AgentUpdate(CamelModel):
    id: UUID
    quota: Optional[int]
    active: Optional[bool]


class AgentUpdateResponse(BaseResponse):
    # This is a model that is used to return a response from the database.  It is used in the `/batch` endpoint.
    success: bool
    error: Optional[str]
    response: Optional[AgentUser]


class AdminUserUpdateName(CamelModel):
    username: str


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
