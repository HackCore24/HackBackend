from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from api.users.schema import UserRead
from api.users.service import user_service
from utils.base.authentication import get_me

users_router = APIRouter()


@users_router.get('/', name='get all user', response_model=List[UserRead])
async def all_user(users=user_service, me=Depends(get_me)):
    if me.role not in ["admin"]:
        raise HTTPException(403, "forbidden")
    return await users.all()


@users_router.get('/filter', name='get users by flters', response_model=List[UserRead])
async def users_by_filter(role: Optional[str] = None,
                          name: Optional[str] = None,
                          email: Optional[str] = None,
                          users=user_service,
                          me=Depends(get_me)):
    return await users.filter_users(role, name, email)


@users_router.get('/me', name='get me')
async def current_user(user=Depends(get_me)):
    return user


@users_router.get('/{user_id}', name='get user by id', response_model=UserRead)
async def user_by_id(user_id: str, users=user_service, me=Depends(get_me)):
    return await users.id(user_id)
