import uuid
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.routing import APIRoute
from pydantic import BaseModel


class User(BaseModel):
    username: str
    phone: str
    headImage: str
    creditAccount: dict


class AppRoutes:
    def __init__(self, app: FastAPI):
        self.app = app

    def add_post_route(self, endpoint, tag, response_data=None):
        def post_route(data: BaseModel, user_id: int = 1):
            if user_id == 1:
                return {"success": True, "response": response_data or data.dict()}
            else:
                return {"success": False, "error": "User not created"}

        self.app.post(endpoint, tags=[tag], response_model=Union[dict, User], responses={200: {"model": dict}})
        return post_route


@pytest.fixture(scope="session")
def client():
    from main import app
    return TestClient(app)


@pytest.fixture(scope="module")
def api_routes():
    app = FastAPI()
    routes = AppRoutes(app)

    create_user_data = User(
        username="test_user",
        email="test@example.com",
        headImage="https://example.com/avatar.png",
        creditAccount={"balance": 100}
    )

    routes.add_post_route("/manage/create_user", "create user", create_user_data.dict())

    return routes


def test_create_user_success(api_routes, client):
    response = client.post("/manage/create_user", json=api_routes.add_post_route("/manage/create_user"), headers={"user_id": "1"})

    assert response.status_code == 200
    assert response.json()["success"] == True


def test_create_user_no_agent(api_routes, client):
    response = client.post("/manage/create_user", json=api_routes.add_post_route("/manage/create_user"), headers={"user_id": str(uuid.uuid4())})

    assert response.status_code == 200
    assert response.json()["success"] == False
    assert response.json()["error"] == "User not created"


def test_create_user_invalid_data(api_routes, client):
    response = client.post("/manage/create_user", json={}, headers={"user_id": "1"})

    assert response.status_code == 422