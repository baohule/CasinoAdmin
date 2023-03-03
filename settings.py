import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    postgres_connection: str = os.getenv("POSTGRES_CONNECTION", "")
    fastapi_host: str = os.getenv("FASTAPI_HOST", "127.0.0.1")
    fastapi_port: int = int(os.getenv("FASTAPI_PORT", 8000))
    fastapi_key: str = os.getenv("FASTAPI_KEY", "")
    salt: str = os.getenv("SALT", "")
    jwt_algo: str = os.getenv("JWT_ALGO")
    admin_key: str = os.getenv("ADMIN_KEY")
    mailgun_key: str = os.getenv("MAILGUN_KEY", "")
    mailgun_host: str = os.getenv("MAILGUN_HOST", "")
    twilio_sid: str = os.getenv("TWILIO_SID", "")
    twilio_token: str = os.getenv("TWILIO_TOKEN", "")
    twilio_phone: str = os.getenv("TWILIO_PHONE", "")
    redis_host: str = os.getenv("REDIS_HOST", "")
    auth0_client_id: str = os.getenv("AUTH0_CLIENT_ID", "")
    auth0_client_secret: str = os.getenv("AUTH0_CLIENT_SECRET", "")
    auth0_domain: str = os.getenv("AUTH0_DOMAIN", "")
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_image_bucket: str = os.getenv("S3_IMAGE_BUCKET")
    s3_video_bucket: str = os.getenv("S3_VIDEO_BUCKET")
    broker_url: str = os.getenv("BROKER_URL", "")
    celery_database: str = os.getenv("CELERY_DATABASE", "")
    workers: int = int(os.getenv("WORKERS", 15))
    reload: bool = os.getenv("RELOAD", False)
    sentry_ingestion_url: str = os.getenv("SENTRY_INGESTION_URL", "")
    sentry_environment: str = os.getenv("SENTRY_ENVIRONMENT", "local")
    meilisearch_url: str = os.getenv("MEILISEARCH_URL", "")
    meili_admin_key: str = os.getenv("MEILI_ADMIN_KEY", "")
    meili_query_key: str = os.getenv("MEILI_QUERY_KEY", "")

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "app": {"handlers": ["default"], "level": "DEBUG"},
        },
    }
