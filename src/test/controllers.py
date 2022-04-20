from fastapi import APIRouter, UploadFile, Body, Depends
from fastapi.params import File
from src.test.service import TestService

test_router = APIRouter(
    prefix='/admin/test'
)


@test_router.post('/')
async def create_test(
    info: UploadFile = Body(...),
    file: UploadFile = File(...),
    test_service: TestService = Depends()
):
    return await test_service.create_test(info, file)
