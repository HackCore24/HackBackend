from fastapi import APIRouter

from api.users.auth_router import auth_router
from api.users.users_router import users_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=['Auth'], prefix='/auth')
api_router.include_router(users_router, tags=['Users'], prefix='/users')
