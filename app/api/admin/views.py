"""
@author: Kuro
"""
from fastapi import APIRouter, Depends, Request

from app.api.admin.schema import (
    AgentUpdateResponse,
    AgentUpdate,
    ListAdminUserResponse,
    GetUserList,
    GetAgent,
    RemoveUser,
    AgentCreateResponse, SearchResults, SearchUser,
)
from app.api.agent.models import Agent
from app.api.user.models import User
from app.shared.auth.password_handler import get_password_hash
from app.shared.middleware.auth import JWTBearer
from app.api.user.schema import AdminUserCreate, AdminUserCreateResponse
from app.api.admin.models import Admin
from fastapi.exceptions import HTTPException

# from app.shared.helper.logger import StandardizedLogger

# logger = StandardizedLogger(__name__)
from app.shared.schemas.ResponseSchemas import BaseResponse
from app.shared.schemas.page_schema import PagedResponse

router = APIRouter(
    prefix="/api/admin",
    dependencies=[Depends(JWTBearer(admin=True))],
    tags=["admin"],
)


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
    user.password = get_password_hash(user.name + user.password)
    admin = Admin.add_admin(**user.dict())
    return (
        AdminUserCreateResponse(success=True, response=admin)
        if admin
        else BaseResponse(success=False, response="Admin not found")
    )


@router.post("/manage/create_agent", response_model=AgentCreateResponse)
async def create_agent(context: AdminUserCreate, request: Request):
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

    context.password = get_password_hash(context.name + context.password)
    agent = Agent.add_agent(**context.dict())
    return (
        AgentCreateResponse(success=True, response=agent)
        if agent
        else BaseResponse(success=False, response="Agent not found")
    )


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
    data = context.dict(exclude_unset=True)
    agent = Agent.update_agent(**data)
    if not agent:
        BaseResponse(success=False, response="Agent not found")
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
    agent_pages = Agent.list_all_agents(context.params.page, context.params.size)

    return ListAdminUserResponse(success=True, response=agent_pages)


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
    agent = Agent.get(id=user.id)
    if not agent:
        BaseResponse(success=False, response="Agent not found")
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

    :param query:schema.SearchUsers: Used to Pass the data to the function.
    :param request:Request: Used to Access the user object.
    :return: A list of users that match the search criteria.
    """
    model = User
    if context.type == 'agent':
        model = Agent
    if context.type == 'admin':
        model = Admin
    if context.type == 'user':
        model = User
    result = model.search(**context.dict(exclude_none=True))
    return SearchResults(success=True, response=result)

