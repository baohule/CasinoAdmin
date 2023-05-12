"""
@author: Kuro
"""

import contextlib
from fastapi.routing import APIRoute
from app.endpoints.urls import APIPrefix, SocketPrefix


def use_route_names_as_operation_ids(app):
    """
    It takes a FastAPI app and sets the operation_id of
    each route to be the tag, name, and method of the route

    :param app: The FastAPI application
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            method = list(route.methods)[0].lower()
            route.operation_id = f"{route.tags[0]}_{route.name}_{method}"


def add_routes(app):
    """
    It imports all the routers from the routes.include list
    and includes them in the app
    :return: The app object is being returned.
    """
    for route in APIPrefix.include:
        with contextlib.suppress(ImportError, ModuleNotFoundError):
            exec(f"from app.api.{route}.views import router as {route}")
            exec(f"app.include_router({route})")
    use_route_names_as_operation_ids(app)
    return app


def add_socket_routes(socket):

    for route in SocketPrefix.include:
        exec(f'from app.rpc.{route}.views import socket')
        return socket