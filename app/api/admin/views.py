"""
@author: Kuro
"""
from fastapi import APIRouter, Depends, Request

from app import logging
from app.api.admin.models import Admin
from app.api.admin.schema import (
    AgentUpdateResponse,
    AgentUpdate,
    ListAdminUserResponse,
    GetUserList,
    GetAgent,
    RemoveUser,
    AgentCreateResponse,
    SearchResults,
    SearchUser,
    AdminPagedResponse,
)
from app.api.agent.models import Agent
from app.api.credit.models import Quota
from app.api.user.models import User
from app.api.user.schema import (
    AdminUserCreate,
    AdminUserCreateResponse,
    AgentUserCreate,
)
from app.shared.auth.password_handler import get_password_hash
from app.shared.middleware.auth import JWTBearer
# logger = StandardizedLogger(__name__)
from app.shared.schemas.ResponseSchemas import BaseResponse

# from app.shared.helper.logger import StandardizedLogger

router = APIRouter(
    prefix="/api/admin",
    dependencies=[Depends(JWTBearer(admin=True))],
    tags=["admin"],
)
logger = logging.getLogger("admin")
logger.addHandler(logging.StreamHandler())


@router.post("/manage/create_admin", response_model=AdminUserCreateResponse)
async def create_admin(user: AdminUserCreate, request: Request):
    """
    The create_admin function creates a new admin in the database.
    It takes in a UserCreate object and returns a dictionary with either success: True or error: <error message>.
    The create_agent function requires an AdminUser role to execute.

    :param user:UserCreate: Used to Specify the type of data that is being passed to the function.
    :param request:Request: Used to Get the current user.
    :return: A dictionary with the key "success" set to true or false.


    """
    user.password = get_password_hash(user.password)
    logger.info(f"Creating admin with email {user.email}")
    if admin := Admin.add_admin(**user.dict()):
        logger.info(f"Admin created with email {user.email}")
        return AdminUserCreateResponse(success=True, response=admin)
    return AdminUserCreateResponse(error="Admin not created")


@router.post("/manage/create_agent", response_model=AgentCreateResponse)
async def create_agent(context: AgentUserCreate, request: Request):
    """
    > This function creates an agent with the given details

    :param context: AdminUserCreate - This is the context that is
    passed to the function. It is a Pydantic model that is defined
    in the models.py file
    :type context: AdminUserCreate
    :param request: Request - This is the request object that is passed to the function
    :type request: Request
    :return: AgentCreateResponse(success=True, response=agent)
    """
    logger.info(f"Creating agent with email {context.email}")
    context.password = get_password_hash(context.password)
    agent = Agent.create(
        username=context.username, email=context.email, password=context.password
    )
    if not agent:
        logger.info(f"Agent not created with email {context.email}")
        return BaseResponse(success=False, error="Admin not created")
    quota = Quota.create(agentId=agent.id, balance=context.quota)
    if not agent and quota:
        logger.info(f"Quota not created for user {context.email}")
        return BaseResponse(success=False, error="Admin not created")
    logger.info(f"Agent and quota created with email {context.email}")
    return AgentCreateResponse(success=True, response=agent)


@router.post("/manage/update_agent", response_model=AgentUpdateResponse)
async def update_agent(context: AgentUpdate, request: Request):
    """
    > Update an agent with the given data

    :param context: AgentUpdate - this is the request body that is passed in
    :type context: AgentUpdate
    :param request: Request - This is the request object that is passed to the function
    :type request: Request
    :return: AgentUpdateResponse
    """
    logger.info(f"Updating agent with id {context.agentId}")
    agent = Agent.update_agent(id=context.agentId, active=context.active)
    if context.quota:
        Quota.update(agentId=context.agentId, balance=context.quota)
    if not agent:
        logger.info(f"Agent not found with id {context.agentId}")
        BaseResponse(success=False, response="Agent not found")
    logger.info(f"Agent updated with id {context.agentId}")
    return AgentUpdateResponse(success=True, response=agent)


@router.post("/manage/remove_agent", response_model=BaseResponse)
async def remove_agent(user: RemoveUser, request: Request):
    """
    > This function removes an agent from the database

    :param user: RemoveUser - This is the parameter that will be passed to
    the function. It is a class that is defined in the
    :type user: RemoveUser
    :param request: Request - This is the request object that is passed to the function
    :type request: Request
    :return: The response is a BaseResponse object.
    """
    logger.info(f"Removing agent with id {user.id}")
    return BaseResponse(success=True, response=Agent.remove_agent(id=user.id))


@router.post("/list_agents", response_model=ListAdminUserResponse)
async def list_agents(context: GetUserList, request: Request):
    """
    > This function returns a list of agents

    :param context: GetUserList - this is the context object that is passed
    to the function. It contains the parameters that are passed in the request
    :type context: GetUserList
    :param request: Request - This is the request object that is passed to the function
    :type request: Request
    :return: ListAdminUserResponse
    """
    logger.info(
        f"Listing agents with page {context.params.page} and size {context.params.size}"
    )
    agent_pages = Agent.list_all_agents(
        context.params.page, context.params.size, active=context.context.filter.active
    )
    logger.info(f"{len(agent_pages.items)} agents found")
    return ListAdminUserResponse(
        success=True, response=AdminPagedResponse(**agent_pages.as_dict())
    )


@router.post("/get_agent", response_model=BaseResponse)
async def get_agent(user: GetAgent, request: Request):
    """
    > Get an agent by id

    :param user: GetAgent - This is the request object that will be passed to the function
    :type user: GetAgent
    :param request: Request - This is the request object that is passed to the function
    :type request: Request
    :return: BaseResponse(success=True, response=agent)
    """
    logger.info(f"Getting agent with id {user.id}")
    agent = Agent.get(id=user.id)
    if not agent:
        logger.info(f"Agent not found with id {user.id}")
        BaseResponse(success=False, response="Agent not found")
    logger.info(f"Agent found with id {user.id}")
    return BaseResponse(success=True, response=agent)


@router.post("/search", response_model=SearchResults)
async def search_users(context: SearchUser, request: Request):
    """
    The search_users function searches for users in the database.
    It accepts a list of dictionaries, each dictionary containing search parameters.
    Each dictionary is searched independently and the results are merged together.
    The keys of each dictionary should be one or more fields from the User model,
    and their values should be strings to search for.

     Phone number can be any form as long as it exists in the db.

    :param context: SearchUsers: Used to Pass the data to the function.
    :param request:Request: Used to Access the user object.
    :return: A list of users that match the search criteria.
    """
    logger.info(f"Searching for {context.type}s")
    model = User
    if context.type == "agent":
        model = Agent
    if context.type == "admin":
        model = Admin
    if context.type == "user":
        model = User
    logger.info(f"{model} selected for search")
    result = model.search(**context.dict(exclude_none=True)) or []
    logger.info(f"{len(result)} {context.type}s found")
    return SearchResults(success=True, response=result)
