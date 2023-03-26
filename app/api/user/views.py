from fastapi import APIRouter, Depends, Request
from app.api.user import schema
from app.api.user.models import User
from app.api.user.schema import GetUserListResponse, LoadUserResponse, GetUserListItems, GetAllUsers
from app.shared.middleware.auth import JWTBearer
from fastapi.exceptions import HTTPException

from app.shared.schemas.page_schema import PagedResponse

router = APIRouter(
    prefix="/api/user",
    dependencies=[Depends(JWTBearer())],
    tags=["user"],
)


@router.post("/get_user", response_model=LoadUserResponse)
async def post_user_data(context: schema.GetUser, request: Request):
    """
    The post_user_data function is used to create a new user in the database.
    It takes a context argument, which is an instance of schema.GetUser.

    :param request:
    :param context:schema.GetUser: Used to Pass the user data to the function.
    :return: A GetUserResponse object.
    """
    user = User.get(id=context.id)
    return LoadUserResponse(success=True, response=user)


@router.get("/get_user", response_model=LoadUserResponse)
async def get_user_data(request: Request):
    """f
    The get_user_data function returns the user data for a given user.

    :param request:Request: Used to Get the user object from the request.
    :return: A dictionary with the user's username, email and is_superuser attributes.
    """
    user = request.user


@router.post("/list_all_users", response_model=GetUserListResponse)
async def list_all_users(context: GetAllUsers):
    """
    The list_all_users function returns a list of all users.
    :return: A list of all users.
    """
    paged_users = User.get_all_users(context.params.page, context.params.size)
    return GetUserListResponse(success=True, response=paged_users)
