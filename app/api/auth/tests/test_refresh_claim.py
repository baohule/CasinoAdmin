from fastapi.testclient import TestClient
from app import app
from app.endpoints.routes import add_routes
from app.api.auth.views import refresh_token, AuthController
from types import SimpleNamespace
from fastapi.exceptions import HTTPException

user_data = {
    "id": "eb773795-b3a2-4d0e-af1d-4b1c9d90ae26",
    "username": "jory",
    "phone": "+14062093508",
    "name": "Jory",
    "birthdate": "1978-03-22",
    "created": "2021-11-18 22:09:05.842894",
}

test_user = SimpleNamespace(**user_data)

client = TestClient(app)
add_routes()


def test_jwt_claim():
    token_response = dict()

    jwt_refresh_token = AuthController.sign_jwt(test_user.id, refresh=True)
    access_token = AuthController.sign_jwt(jwt_refresh_token["access_token"])

    token_response["access_token"] = access_token["access_token"]
    token_response["refresh_token"] = jwt_refresh_token["access_token"]

    at = token_response.get("access_token")
    rt = token_response.get("refresh_token")

    assert at is not None
    assert rt is not None
    assert at != rt

    refresh_response = client.post(
        "/api/auth/refresh_token", headers={"Authorization": f"Bearer {rt}"}
    )
    assert refresh_response.status_code == 200

    response_data = refresh_response.json()
    jwt = response_data.get("access_token")

    assert response_data != {"success": False, "error": 4}
    assert jwt is not None


def test_wrong_jwt():
    jwt_refresh_token = AuthController.sign_jwt(test_user.id, refresh=True)
    try:
        access_token = AuthController.sign_jwt(jwt_refresh_token["access_token"])
        assert access_token
    except HTTPException:
        pass
