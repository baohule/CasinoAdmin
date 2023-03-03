from fastapi.testclient import TestClient
from app import app
from app.endpoints.routes import add_routes
from app.shared.email.mailgun import send_verification_email, send_recovery_email
from app.shared.auth.token_handler import generate_confirmation_token
from app.shared.twilio.sms import send_sms

client = TestClient(app)
add_routes()


test_user = {
    "email": "michael.brown@insidersapp.io",
    "password": "$2b$12$rz1X7jLiWDtleSGTdWebz.Vfr7PBRwszvqgNskoB8hWm4rEGOzI/a",
    "confirmed": False,
    "phone": "4805727268",
    "first_name": "some",
    "last_name": "guy",
    "address_line1": "123 n potato lane",
    "address_line2": "apartment b",
    "city": "phoenix",
    "state": "az",
    "zipcode": 85051,
}


def test_verification_email():
    email = test_user.get("email")
    token = generate_confirmation_token(email)
    response = send_verification_email(email, token)
    response_data = response.json()
    assert response_data.get("message") == "Queued. Thank you."


def test_recovery_email():
    email = test_user.get("email")
    token = generate_confirmation_token(email)
    response = send_recovery_email(email, token)
    response_data = response.json()
    assert response_data.get("message") == "Queued. Thank you."


def test_sms():
    phone = test_user.get("phone")
    response = send_sms(phone, "test")
    assert response == True
