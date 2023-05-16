from socketio import AsyncServer
from socketio import ASGIApp
from starlette.routing import Mount
from uvicorn import run


import logging

from app.endpoints.routes import add_socket_routes

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

socket = AsyncServer(async_mode="asgi")
app = ASGIApp(socketio_server=socket)
socket = add_socket_routes(socket)


@socket.on("connect")
async def connect(sid, environ):
    print("connect ", sid)
    await socket.emit("my_response", {"data": "Connected", "count": 0}, room=sid)
    print("envrionment: \n", environ)


@socket.on("disconnect")
async def disconnect(sid):
    print("disconnect ", sid)


#
# app.mount('/socket.io', Mount("/", app=socket.handle_request, name="socket.io"))
# app.add_websocket_route("/", socket.handle_request, name="socket.io")
