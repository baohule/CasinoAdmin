from fastapi.routing import APIRoute

from app import app
from app.api.auth.views import router as auth
from app.api.admin.views import router as admin


def use_route_names_as_operation_ids(app):
    for route in app.routes:
        if isinstance(route, APIRoute):
            method = list(route.methods)[0].lower()
            route.operation_id = f"{route.tags[0]}_{route.name}_{method}"


def add_routes():
    app.include_router(auth)
    app.include_router(admin)
    use_route_names_as_operation_ids(app)
    return app
