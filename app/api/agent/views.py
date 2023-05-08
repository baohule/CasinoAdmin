"""
@author: Kuro
"""
from app import logging
from types import SimpleNamespace

from fastapi import APIRouter, Depends, Request

from app.api.agent.models import Agent
from app.api.agent.schema import (
    CreateAgent,
    RemoveUser,
    UpdateUser,
    AgentCreateUser,
    AgentCreateUserResponse,
    UpdateUserResponse,
    GetAgentUsersResponse,
    GetAgentUsers,
    GetAgentResponse,
    GetAgent, RemoveUserResponse
)
from app.api.credit.models import Balance
from app.api.user.models import User
from app.api.user.schema import GetUserListResponse, GetAllUsers, GetUserListItems
from app.shared.auth.password_handler import get_password_hash
from app.shared.bases.base_model import paginate
from app.shared.middleware.auth import JWTBearer
from app.shared.auth.password_generator import generate_password
from app.shared.email.mailgun import send_password_email
# logger = StandardizedLogger(__name__)
from app.shared.schemas.ResponseSchemas import BaseResponse, PagedBaseResponse

# from app.shared.helper.logger import StandardizedLogger

router = APIRouter(
    prefix="/api/agent",
    dependencies=[Depends(JWTBearer(admin=True))],
    tags=["agent"]
)

logger = logging.getLogger("agent")
logger.addHandler(logging.StreamHandler())


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
    logger.info(f"Creating user with phone {context.phone}")

    def _make_user(_context, _password):
        if not (
                user_data := dict(
                    phone=context.phone,
                    password=get_password_hash(_password),
                    username=context.username.lower(),
                    headImage=context.headImage,
                )
        ):
            logger.info("Invalid user data")
            return

        if request.user.agent:
            logger.info("Updating user data with agentId")
            user_data.update(dict(agentId=request.user.id))

        _user = User.create(**user_data)
        if not _user:
            logging.info("User not created")
            return
        logger.info(f"User created with id {_user.id}")
        balance = Balance.create(
            ownerId=_user.id, balance=context.creditAccount and context.creditAccount.balance or 0
        )
        if not balance:
            return
        logger.info(f"Balance created with id {balance.id}")
        return _user

    logger.info("Generating password")
    password = generate_password()
    if user := _make_user(context, password):
        send_password_email(user.email, User.username, password)
        logger.info("Password email sent")
        return AgentCreateUserResponse(success=True, response=user)
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
    if updated_user := User.update_user(**data):
        logger.info(f"Updated user with id {updated_user.id}")
        return UpdateUserResponse(success=True, response=updated_user)
    return UpdateUserResponse(success=False, error="User not updated")


@router.post("/manage/remove_user", response_model=RemoveUserResponse)
async def remove_user(context: RemoveUser, request: Request):
    """
    `Remove the user with the given id.`
    :param context: RemoveUser - this is the context object that is passed to the function.
    It contains the id of the user to be removed
    :type context: RemoveUser
    :param request: Request - The request object that was sent to the server
    :type request: Request
    :return: The agent is being returned.
    """
    logger.info(f"Removing user with id {context.id}")
    return RemoveUserResponse(success=True, response=User.remove_user(id=context.id))


@router.post("/manage/remove_agent", response_model=BaseResponse)
def remove_agent(context: RemoveUser, request: Request) -> BaseResponse:
    """
    remove_agent = Agent.remove_agent(id=context.id)
    return BaseResponse(success=True, response=remove_agent)
    """
    logger.info(f"Removing agent with id {context.id}")
    return BaseResponse(success=True, response=Agent.remove_agent(id=context.id))


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
    if agent := Agent.read(id=context.id):
        logger.info(f"Retrieved agent with id {context.id}")
        return GetAgentResponse(success=True, response=agent)
    return GetAgentResponse(success=False, error="Agent not found")


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
    logger.info(f"Retrieving users for agent with id {context.context.filter.id}")
    agent_users = paginate(
        User.where(
            agentId=context.context.filter.id
        ),
        context.params.page,
        context.params.size
    )
    logger.info(f"Retrieved {len(agent_users.items)} users for agent with id {context.context.filter.id}")
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
    logger.info("Retrieving all users")
    paged_users: GetUserListItems = User.get_all_users(context.params.page, context.params.size)
    logger.info(f"Retrieved {len(paged_users.items)} users")
    return GetUserListResponse(success=True, response=paged_users)
