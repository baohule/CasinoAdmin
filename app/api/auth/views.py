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
    model.session.close()
    if not claim:
        return TokenResponse(success=False, error="Wrong login details")
    claim.admin = admin
    claim.agent = agent
    signed_jwt: TokenResponse = sign_jwt(claim)
    return signed_jwt


@router.post("/login/agent", response_model=TokenResponse)
async def agent_login(context: AgentLogin) -> TokenResponse:
    """
    The agent_login function takes a user object and returns a JWT token.
    The function uses the Auth0 email_token method to generate an access token for the agent user.

    :param context:schema.AgentLogin: Used to Pass in the user object.
    :return: A dictionary with a jwt token.
    """
    return jwt_login(context, agent=True)


@router.post("/login/email", response_model=TokenResponse)
async def email_login(context: UserLogin) -> TokenResponse:
    """
    Takes a user login object, and returns a token response
    :param context: UserLogin
    :return: A token response
    """
    return jwt_login(context)
