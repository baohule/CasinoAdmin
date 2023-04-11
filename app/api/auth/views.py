"""
@author: Kuro
"""
from app.api.admin.models import Admin
from app.api.agent.models import Agent
from app.api.auth.schema import UserClaim
from app.api.credit.models import Balance
from app.api.user import schema as user_schema
from app.api.user.models import User
from app.api.user.schema import AdminLogin, UserLogin, AgentLogin, AdminUserCreate
from app.shared.auth.auth_handler import sign_jwt, TokenResponse
from app.shared.auth.password_handler import get_password_hash
from typing import Union

from fastapi import APIRouter

# from app.shared.helper.logger import StandardizedLogger

# logger = StandardizedLogger(__name__)

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post("/signup", response_model=TokenResponse)
async def create_user(context: AdminUserCreate) -> TokenResponse:
    """
    > Create a user and return a JWT if successful

    :param context: AdminUserCreate - This is the request body that is passed in
    :type context: AdminUserCreate
    :return: A TokenResponse
    """
    context_data = context.dict(exclude_unset=True)
    password_authentication = get_password_hash(context.password)
    context_data["password"] = password_authentication
    user_response = User.create(**context_data)
    User.session.close()
    if not user_response:
        return TokenResponse(success=False, error="Object not created")
    Balance.create(ownerId=user_response.id, balance=0)
    Balance.session.close()
    return sign_jwt(UserClaim(id=user_response.id, email=context.email))


def jwt_login(
    context: Union[AdminLogin, UserLogin, AgentLogin], admin=False, agent=False
) -> TokenResponse:
    """
    Takes a context object, which is either an AdminLogin, UserLogin or AgentLogin,
    and returns a signed JWT if the password is correct, otherwise it returns a
    BaseResponse with an error message

    :param context: Union[AdminLogin, UserLogin, AgentLogin]
    :type context: Union[AdminLogin, UserLogin, AgentLogin]
    :param admin: Boolean, if True, the user is an admin, defaults to False (optional)
    :param agent: bool = False, defaults to False (optional)
    :return: A signed JWT token
    """
    model = admin and Admin or agent and Agent or User
    claim: UserClaim = model.user_claims(**context.dict())
    if not claim:
        return TokenResponse(success=False, error="Wrong login details")
    claim.admin = admin
    claim.agent = agent
    signed_jwt: TokenResponse = sign_jwt(claim)
    return signed_jwt


@router.post("/login/agent", response_model=TokenResponse)
async def agent_login(context: AgentLogin) -> TokenResponse:
    """
    This function logs in an agent and returns a token response using JWT authentication.

    :param context: The `context` parameter in the `agent_login` function is an instance of the `AgentLogin` class. It likely contains information about the agent trying to log in,
    such as their username and password
    :type context: AgentLogin
    :return: The function `agent_login` is returning a
    `TokenResponse` object. The `TokenResponse` object
    is the result of calling the `jwt_login` function with the
    `context` argument
    and the `agent` parameter set to `True`.
    """
    return jwt_login(context, agent=True)


@router.post("/login/admin", response_model=TokenResponse)
async def admin_login(context: AdminLogin) -> TokenResponse:
    """
    This function logs in an agent and returns a dictionary with a JWT token.

    :param context: The context parameter is an instance of the
    AgentLogin schema class, which is used to pass in the user object. This object contains information about the user who
    is attempting to log in, such as their email and password
    :type context: AgentLogin
    :return: a dictionary with a JWT token.
    """
    return jwt_login(context, admin=True)


@router.post("/login/user", response_model=TokenResponse)
async def email_login(context: UserLogin) -> TokenResponse:
    """
    Takes a user login object, and returns a token response
    :param context: UserLogin
    :return: A token response
    """
    return jwt_login(context)
