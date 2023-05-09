"""
@author: Kuro
"""
import uvicorn
from fastapi.logger import logger
from fastapi_socketio import SocketManager

from app.api.auth.schema import OTPLoginStart, OTPLoginStartResponse
from app.api.auth.views import start_otp_login
from settings import Config
from app.endpoints.routes import add_routes
from app import app

app = add_routes(app)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=Config.fastapi_host,
        port=Config.fastapi_port,
        ssl_keyfile="certs/local.key",
        ssl_certfile="certs/local.pem",
        workers=Config.workers,
    )
