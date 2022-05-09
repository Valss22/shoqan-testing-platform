from fastapi import APIRouter, Depends, Header, Query

from src.certificate.schemas import CertificateOut
from src.certificate.service import CertificateService

certificate_router = APIRouter(
    prefix="/certificate"
)


@certificate_router.get("/", response_model=list[CertificateOut])
async def get_all_certificates(
    all_users: bool = Query(..., alias="all"),
    Authorization: str = Header(...),
    certificate_service: CertificateService = Depends()
):
    return await certificate_service.get_all_certificates(all_users, Authorization)
