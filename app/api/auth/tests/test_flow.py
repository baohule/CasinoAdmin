from unittest import TestCase
import faker
from fastapi.testclient import TestClient
from app.api.auth.schema import TokenResponse
from app import app
from app.endpoints.routes import add_routes
add_routes()


client = TestClient(app)


class TestFlow(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_toke = None
        self.password = "1121"
        self.new_valid_email = faker.Faker().email()
        self.invalid_email = "test@example"
        self.valid_user_json = {"email": self.new_valid_email, "password": self.password, "name": "test"}
        self.invalid_user_json = {"email": self.invalid_email, "password": self.password, "name": "test"}
        self.passed_email = None

    def test_create_user_valid_input(self):
        response = client.post("/api/auth/signup", json=self.valid_user_json)
        print(self.valid_user_json, response.json())
        assert response.status_code == 200
        assert TokenResponse(**response.json())
        assert TokenResponse(**response.json()).success is True
        assert TokenResponse(**response.json()).response.access_token
        self.passed_email = self.valid_user_json.copy()["email"]


    def test_create_user_invalid_input(self):
        response = client.post("/api/auth/signup", json=self.invalid_user_json)
        assert response.status_code == 422

    def test_jwt_login_valid_input(self):
        self.valid_login_json = {"email": self.passed_email, "password": self.password}
        print(self.valid_login_json)
        response = client.post("/api/auth/login/email", json=self.valid_login_json)
        assert response.status_code == 200
        assert TokenResponse(**response.json())
        assert TokenResponse(**response.json()).success is True
        assert TokenResponse(**response.json()).response.access_token


def test_jwt_login_invalid_input(mock_jwt_login):
    mock_jwt_login.return_value = TokenResponse(success=False, error="Wrong login details")
    response = client.post("/api/auth/login/email", json="invalid_jwt_login_data")
    assert response.status_code == 401
    assert response.json() == TokenResponse(success=False, error="Wrong login details")
    mock_jwt_login.assert_called_once_with("invalid_jwt_login_data")


# Mocked data for valid agent_login test
valid_agent_login_data = {
    "email": "agent@example.com",
    "password": "password",
}

# Mocked data for invalid agent_login test
invalid_agent_login_data = {
    "email": "non_existent_agent@example.com",
    "password": "password",
}


def test_agent_login_valid_input(mock_jwt_login):
    mock_jwt_login.return_value = TokenResponse(success=True)
    response = client.post("/api/auth/login/agent", json=valid_agent_login_data)
    assert response.status_code == 200
    assert response.json() == TokenResponse(success=True)
    mock_jwt_login.assert_called_once_with(valid_agent_login_data, agent=True)



def test_agent_login_invalid_input(mock_jwt_login):
    mock_jwt_login.return_value = TokenResponse(success=False, error="Wrong login details")
    response = client.post("/api/auth/login/agent", json=invalid_agent_login_data)
    assert response.status_code == 401
    assert response.json() == TokenResponse(success=False, error="Wrong login details")
    mock_jwt_login.assert_called_once_with(invalid_agent_login_data, agent=True)


# Mocked data for valid email_login test
valid_email_login_data = {
    "email": "test@example.com",
    "password": "password",
}

# Mocked data for invalid email_login test
invalid_email_login_data = {
    "email": "non_existent_user@example.com",
    "password": "password",
}



def test_email_login_valid_input(mock_jwt_login):
    mock_jwt_login.return_value = TokenResponse(success=True)
    response = client.post("/api/auth/login/email", json=valid_email_login_data)
    assert response.status_code == 200
    assert response.json() == TokenResponse(success=True)
    mock_jwt_login.assert_called_once_with(valid_email_login_data)


def test_email_login_invalid_input(mock_jwt_login):
    mock_jwt_login.return_value = TokenResponse(success=False, error="Wrong login details")
    response = client.post("/api/auth/login/email", json=invalid_email_login_data)
    assert response.status_code == 401
    assert response.json() == TokenResponse(success=False, error="Wrong login details")
    mock_jwt_login.assert_called_once_with(invalid_email_login_data)