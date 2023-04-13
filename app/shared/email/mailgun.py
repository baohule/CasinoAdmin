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


def send_password_email(email, password):
    response = requests.post(
        f"{Config.mailgun_host}/messages",
        auth=("api", Config.mailgun_key),
        data={
            "from": " Mailer<roreply@baohule.com>",
            "to": [{email}, ""],
            "subject": "New Password",
            "html": f"""A New Password for your account has been generated,\n
                <span style="background-color: gainsboro;"">{password}</span>
            """
        },
    )
    if response.status_code == 200:
        return True
    return
