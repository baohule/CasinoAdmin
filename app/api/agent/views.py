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
from app.shared.middleware.auth import JWTBearer

# logger = StandardizedLogger(__name__)
from app.shared.schemas.ResponseSchemas import BaseResponse, PagedBaseResponse

# from app.shared.helper.logger import StandardizedLogger

router = APIRouter(
    prefix="/api/agent", dependencies=[Depends(JWTBearer(admin=True))], tags=["agent"]
)

def make_user(context):
    user_data = context.dict(exclude_unset=True)
    user_response = User.create(**user_data)
    Balance.create(
        ownerId=user_response.id, balance=context.creditAccount.balance
    )
    return user_response

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
    agent = Agent.read(id=request.user.id)
    if not agent:
        return AgentCreateUserResponse(success=True, response=make_user(context))
    agent_users = len(agent.users)
    if agent_users >= agent.quota:
        return BaseResponse(success=False, error="You have reached your quota")
    return AgentCreateUserResponse(success=True, response=make_user(context))


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
        UpdateUserResponse(success=True, response=updated_user)
        if updated_user
        else BaseResponse(success=False, error="Object not updated")
    )


@router.post("/manage/remove_user", response_model=BaseResponse)
async def remove_user(context: RemoveUser, request: Request) -> BaseResponse:
    """
    `Remove the user with the given id.`

    :param context: RemoveUser - this is the context object that is passed to the function. It contains the id of the user to be removed
    :type context: RemoveUser
    :param request: Request - The request object that was sent to the server
    :type request: Request
    :return: The agent is being returned.
    """
    remove_agent = Agent.remove_agent(id=context.id)
    return BaseResponse(success=True, response=remove_agent)


@router.post("/list_agents", response_model=PagedBaseResponse)
async def list_agents(context: GetAgentList, request: Request) -> PagedBaseResponse:
    """
    The list_all_agents function returns a list of all agents in the system.

    This function requires admin privileges to run.

    :param context:schema.GetUserList: Used to Pass in the request object.
    :param request:Request: Used to Pass in the current request.
    :return: A list of users.
    """
    paged_response = Agent.list_all_agents(context.params.page, context.params.size)
    return PagedBaseResponse(success=True, response=paged_response)


@router.post("/get_agent", response_model=GetAgentResponse)
async def get_agent(context: GetAgent, request: Request):
    """
    This function retrieves an agent object based on the provided ID and returns it as a response.

    :param context: The context parameter is of type GetAgent, contains information about the request being made to retrieve an agent.
    :type context: GetAgent
    \   :param request: The `request` parameter is an instance of the `Request` class, which represents an HTTP request received by the server.
]|) :type request: Request
    :return: The function `get_agent` returns a `GetAgentResponse` object with a boolean `success` attribute set to `True` and an `Agent` object as the `response` attribute.
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
