from fastapi import APIRouter, Depends, Request

from typing import Union, Any

from fastapi import APIRouter, Depends, Request

# import app.shared.auth.auth0_handler as auth0
from app.api.admin.schema import Response
from app.api.auth import schema
from app.api.user import schema as user_schema
from app.api.user.models import User
from app.api.user.schema import UserResponse
from app.shared.auth.auth_handler import AuthController
from app.shared.auth.password_handler import get_password_hash, authenticate_user
from app.shared.bases.base_model import ModelType
from app.shared.middleware.auth import JWTBearer
# from app.shared.helper.logger import StandardizedLogger

# logger = StandardizedLogger(__name__)

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post("/signup", response_model=UserResponse)
async def create_user(
    user: user_schema.AdminUserCreate,
) -> Union[Union[dict[str, Any], Response, None, str], Any]:
    """
    The create_user function creates a new user in the database.
    It takes in a UserCreate object and returns an error if it cannot create the user.
    Otherwise, it returns the newly created user's id.

    Phone number will accept any form as long as it starts with a +1.
    Birthday has to be in format year-month-day.
    Username cannot contain special characters.

    :param user:schema.UserCreate: Used to Pass in the user object.
    :return: A dictionary with a key "error" if the creation fails.
    """
    return_data = User.create_user(**user.dict(exclude_unset=True))
    # if return_data.get('error'):
    if return_data.error:
        return return_data
    user: ModelType = return_data.get("response")
    return AuthController.sign_jwt(user.phone, skip_verification=True)


@router.post(
    "/refresh_token",
    dependencies=[Depends(JWTBearer())],
)
async def refresh_token(request: Request):
    """
    The refresh_token function is used to generate a new access token from the refresh token.
    The function takes in the request object and returns an updated access token.

    :param request:Request: Used to Get the request object from the asgi server.
    :return: A token that is signed with the refresh_token key.

    """
    bearer = JWTBearer().__call__(request)
    jwt_refresh = AuthController.sign_jwt(str(bearer), refresh=True, claim_check=True)
    if bearer == jwt_refresh:
        access_token = AuthController.sign_jwt(jwt_refresh)
        access_token.update({"success": True})
        return access_token
    return {"success": False, "error": 4}


@router.post(
    "/refresh_admin_token",
    dependencies=[Depends(JWTBearer(admin=True))],
    response_model=schema.RefreshTokenResponse,
)
def refresh_token_admin(request: Request):
    """
    The refresh_token_admin function is used to refresh the token of an admin user.
    It takes a request object as its only parameter and returns a dictionary with two keys:
    'access_token' and 'refresh_token'. The access token is for the current session, while the
    refresh token is for future sessions.

    :param request:Request: Used to Get the refresh token from the request.
    :return: A dictionary containing the following keys:.
    """
    return AuthController.sign_jwt(request.user.id, admin=True)


def jwt_login(user: Union[user_schema.AdminLogin, user_schema.UserLogin], admin: bool):
    """
    > It takes a user object and a boolean value, and returns a JWT token if the user is authenticated, otherwise it returns an error message

    :param user: User - This is the user object that you want to login
    :type user: User
    :param admin: bool - If the user is an admin or not
    :type admin: bool
    :return: A dictionary with a key of error and a value of "Wrong login details" and a key of success and a value of False.
    """
    password_authentication = authenticate_user(
        email=user.email, password=user.password, admin=admin
    )

    if not password_authentication:
        return {"error": "Wrong login details", "success": False}

    response = AuthController.sign_jwt(claim_id=password_authentication.id, admin=True)

    User.update_user(
        email=user.email, access_token=response.access_token, id_token=response.id_token
    )
    return response


@router.post("/admin_login", response_model=user_schema.UserResponse)
async def admin_login(user: user_schema.AdminLogin) -> UserResponse:
    """
    The admin_login function takes a user object and returns a JWT token.
    The function uses the Auth0 email_token method to generate an access token for the admin user.

    :param user:schema.AdminLogin: Used to Pass in the user object.
    :return: A dictionary with a jwt token.
    """
    return jwt_login(user, admin=True)


@router.post("/login/email", response_model=schema.OTPLoginResponse)
async def email_login(user: user_schema.UserLogin) -> UserResponse:
    """
    The otp_login_email function is used to log in a user with an email and password.
    It takes the user's email and password as input, authenticates them using Auth0,
    and returns the JWT token for that user.

    :param user:schema.EmailLogin: Used to Pass the email and password to the auth0.
    :return: A BaseResponse containing JWT token or error

    """
    return jwt_login(user=user, admin=False)


@router.post("/verify/recovery", response_model=schema.Response)
async def recover_verify(user: schema.Recovery) -> dict:
    """
    The recover_verify function is used to verify the user's email address.
    It takes a user object and returns a dictionary with two keys: success,
    which is True if the verification was successful, and response, which
    contains an error message if there was one.

    :param user:schema.Recovery: Used to Pass the email address of the user that is requesting a password reset.
    :return: A dictionary with the key "success" and if it is true, a response message.

    """
    response = auth0.email_token(user)
    error = response.get("error")
    if not error:
        password = get_password_hash(user.password)
        User.update_user(email=user.email, password=password)
        return {"success": True, "response": "password updated"}
    return {"success": False, "error": "user not updated"}


@router.post("/delete_self", response_model=Response)
async def delete_self(request: Request):
    """
    The delete_self function will delete the user's account.

    :param request:Request: Used to Get the user who is currently logged in.
    :return: A boolean value.

    """
    owner = request.user
    success = User.remove_user(id=owner.id)
    return {"success": success}
