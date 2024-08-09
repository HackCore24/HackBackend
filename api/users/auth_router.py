from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from api.users.schema import UserCreate, UserRead, TelegramAuthData, TelegramRegisterData
from api.users.service import user_service
from utils.base.authentication import get_me

auth_router = APIRouter()


@auth_router.post('/register', name='register user', response_model=UserRead, status_code=201)
async def create_user(user: UserCreate, users=user_service):
    return await users.create_user(user.__dict__)


@auth_router.post('/login', name='login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), users=user_service):
    access_info = await users.login(form_data)
    response = JSONResponse(content=access_info)
    response.set_cookie(key="refresh_token", value=access_info.get('refresh_token'), secure=True, samesite="none")
    response.set_cookie(key="access_token", value=access_info.get('access_token'), secure=True, samesite="none")
    response.headers["Authorization"] = f"Bearer {access_info.get('access_token')}"
    return response


@auth_router.post("/telegram")
async def auth_telegram(telegram_data: TelegramAuthData, users=user_service):
    verified = users.check_telegram_authorization(telegram_data)
    print(verified)
    if not verified:
        raise HTTPException(status_code=401, detail="Invalid authentication data")
    user = await users.get(by="telegram_id", value=telegram_data.id)
    if not user:
        raise HTTPException(404, 'not found')
    return await users.admin_login(user.username)


@auth_router.post("/telegram/register", name='register user by telegram', status_code=201)
async def auth_telegram(telegram_data: TelegramRegisterData, username: Optional[str] = None, users=user_service):
    if telegram_data.webapp_data:
        verified = users.check_webapp_telegram_authorization(telegram_data.webapp_data)
    else:
        verified = users.check_telegram_authorization(telegram_data)
    if not verified:
        raise HTTPException(status_code=401, detail="Invalid authentication data")
    user = await users.create_telegram_user(telegram_data=telegram_data, username=username)
    if not user:
        raise HTTPException(404, 'not found')
    return await users.admin_login(user.username)


@auth_router.post("/telegram/connect", name='connect telegram account', response_model=UserRead)
async def auth_telegram(telegram_data: TelegramAuthData, users=user_service, me=Depends(get_me)):
    if telegram_data.webapp_data:
        verified = users.check_webapp_telegram_authorization(telegram_data.webapp_data)
    else:
        verified = users.check_telegram_authorization(telegram_data)
    if not verified:
        raise HTTPException(status_code=401, detail="Invalid authentication data")
    user = await users.connect_telegram(telegram_data=telegram_data, user=me)
    return user
