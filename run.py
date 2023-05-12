"""
@author: Kuro
"""
import uvicorn
from fastapi.logger import logger
from fastapi_socketio import SocketManager
from py_linq import Enumerable

from app.api.auth.schema import OTPLoginStart, OTPLoginStartResponse
from app.api.auth.views import start_otp_login
from settings import Config as config
from app.endpoints.routes import add_routes
from app import app

app = add_routes(app)

import asyncio
from uvicorn import Server, Config


class SocketServer(Server):
    async def run(self, sockets=None):
        self.config.setup_event_loop()
        return await self.serve(sockets=sockets)


async def run():
    app_configs = [{
        "WebAPI": Config(
            "app:app",
            host=config.fastapi_host,
            port=config.fastapi_port,
            # ssl_keyfile="certs/local.key",
            # ssl_certfile="certs/local.pem",
            workers=config.workers,
        )
    },       {
        "SocketIO": Config(
            "app.rpc:app",
            host=config.fastapi_host,
            port=config.fastapi_port + 1,
        )
    }]




    apps = [
        SocketServer(
            config=Enumerable(_config.values()).first()
        ).run() for _config in app_configs
    ]

    return await asyncio.gather(*apps)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())



if __name__ == "__main__":
    uvicorn.run(
        "app.rpc:app",
        host=config.fastapi_host,
        port=config.fastapi_port,
        # ssl_keyfile="certs/local.key",
        # ssl_certfile="certs/local.pem",
        workers=config.workers,
    )

