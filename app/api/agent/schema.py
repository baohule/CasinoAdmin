"""
@author: Kuro
"""
from datetime import datetime
from typing import Optional, List, Dict, Union
from uuid import UUID

from fastapi_camelcase import CamelModel
from pydantic import BaseModel, EmailStr, Field

from app.api.user.schema import User, UserCredit
from app.shared.schemas.ResponseSchemas import BaseResponse, PagedBaseResponse
from app.shared.schemas.orm_schema import ORMCamelModel
from app.shared.schemas.page_schema import (
    GetOptionalContextPages,
    PagedResponse,
    Any,
    GetPages,
    Filter, GetNoContextPages,
)


class AgentUser(ORMCamelModel):
    """
    `Agent` is a class that is used to represent an agent.
    """

    id: Optional[UUID]
    name: Optional[str]
    email: Optional[str]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]
    creditAccount: Optional[UserCredit]


class GetAgent(CamelModel):
    """
    `GetAgent` is a class that is used to represent a request
    """

    id: UUID


class GetAgentResponse(BaseResponse):
    """
    `GetAgentResponse` is a class that is used to represent a response
    """

    response: Optional[AgentUser]


class UpdateUser(CamelModel):
    """
    It's a model that represents a user that is being updated.
    """

    id: UUID
    email: Optional[str]
    active: Optional[bool]
    credit_account: Optional[UserCredit]


class UpdateUserResponse(BaseResponse):
    """
    It's a model that represents a user that is being updated.
    """

    response: Optional[User]


class RemoveUser(CamelModel):
    """
    It's a model that is used to remove a user from the database.
    """

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
    name: Optional[str]
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
                "name": "newuser27",
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
    name: Optional[str]
    active: Optional[bool]
    credit_account: Optional[UserCredit]


class AgentPagedResponse(PagedResponse):
    """
    The AgentPagedResponse class is a PagedResponse class that is
    used to return a list of users
    """

    items: List[BaseUserResponse]


class ListAgentUserResponse(BaseResponse):
    """
    The ListUserResponse class is a PagedResponse class that is
    used to return a list of users
    """

    response: AgentPagedResponse


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


class GetAgentList(GetNoContextPages):
    """
    GetUserList is a model that is used to get a list of users.
    that is used in the `/list` endpoint.
    """

    __self__: GetNoContextPages


class BatchUsers(CamelModel):
    """
    BatchUsers is a model that is used to update multiple users at once.
    It is used in the `/batch` endpoint.
    """

    __root__: List[UpdateUser]


class AgentRoleCreate(BaseModel):
    """
    It's a model that represents the data required to create an Agent Role.
    """

    name: str
    parameters: Optional[Dict]


class AgentSetRole(BaseModel):
    """
    It's a model that represents the data required to create an Agent Role.
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


class SearchUsers(CamelModel):
    """
    `SearchUsers` is a model that is used to search for users.
    It is used in the `/search` endpoint.
    """

    users: List[BaseUser]


class Agent(BaseModel):
    """
    `Agent` is a model that is used to represent an Agent user that is being returned from the database.
    """

    id: Optional[UUID]
    email: EmailStr
    name: Optional[str]
    password: Optional[str]
    quota: Optional[float]
    active: Optional[str]
    avatar: Optional[str]
    created_by: Optional[UUID]
    created: Optional[str]


class CreateUserResponse(BaseResponse):
    """
    `CreateUserResponse` is a model that is used to return a response from the creation of a user
    """

    response: Optional[UUID]


class Balance(BaseModel):
    """
    `CreditAccount` is a model that is used to credit an account.
    """

    balance: float = Field(default=0.0)


class CreateUser(BaseModel):
    """
    `CreateUser` is a class that is used to validate the data that is being passed to the `/user` route.
    """

    email: EmailStr
    password: str
    name: str


class AgentCreateUser(BaseModel):
    """
    `CreateUser` is a class that is used to validate the data that is being passed to the `/user` route.
    """

    email: EmailStr
    name: Optional[str]
    headImage: Optional[str]
    credit_account: Optional[Balance] = Field(title="CreditAccount")


class CreateAgent(CamelModel):
    """
    `UserCreate` is a class that is used to validate the data that is being passed to the `/user` route.
    """

    email: EmailStr
    password: str
    name: str


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


class AgentUserUpdateName(CamelModel):
    name: str


class AgentUserUpdateNameResponse(BaseResponse):
    success: bool
    error: Optional[str]


class AgentSetPassword(CamelModel):
    id: UUID
    password: str


class AgentSetPasswordResponse(BaseResponse):
    success: bool
    error: Optional[str]


class AgentCreateUserResponse(BaseResponse):
    """
    `AgentCreateResponse` is a model that is used to return a response from the `/user` route.
    """

    response: Optional[User]


class AgentCreateResponse(BaseResponse):
    """
    `AgentCreateResponse` is a model that is used to return a response from the `/user` route.
    """

    response: Optional[Agent]


class GetAgentUsersItems(PagedResponse):
    items: List[BaseUserResponse]



class GetAgentUsersResponse(PagedBaseResponse):
    response: GetAgentUsersItems


class AgentContext(BaseModel):
    id: Optional[UUID]


class GetAgentPagedContext(Filter):
    filter: Optional[AgentContext]


class GetAgentUsers(GetPages):
    context: GetAgentPagedContext
