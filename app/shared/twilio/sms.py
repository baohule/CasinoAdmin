"""
@author: Kuro
"""
from settings import Config
import logging
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

client = Client(Config.twilio_sid, Config.twilio_token)


def send_sms(phone: str, body: str):
    error_details = None
    logger.info(f"Sending SMS to {phone}: {body}")
    try:
        client.messages.create(to=phone, from_=f"{Config.twilio_phone}", body=body)
        logger.info(f"message sent to {phone}")
    except TwilioRestException as e:
        if e.code in [21614, 21211]:
            errors = "Invalid phone number"
        else:
            errors = "System Error - Unable to send SMS"
            error_details = str(e)
        logger.info(errors, error_details)
        return
    except Exception as e:
        errors = "Twilio Error"
        error_details = str(e)
        logger.info(errors, error_details)
        return
    return True
