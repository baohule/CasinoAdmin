import time
from datetime import timedelta

import jwt
from fastapi.exceptions import HTTPException

from app.shared.auth.token_handler import generate_confirmation_token, confirm_token
from app.shared.bases.base_model import ModelType, ModelMixin
from app.shared.middleware.json_encoders import ModelEncoder
from settings import Config
from fastapi.logger import logger

JWT_SECRET = Config.fastapi_key
JWT_ALGORITHM = Config.jwt_algo
ADMIN_SECRET = Config.admin_key


class AuthController(ModelMixin):
    """
    AuthController for common JWT Functions
    """

    __abstract__ = True

    @classmethod
    def token_response(cls, token: str, refresh_token: str):
        """
        The token_response function returns a dictionary containing the token and refresh_token.
        The function takes in two parameters, token and refresh_token. The function returns a dictionary
        containing the token and refresh_token.

        :param cls: Used to Set the class of the object that is being created.
        :param token:str: Used to Store the token that is returned by the oauth2 server.
        :param refresh_token:str: Used to Create a new access token.
        :return: A dictionary with the following keys:.


        """
        return {"success": True, "access_token": token, "refresh_token": refresh_token}

    @classmethod
    def sign_jwt(
        cls: ModelType,
        claim_id: str,
        admin=False,
        refresh=False,
        claim_check=False,
        skip_verification=False,
    ):
        """
        It signs a JWT token.

        :param cls: The model class that the JWT is being created for
        :type cls: ModelType
        :param claim_id: The id of the claim to be signed
        :type claim_id: str
        :param admin: If True, the JWT will be signed with the admin secret, defaults to False (optional)
        :param refresh: If True, the token will be a refresh token, defaults to False (optional)
        :param claim_check: If True, the claim_id will be checked against the database, defaults to False (optional)
        :param skip_verification: If True, the token will not be verified, defaults to False (optional)
        """

        # TODO: Cyclomatic Complexity of this method is too high.
        #  Cyclomatic Complexity is a measure of how hard the control flow of a function is to understand.
        #  Functions with high Cyclomatic Complexity will be difficult to maintain.
        #  Cyclomatic Complexity was initially formulated as a measurement of the “testability and
        #  maintainability” of the control flow of a module. While it excels at measuring the former,
        #  its underlying mathematical model is unsatisfactory at producing a value that measures the latter.
        # FIXME: obviously the only viable step is to replace this and reduce the complexity of it's operations

        def generate_refresh_token(claim):
            """
            The generate_refresh_token function generates a refresh token for the user.
            It takes in a claim dictionary and returns an encoded JWT token.
            The secret key is set to the admin_key if the user is an admin, otherwise it's set to fastapi_key.

            :param claim: Used to Check if the user is an admin or not.
            :return: A refresh token.

            """
            secret = Config.fastapi_key
            if claim.get("admin"):
                secret = Config.admin_key
            if not claim_check:
                claim["expires"] = time.time() + timedelta(hours=3).seconds
            return jwt.encode(
                claim, secret, algorithm=JWT_ALGORITHM, json_encoder=ModelEncoder
            )

        def generate_main_jwt(refresh_token):
            """
            The generate_main_jwt function generates a JWT token for the user.
            It takes in a refresh_token and returns an access_token. The access token is valid for 10 minutes.

            :param refresh_token: Used to Generate the access_token.
            :return: A jwt token that is generated from the refresh_token.


            """
            secret = Config.fastapi_key
            if claim.get("admin"):
                secret = Config.admin_key
            payload = {
                "access_token": generate_confirmation_token(refresh_token),
                "expires": time.time() + timedelta(minutes=10).seconds,
            }
            return jwt.encode(
                payload, secret, algorithm=JWT_ALGORITHM, json_encoder=ModelEncoder
            )

        def decode_refresh_token(claim):
            """
            The decode_refresh_token function takes a refresh token as an argument and returns the decoded version of it.
            It does this by decoding the jwt, confirming that it is a refresh token, and returning the access_token from within
            the decoded jwt.

            :param claim: Used to Decode the refresh token.
            :return: The refresh token.


            """
            old_claim = cls.decode_jwt(claim)
            is_refresh_token = old_claim.get("user_id")
            if not is_refresh_token:
                if decoded_claim := confirm_token(claim_id):
                    refresh_token = decoded_claim.get("access_token")
                    if refresh_token:
                        return cls.decode_jwt(claim_id)
            return old_claim

        if skip_verification:
            claim = cls.user_claims(claim_id)
            refresh_token = generate_refresh_token(claim)
            token = generate_main_jwt(refresh_token)
            return cls.token_response(token, refresh_token)

        if claim_check:
            claim_from_refresh = decode_refresh_token(claim_id)
            refresh_token = generate_refresh_token(claim_from_refresh)
            if not refresh_token:
                raise HTTPException(401, detail="Invalid JWT")
            return refresh_token

        if refresh:
            claim = cls.user_claims(claim_id)
            refresh_token = generate_refresh_token(claim)
            return refresh_token

        # TODO: add db error handling
        user_id = claim_id
        claim = cls.decode_jwt(claim_id)
        if claim:
            user_id = claim.get("user_id")
        user_claim = cls.user_claims(user_id)
        refresh_token = generate_refresh_token(user_claim)
        token = generate_main_jwt(refresh_token)

        if admin:
            token = generate_main_jwt(claim_id)

        return cls.token_response(token, refresh_token)

    @classmethod
    def decode_jwt(cls, token: str, admin=False, refresh=False) -> dict:
        """
        The decode_jwt function takes a token and checks if it is valid. If the token is valid,
        it returns the claims of that token. Otherwise, it returns None.

        :param cls: Used to Pass in the class itself.
        :param token:str: Used to Pass in the token that is being decoded.
        :param admin: Used to Determine if the token is an admin token or a user token.
        :param refresh: Used to Determine if the token is a refresh token.
        :return: The decoded token as a dictionary.
        """

        try:
            if admin:
                claims = jwt.decode(token, ADMIN_SECRET, algorithms=[JWT_ALGORITHM])
                is_valid_admin = claims.get("user_id")
                if not is_valid_admin:
                    return {}
            else:
                claims = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                return claims if claims["expires"] >= time.time() else None
        except Exception as e:
            logger.info(e)
            return {}
