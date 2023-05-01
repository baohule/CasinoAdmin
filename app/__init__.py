"""
@author: Kuro
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware, db

from app.shared.bases.base_model import ModelMixin
from app.shared.middleware.request_logging import LoggingMiddleware

from settings import Config

import sentry_sdk
from celery import Celery
from app.shared.middleware.auth import JWTBearer
import app.shared.search.search as search

from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
import logging
from urllib.parse import quote_plus

#
# sentry_sdk.init(
#     Config.sentry_ingestion_url,
#     traces_sample_rate=1.0,
#     environment=Config.sentry_environment,
#     transport=print
# )


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
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=JWTBearer())
app.add_middleware(SentryAsgiMiddleware)
app.add_middleware(
    DBSessionMiddleware,
    db_url=f"postgresql+psycopg2://{Config.postgres_connection}",
    engine_args={"pool_size": 100000, "max_overflow": 10000},
)
logger.debug("Middleware registered")

logger.debug("Database connection established")
# celery = Celery("tasks", broker=Config.broker_url, backend=Config.redis_host)
# celery.conf.update({"accept_content": ["text/plain", "json"]})
# celery.conf.task_protocol = 1
# celery.autodiscover_tasks(related_name=["tasks", "task", "app"])
# celery.select_queues("posts")

# Uncomment this line if you need to NUKE the meilisearch database
# search.nuke_ms_db()
# Uncomment this line if you need to SEED the meilisearch database
# search.seed_ms_db()
