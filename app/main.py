# type: ignore
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
import os
from dotenv import load_dotenv
from app.routers import api_router

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

register_tortoise(
    app,
    db_url=f'postgres:'
           f'//{os.getenv("USER")}:'
           f'{os.getenv("PASSWORD")}@'
           f'{os.getenv("HOST")}/'
           f'{os.getenv("DATABASE")}',
    modules={"models": ["app.user.model"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(api_router)

