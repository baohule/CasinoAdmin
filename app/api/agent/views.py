"""
@author: Kuro
"""

from fastapi import APIRouter, Depends, Request

from app.api.agent.models import Agent
from app.api.agent.schema import (
    CreateAgent,
    RemoveUser,
    UpdateUser,
    GetUserList,
    AgentCreateUser,
    AgentCreateUserResponse,
    UpdateUserResponse,
    GetAgentUsersResponse,
    GetAgentUsers,
    GetAgentResponse,
    GetAgent, GetAgentList,
)
from app.api.credit.models import Balance
from app.api.user.models import User
from app.api.user.schema import GetUserListResponse, GetAllUsers, GetUserListItems
from app.shared.auth.password_handler import get_password_hash
from app.shared.middleware.auth import JWTBearer
from app.shared.auth.password_generator import generate_password
from app.shared.email.mailgun import send_password_email
# logger = StandardizedLogger(__name__)
from app.shared.schemas.ResponseSchemas import BaseResponse, PagedBaseResponse

# from app.shared.helper.logger import StandardizedLogger

router = APIRouter(
    prefix="/api/agent", dependencies=[Depends(JWTBearer(admin=True))], tags=["agent"]
)


@router.post("/manage/create_user", response_model=AgentCreateUserResponse)
async def create_user(context: AgentCreateUser, request: Request):
    """
    > Create a user with the given data

    :param context: CreateAgent - This is the context object that is passed to the
    function. It contains the data that is passed to the function
    :type context: CreateAgent
    :param request: Request - The request object that was sent to the server
    :type request: Request
    :return: A user object
    """

    def _make_user(_context, _password):
        user_data = context.dict(
            exclude_unset=True,
            exclude_none=True
        ) and context.dict(exclude_unset=True, exclude_none=True).update(dict(password=_password))
        hashed_password = get_password_hash(password)
        user_data['password'] = hashed_password
        credit_account = user_data.pop("credit_account")
        _user_response = User.create(**user_data)
        if not _user_response:
            return
        balance = Balance.create(
            ownerId=_user_response.id, balance=credit_account.get("balance", 0)
        )
        if not balance:
            return
        return _user_response

    if not request.user:
        return BaseResponse(success=False, error="You are not logged in")
    password = generate_password()
    user_response = _make_user(context, password)
    if user_response:
        send_password_email(user_response.email, user_response.name, password)
        return AgentCreateUserResponse(success=True, response=user_response)
    return BaseResponse(success=False, error="User not created")


@router.post("/manage/update_user", response_model=UpdateUserResponse)
async def update_user(context: UpdateUser, request: Request):
    """
    The update_user function updates a user's information.
    It takes in the following parameters:
        - user: The schema object of the user to be updated.
        - request: The request object containing all data sent by client, including session cookie and form data.
        It returns a dictionary with two keys, success and response.  If successful, success is True and response
        contains no value (empty string). Otherwise, success is False and response contains an error message.

    :param :
    :param context:UpdateUser: Used to Pass in the user object.
    :param request:Request: Used to Get the user id of the current logged in user.
    :return: A dictionary with the success key set to true or false depending on whether it was.
    """
    data = context.dict(exclude_unset=True)
    updated_user = User.update_user(**data)
    return (
        UpdateUserResponse(success=True, response=context.dict(exclude_unset=True))
        if updated_user
        else BaseResponse(success=False, error="Object not updated")
    )


@router.post("/manage/remove_user", response_model=BaseResponse)
async def remove_user(context: RemoveUser, request: Request) -> BaseResponse:
    """
    `Remove the user with the given id.`
    :param context: RemoveUser - this is the context object that is passed to the function.
    It contains the id of the user to be removed
    :type context: RemoveUser
    :param request: Request - The request object that was sent to the server
    :type request: Request
    :return: The agent is being returned.
    """
    remove_agent = Agent.remove_agent(id=context.id)
    return BaseResponse(success=True, response=remove_agent)


@router.post("/get_agent", response_model=GetAgentResponse)
async def get_agent(context: GetAgent, request: Request):
    """
    This function retrieves an agent object based on the provided ID and returns it as a response.

    :param context: The context parameter is of type GetAgent, contains information about the
    request being made to retrieve an agent.
    :type context: GetAgent
    \   :param request: The `request` parameter is an instance of the `Request` class, which
    represents an HTTP request received by the server.
]|) :type request: Request
    :return: The function `get_agent` returns a `GetAgentResponse` object with a boolean `success`
    attribute set to `True` and an `Agent` object as the `response` attribute.
    """
    agent = Agent.read(id=context.id)
    return GetAgentResponse(success=True, response=agent)


@router.post("/get_agent_users", response_model=GetAgentUsersResponse)
async def get_agent_users(
        context: GetAgentUsers, request: Request
) -> GetAgentUsersResponse:
    """
    `GetAgentUsersResponse` is a response object that contains a list of `AgentUser` objects

    :param context: GetAgentUsers - This is the context object that is passed to the function. It contains the request parameters and the context object
    :type context: GetAgentUsers
    :param request: Request - This is the request object that is passed to the function
    :type request: Request
    :return: GetAgentUsersResponse
    """
    agent_users = Agent.agent_users(
        context.context.filter.id, context.params.page, context.params.size
    )
    return GetAgentUsersResponse(success=True, response=agent_users)


@router.post("/list_all_users", response_model=GetUserListResponse)
async def list_all_users(context: GetAllUsers):
    """
    This function lists all users in a paged format.

    :param context: The context parameter is an object of type GetAllUsers,
    which likely contains additional information or context needed to execute the list_all_users function. This
    could include things like authentication credentials, request headers, or other metadata
    :type context: GetAllUsers
    :return: The function `list_all_users` returns an instance of `GetUserListResponse`
    with a boolean `success` attribute set to `True` and a `response` attribute containing a paged
    list of users obtained from the `User` model's `get_all_users` method.
    """
    paged_users: GetUserListItems = User.get_all_users(context.params.page, context.params.size)
    return GetUserListResponse(success=True, response=paged_users)


