from fastapi import APIRouter, Depends, Request
from app.api.user import schema
from app.api.user.models import User
from app.shared.middleware.auth import JWTBearer
from fastapi.exceptions import HTTPException
# from app.shared.helper.logger import StandardizedLogger

# logger = StandardizedLogger(__name__)

router = APIRouter(
    prefix="/api/user",
    dependencies=[Depends(JWTBearer())],
    tags=["user"],
)


@router.post("/get_user", response_model=schema.AdminBaseResponse)
async def post_user_data(context: schema.GetUser):
    """
    The post_user_data function is used to create a new user in the database.
    It takes a context argument, which is an instance of schema.GetUser.

    :param request:
    :param context:schema.GetUser: Used to Pass the user data to the function.
    :return: A GetUserResponse object.
    """
    return User.load_user(user_id=context.user_id)


@router.get("/get_user", response_model=schema.AdminBaseResponse)
async def get_user_data(request: Request):
    """f
    The get_user_data function returns the user data for a given user.

    :param request:Request: Used to Get the user object from the request.
    :return: A dictionary with the user's username, email and is_superuser attributes.
    """
    user = request.user
    if not user.is_authenticated:
        raise HTTPException(403, detail="Unauthenticated")
    return User.load_user(user_id=user.id)


@router.post("/set_name", response_model=schema.AdminUpdateNameResponse)
async def set_name(context: schema.AdminUpdateName, request: Request):
    """
    The set_name function updates the name of a user.
    It expects a full name ex. "Jory Lenz"

    :param context:schema.UserUpdateName: Used to Pass in the name.
    :param request:Request: Used to Get the user id.
    :return: The new name.

    """
    new_name = context.dict()
    user_id = request.user.id
    return User.update_user(user_id=user_id, **new_name)
