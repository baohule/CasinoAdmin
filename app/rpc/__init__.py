# logger.setLevel(logging.DEBUG)
from fastapi import FastAPI
from socketio import AsyncServer
from socketio import ASGIApp

from run import app
from app import logging

logger = logging.getLogger("backend")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class CustomASGIApp:
    def __init__(
            self,

            other_asgi_app: FastAPI = None,
            async_mode: str = "asgi",
            cors_allowed_origins: str = "*",
            mount_location: str = "/ws",
            socketio_path: str = "socket.io",
            **kwargs
    ):
        self._sio = AsyncServer(async_mode=async_mode, cors_allowed_origins=cors_allowed_origins, **{k: v for k, v in kwargs.items() if v})
        self._app = ASGIApp(
            socketio_path=socketio_path,
            other_asgi_app=other_asgi_app,
            socketio_server=self._sio,
            **kwargs
        )

        app.mount(mount_location, self._app)
        app.ssid = self._sio
        self.app = self._app
        self.socket_server = self._sio

    @property
    def on(self):
        return self._sio.on

    @property
    def attach(self):
        return self._sio.attach

    @property
    def emit(self):
        return self._sio.emit

    @property
    def send(self):
        return self._sio.send

    @property
    def call(self):
        return self._sio.call

    @property
    def close_room(self):
        return self._sio.close_room

    @property
    def get_session(self):
        return self._sio.get_session

    @property
    def save_session(self):
        return self._sio.save_session

    @property
    def session(self):
        return self._sio.session

    @property
    def disconnect(self):
        return self._sio.disconnect

    @property
    def handle_request(self):
        return self._sio.handle_request

    @property
    def start_background_task(self):
        return self._sio.start_background_task

    @property
    def sleep(self):
        return self._sio.sleep

    @property
    def enter_room(self):
        return self._sio.enter_room

    @property
    def leave_room(self):
        return self._sio.leave_room


socket_app = CustomASGIApp(other_asgi_app=app)
app.add_route("/socket.io/", route=socket_app._app, methods=['GET', 'POST'])
app.add_websocket_route("/socket.io/", socket_app._app, name="socket.io")
# socket = socket_app
