"""
@author: Kuro
"""
from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi_sqlalchemy import DBSessionMiddleware, db
from starlette.middleware.authentication import AuthenticationMiddleware

from app.shared.bases.base_model import ModelMixin, ModelType
from app.shared.middleware.request_logging import LoggingMiddleware

from settings import Config

from app.shared.middleware.auth import JWTBearer
import logging
from app.shared.redis.redis_services import RedisServices

from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a',
    force=True
)
# logger.setLevel(logging.DEBUG)

logger = logging.getLogger("backend")
logger.addHandler(logging.StreamHandler())

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "https://baohule-dashboard.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=JWTBearer())
app.add_middleware(
    DBSessionMiddleware,
    db_url=f"postgresql+psycopg2://{Config.postgres_connection}",
    engine_args={"pool_size": 100000, "max_overflow": 10000},
)
logger.debug("Middleware registered")

logger.debug("Database connection established")
with db():
    ModelMixin.set_session(db.session)


main_socket = SocketManager(app)


app.add_route("/socket.io/", route=main_socket._app, methods=['GET', 'POST'])
app.add_websocket_route("/socket.io/", main_socket._app)
