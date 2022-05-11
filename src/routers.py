from fastapi import APIRouter

from src.certificate.controllers import certificate_router
from src.competence.controllers import competence_router
from src.test.controllers import test_router
from src.test.docx_parser.controllers import parser_router
from src.test.stress.controllers import stress_router
from src.user.controllers import user_router
from src.user_profile.controllers import user_profile_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(user_profile_router)
api_router.include_router(test_router)
api_router.include_router(stress_router)
api_router.include_router(parser_router)
api_router.include_router(certificate_router)
api_router.include_router(competence_router)


api_router2 = APIRouter()
api_router2.include_router(user_profile_router)
api_router2.include_router(test_router)
api_router2.include_router(stress_router)
api_router2.include_router(parser_router)
api_router2.include_router(certificate_router)
api_router2.include_router(competence_router)
