from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

from app.type_tables.asset_type.models import Base
from app.type_tables.property_type.models import Base
from app.type_tables.round_type.models import Base
from app.type_tables.topic_type.models import Base
from app.api.user.models import Base
from app.api.post.models import Base
from app.api.review.models import Base
from app.api.files.models import Base
from app.api.like.models import Base
from app.api.strategy.models import Base
from app.api.follow.models import Base
from app.api.update.models import Base
from app.api.reaction.models import Base
from app.api.portfolio.models import Base
from app.api.question.models import Base
from app.api.comment.models import Base
from app.api.investment.models import Base
from app.api.interest.models import Base
from app.api.profile.models import Base
from app.api.admin.models import Base
from app.api.history.models import Base
from app.api.allocation.models import Base
from app.api.topic.models import Base


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
