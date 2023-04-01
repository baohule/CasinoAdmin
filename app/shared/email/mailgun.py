"""
@author: Kuro
"""
import requests
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
