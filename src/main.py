# type: ignore
import cloudinary
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
import os
from dotenv import load_dotenv

# from src.middlewares.auth import run_middleware
from src.routers import api_router

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
    # db_url=os.getenv("DATABASE_URL"),

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

# run_middleware(app)