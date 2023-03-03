import sys, os

sys.path.insert(1, os.path.join(sys.path[0], "..\\..\\..\\.."))

from app.api.user.models import User
from app import app
from fastapi_sqlalchemy import db
from fastapi.testclient import TestClient
from app.endpoints.routes import add_routes

client = TestClient(app)
add_routes()


def test_overwrite_default_user():
    with db():
        default_user = db.session.query(User).filter_by(username="haxuser")
        default_user.update({"id": "eb773795-b3a2-4d0e-af1d-4b1c9d90ae26"})
        db.session.commit()


test_overwrite_default_user()
