from fastapi.testclient import TestClient
from app import app
from app.endpoints.routes import add_routes
from app.api.user.models import User
from app.shared.auth.token_handler import generate_confirmation_token

client = TestClient(app)
add_routes()

test_new_user = {
    "email": "test@test.com",
    "password": "weakpassword",
    "phone": "4801234567",
    "first_name": "some",
    "last_name": "guy",
    "address_line1": "123 n potato lane",
    "address_line2": "apartment b",
    "city": "phoenix",
    "state": "az",
    "zipcode": 85051,
}

test_user = {"email": "test@test.com", "password": "weakpassword"}


def test_create_user():
    User.remove_user(test_new_user.get("email"))
    response = client.post("/api/auth/signup")
    assert response.status_code == 422
    response = client.post("/api/auth/signup", json=test_new_user)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("success") == True
    assert response_data.get("access_token") != None


def test_create_user_exists():
    response = client.post("/api/auth/signup", json=test_new_user)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("success") == False
    assert response_data.get("error") == "user already exists"


def test_login():
    User.update_user(email=test_user.get("email"), confirmed=True)
    response = client.post("/api/auth/login", json=test_user)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("success") == True
    assert response_data.get("access_token") != None


def test_email_confirm():
    User.update_user(email=test_user.get("email"), confirmed=False)
    token = generate_confirmation_token(test_user.get("email"))
    response = client.get(f"/api/auth/verify/{token}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("success") == True


def test_login_fail():
    response = client.post(
        "/api/auth/login", json={"email": "random@nouser.com", "password": "potato"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("success") == False


def test_recovery_token():
    response = client.post("/api/auth/recovery", json={"email": "test@test.com"})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data.get("success") == True
