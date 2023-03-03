import uvicorn
from settings import Config
from app.endpoints.routes import add_routes
from logging.config import dictConfig
from fastapi.logger import logger

dictConfig(Config.log_config)
app = add_routes()

logger.info(f"Starting application with {Config.workers} workers")

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=Config.fastapi_host,
        port=Config.fastapi_port,
        # ssl_keyfile="certs/local.key",
        # ssl_certfile="certs/local.pem",
        workers=Config.workers,
    )
