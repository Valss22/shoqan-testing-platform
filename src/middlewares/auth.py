import jwt
from fastapi import FastAPI
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from src.settings import TOKEN_KEY
from src.user.model import User


def run_auth_middleware(app: FastAPI):
    @app.middleware("http")
    async def is_auth(request: Request, call_next) -> Response:
        try:
            auth_header: str = request.headers["authorization"]
        except KeyError:
            return await call_next(request)
        try:
            jwt.decode(
                auth_header.split(" ")[1],
                TOKEN_KEY, algorithms="HS256"
            )
            return await call_next(request)
        except (InvalidTokenError or ExpiredSignatureError) as e:

            if e == InvalidTokenError:
                return JSONResponse(
                    {"msg": "token has expired"},
                    status.HTTP_400_BAD_REQUEST
                )
            return JSONResponse(
                {"msg": "invalid token"},
                status.HTTP_400_BAD_REQUEST
            )

    return is_auth


async def get_current_user(auth_header: str) -> User:
    decoded_token: dict = jwt.decode(
        auth_header.split(" ")[1],
        TOKEN_KEY, algorithms='HS256'
    )
    return await User.get(id=str(decoded_token['id']))


def get_current_user_id(auth_header: str) -> str:
    decoded_token: dict = jwt.decode(
        auth_header.split(" ")[1],
        TOKEN_KEY, algorithms='HS256'
    )
    return str(decoded_token['id'])
