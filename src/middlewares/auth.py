from typing import Optional
import jwt
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from src.settings import TOKEN_KEY


# def run_middleware(app: FastAPI):
#     @app.middleware("http")
#     async def get_current_user_id(request: Request, call_next) -> Response:
#
#         response: Response = await call_next(request)
#         auth_header: str = request.headers["authorization"]
#
#         if auth_header:
#             decoded_token: dict = jwt.decode(
#                 auth_header.split(" ")[1],
#                 TOKEN_KEY, algorithms='HS256'
#             )
#
#             print('______________')
#             print(request.receive)
#             print(request.user)
#             return response
#
#         return Response(
#             {"msg": "empty auth header"},
#             status.HTTP_400_BAD_REQUEST
#         )
#
#     return get_current_user_id

def get_current_user_id(auth_header: str) -> Optional[str]:
    if auth_header:
        decoded_token: dict = jwt.decode(
            auth_header.split(" ")[1],
            TOKEN_KEY, algorithms='HS256'
        )
        return str(decoded_token['id'])
    raise ValueError
