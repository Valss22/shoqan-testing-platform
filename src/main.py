# type: ignore
import cloudinary
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
import os
from dotenv import load_dotenv
from src.middlewares.auth import add_auth_middleware
from src.routers import api_router, api_router2

load_dotenv()
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cloudinary.config(
    cloud_name="dmh0ekjaw",
    api_key="963345615946785",
    api_secret="JqFaq0KIFuk6rx-Z8eJSK-Gfpgc",
)

register_tortoise(
    app,
    db_url=f'postgres:'
           f'//{os.getenv("USER")}:'
           f'{os.getenv("PASSWORD")}@'
           f'{os.getenv("HOST")}/'
           f'{os.getenv("DATABASE")}',
    #db_url=os.getenv("DATABASE_URL"),

    modules={"models": [
        "src.user.model",
        "src.user_profile.model",
        "src.competence.model",
        "src.discipline.model",
        "src.test.model",
    ]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(api_router)

app2 = FastAPI()

app2.include_router(api_router2)

# TODO: возможно зарефакторить мидлы
add_auth_middleware(app2)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if exc.errors()[0]["type"] == "value_error.email":
        return JSONResponse(
            {"detail": "Неправильный формат почты"},
            status.HTTP_400_BAD_REQUEST
        )
