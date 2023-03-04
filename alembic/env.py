import logging
from logging.config import fileConfig
from typing import Optional, Type

from sqlalchemy import engine_from_config, MetaData
from sqlalchemy import pool
from alembic import context
import os
import sys
from dotenv import load_dotenv
from app.endpoints.urls import APIPrefix
from app.shared.bases.base_model import Base

for route in APIPrefix.include:
    try:
        exec(f'from app.api.{route}.models import ModelMixin as Base')
    except ImportError:
        logging.error(f'Route {route} has no tables defined')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)
config = context.config
url = f'postgresql+psycopg2://{os.environ["POSTGRES_CONNECTION"]}'
config.set_main_option("sqlalchemy.url", url)
fileConfig(config.config_file_name)
alembic_config = config.get_section(config.config_ini_section)
connectable = engine_from_config(
    alembic_config, prefix="sqlalchemy.", poolclass=pool.NullPool
)

target_base = Base.metadata

with connectable.connect() as connect:
    context.configure(
        connection=connect, target_metadata=target_base, include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()
