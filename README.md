# CasinoAdmin Backend


CasinoAdmin is a python 3.9 FastAPI Framework application

## Installation

```bash
pip install -r requirements.txt
```
## Configuration
Rename the .env.template file to .env and modify params

```bash
POSTGRES_CONNECTION=user:password@ip:port/dbname
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8080
FASTAPI_KEY=
JWT_ALGO=HS256
MAILGUN_KEY=
MAILGUN_HOST=
SALT=abcabc
TWILIO_TOKEN=
TWILIO_SID=
TWILIO_PHONE=
REDIS_HOST=
AUTH0_CLIENT_ID=
AUTH0_CLIENT_SECRET=
AUTH0_DOMAIN=
ADMIN_KEY=
S3_IMAGE_BUCKET=
S3_VIDEO_BUCKET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
CERTFILE=
KEYFILE=
BROKER_URL=
CELERY_DATABASE=
WORKERS=1
RELOAD=True
SENTRY_INGESTION_URL=
```

## Run application

```bash
python run.py
```

## Run with docker
Assuming you have docker installed, running the application is easy!

## Run application

```bash
docker build -t CasinoAdmin:backend .
docker run -t -i -d --name CasinoAdmin -p 80:80 CasinoAdmin:backend
docker exec CasinoAdmin alembic upgrade head
```

That's it! happy hacking ^^v

## How to make a database table change
After making database model table changes run in project terminal:
1.alembic migration
2.alembic revision --autogenerate -m “First commit”
3.alembic upgrade head

