"""
@author: Kuro
"""
import uvicorn
from settings import Config
from app.endpoints.routes import add_routes

app = add_routes()

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=Config.fastapi_host,
        port=Config.fastapi_port,
        # ssl_keyfile="certs/local.key",
        # ssl_certfile="certs/local.pem",
        workers=Config.workers,
    )
