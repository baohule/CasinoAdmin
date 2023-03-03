from app.shared.bases.base_test import mock_post, test_user
from fastapi_sqlalchemy import db


def test_set_name():
    url = "/api/user/set_name"
    data = {"name": "Kody Mitchell"}
    response = mock_post(url, data)
    assert not response.json().get("error")


def test_load_user():
    url = "/api/user/get_user"
    data = {"user_id": "eb773795-b3a2-4d0e-af1d-4b1c9d90ae26"}
    response = mock_post(url, data)
    assert response.status_code == 200
