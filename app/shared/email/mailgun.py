"""
@author: Kuro
"""
import requests

from app.shared.email.templates.new_password import get_template
from settings import Config


def send_verification_email(email, token):
    return requests.post(
        Config.mailgun_host,
        auth=("api", Config.mailgun_key),
        data={
            "from": " Mailer<roreply@>",
            "to": [{email}, ""],
            "subject": "Verify Email",
            "html": f"Please click the following link to verify your email: "
            f"<a href='{token}'>{token}</a>",
        },
    )


def send_recovery_email(email, token):
    return requests.post(
        Config.mailgun_host,
        auth=("api", Config.mailgun_key),
        data={
            "from": " Mailer<roreply@>",
            "to": [{email}, ""],
            "subject": "Recover Account",
            "html": f"Please supply the following token to the app: "
            f"<a href='{token}'>{token}</a>",
        },
    )


def send_password_email(email: str, name: str, password: str):
    response = requests.post(
        f"{Config.mailgun_host}/messages",
        auth=("api", Config.mailgun_key),
        data={
            "from": " Baohule<roreply@baohule.com>",
            "to": [{email}, ""],
            "subject": "New Password",
            "html": get_template(name, password),
        },
    )
    if response.status_code == 200:
        return True
    return
