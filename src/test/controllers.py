from fastapi import APIRouter, UploadFile, Body, Depends
from fastapi.params import Header, File
from src.test.service import TestService

test_router = APIRouter(
    prefix='/admin/test'
)


@test_router.post('/')
async def create_test(
    info: UploadFile = Body(...),
    file: UploadFile = File(...),
    Authorization: str = Header(...),
    test_service: TestService = Depends()
):
    return await test_service.create_test(info, file, Authorization)
