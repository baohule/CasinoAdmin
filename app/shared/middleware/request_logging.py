# import asyncio
import logging
# from concurrent.futures import ThreadPoolExecutor
#
# from fastapi import Request
# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.responses import Response
#
# from app.api.history.models import ActionHistory
#
# from logging import basicConfig
#
# basicConfig(filename='app.log', level=logging.DEBUG)
# logger = logging.getLogger('app')
#
#
# class RequestLoggingMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         if request.scope["type"] not in ("http", "websocket"):
#             return await call_next(request)
#
#         response = await call_next(request)
#         await log_request(request)
#         await log_response(request, response)
#         await log_action_history(request, response)
#
#         return response
#
#
# async def stream_response(response: Response) -> bytes:
#     return b"".join([chunk async for chunk in response.body_iterator])
#
#
# async def read_request_payload(request: Request) -> str:
#     try:
#         return await request.body()
#     except Exception:
#         logger.exception("Failed to read request payload")
#         return ""
#
#
# async def read_response_payload(response: Response) -> bytes:
#     return await stream_response(response)
#
#
# async def log_request(request: Request) -> None:
#     payload = await read_request_payload(request)
#     logger.info(f"Request {request.method} {request.url.path} by {request.client.host}")
#     logger.info(f"Request {request.method} {request.url.path} Payload: {payload}")
#
#
# async def log_response(request: Request, response: Response) -> None:
#     content = await read_response_payload(response)
#     logger.info(f"Response {request.method} {request.url.path} status: {response.status_code}")
#     logger.info(f"Response {request.method} {request.url.path} Payload: {content.decode()}")
#
#
# async def log_action_history(request: Request, response: Response) -> None:
#     user = request.user
#     filters = {'adminId' if user.admin else 'agentId': user.id}
#     try:
#
#         newValueJson = await asyncio.to_thread(
#             ActionHistory.create,
#             **filters,
#             ip=request.client.host,
#             path=request.url.path,
#             newValueJson=await read_response_payload(response),
#         )
#     except Exception:
#         logger.exception(f"Failed to create action history for {request.url.path} by {request.client.host}")
#     else:
#         if not newValueJson:
#             logger.error(f"Failed to create action history for {request.url.path} by {request.client.host}")

from fastapi import Request
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message
from app.api.history.models import ActionHistory
from app.shared.middleware.auth import JWTBearer

logger = logging.getLogger("RequestLoggingMiddleware")
logger.setLevel(logging.DEBUG)


class LoggingMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):

        super().__init__(app)

    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    async def dispatch(self, request, call_next):
        await self.set_body(request)
        try:
            json_body = await request.json()
        except Exception:
            json_body = await request.body()
        actions = {'create', 'update', 'delete', 'approve', 'reject', 'cancel', 'complete', 'assign', 'unassign'}
        if any(part in actions for action in request.url.path.split('/') for part in action.split('_')):
            logger.info(f"\n{request.method} {request.url.path} \nPayload: {json_body}")
            data = dict(
                ip=request.client.host,
                path=request.url.path,
                newValueJson=json_body
            )

            try:
                request.user.id
            except Exception:
                logger.info("User not found")
                return await call_next(request)
            logger.info(f"User: {request.user.id}, AuthInfo: {request.auth}")
            if request.user.id == '44c6b702-6ea5-4872-b140-3b5e0b22ead6' or request.user.admin:
                data['adminId'] = request.user.id
            elif request.user.agent:
                data['agentId'] = request.user.id
            ActionHistory.create(**data)
        return await call_next(request)
