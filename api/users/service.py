import hashlib
import hmac
import random
import string
from datetime import datetime
from urllib.parse import parse_qs

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, func, or_

from api.users.model import Users
from api.users.schema import TelegramAuthData, TelegramRegisterData
from utils.base.authentication import create_access_token, create_refresh_token
from utils.base.config import settings
from utils.base.service import BaseService
from utils.base.session import AsyncDatabase


class HashCheck:
    def __init__(self, data=None):
        if isinstance(data, str):
            pass
        elif data is None:
            pass
        else:
            self.hash = data['hash']
            self.secret_key = hashlib.sha256(settings.bot.token.encode('utf-8')).digest()
            self.data = {}
            for k, v in data.items():
                if not isinstance(v, str) and v is not None:
                    v = str(v)
                if k not in ['password', 'hash'] and v is not None:
                    self.data[k] = v

    def data_check_string(self):
        a = sorted(self.data.items())
        res = '\n'.join(map(lambda x: '='.join(x), a))
        return res

    def calc_hash(self):
        msg = bytearray(self.data_check_string(), 'utf-8')
        res = hmac.new(self.secret_key, msg=msg,
                       digestmod=hashlib.sha256).hexdigest()
        return res

    def check_hash(self):
        return self.hash == self.calc_hash()

    def transform_init_data(self, init_data):
        res = dict(parse_qs(init_data))
        for key, value in res.items():
            res[key] = value[0]
        return res

    def validate_web_app(self, data_str: str):
        data = self.transform_init_data(data_str)
        check_string = "\n".join(
            sorted(f"{key}={value}" for key, value in data.items() if key != "hash" and value is not None))
        secret = hmac.new(key=b'WebAppData', msg=settings.bot.token.encode(), digestmod=hashlib.sha256)
        signature = hmac.new(key=secret.digest(), msg=check_string.encode(), digestmod=hashlib.sha256)
        return hmac.compare_digest(data['hash'], signature.hexdigest())


class UsersService(BaseService):
    model = Users

    @classmethod
    async def password_generator(cls):
        length = random.randint(8, 12)
        characters = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    async def get(self, by: str, value: str | int):
        if by == 'email':
            query = func.lower(Users.email) == value.lower()
        elif by == 'username':
            query = func.lower(Users.username) == value.lower()
        elif by == "phone":
            query = func.lower(Users.phone) == value.lower()
        elif by == "telegram_id":
            query = Users.telegram_id == int(value)
        else:
            raise HTTPException(404, detail='by not valid, most be only email, username or phone')
        result = await self.filter(query)
        return result.first()

    async def check_user_registered_fields(self, user_data):
        username = user_data.get("username")
        email = user_data.get("email")
        phone = user_data.get("phone")

        fields_to_check = {
            Users.username: username,
            Users.email: email,
            Users.phone: phone
        }
        used_fields = []
        for field, value in fields_to_check.items():
            if value:
                query = select(Users).where(field == value)
                result = await self.session.scalars(query)
                user = result.first()
                if user:
                    field_name = field.name
                    used_fields.append(field_name)

        if used_fields:
            raise HTTPException(404, f"Fields already in use: {','.join(used_fields)}")
        else:
            return True

    async def password_check(self, user_data):
        password = user_data['password']
        if not password:
            password = await self.password_generator()
        return password, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    async def create_user(self, user_data: dict):
        await self.check_user_registered_fields(user_data=user_data)
        password, user_data['password'] = await self.password_check(user_data=user_data)
        user = Users(**user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def login(self, login: OAuth2PasswordRequestForm = Depends()):
        query = select(Users).where(func.lower(Users.username) == login.username.strip().lower())
        result = await self.session.scalars(query)
        user = result.first()

        if not user:
            query = select(Users).where(func.lower(Users.email) == login.username.strip().lower())
            result = await self.session.scalars(query)
            user = result.first()
        print(user)
        if not user:
            raise HTTPException(404, detail='user not valid')
        if user.active is False:
            raise HTTPException(404, detail='user deactivated')
        if not user.verify_password(login.password, user.password):
            raise HTTPException(404, detail='user not valid')
        to_encode = {"user_id": str(user.id),
                     "username": user.username,
                     "name": user.firstname,
                     "surname": user.lastname}

        access_token = await create_access_token(data=to_encode)
        refresh_token = await create_refresh_token(data=to_encode)

        user.refresh_token = refresh_token
        user.latest_auth = datetime.utcnow()
        await self.session.commit()

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    async def admin_login(self, login: str):
        query = select(Users).where(func.lower(Users.username) == login.strip().lower())
        result = await self.session.scalars(query)
        user = result.first()
        if not user:
            query = await self.session.scalars(select(Users).where(func.lower(Users.email) == login.strip().lower()))
            user = query.first()
        if not user:
            raise HTTPException(404, detail='user not valid')
        to_encode = {"user_id": str(user.id),
                     "username": user.username,
                     "name": user.firstname,
                     "surname": user.lastname}

        access_token = await create_access_token(data=to_encode)
        refresh_token = await create_refresh_token(data=to_encode)

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    def check_telegram_authorization(self, telegram_data: TelegramAuthData | TelegramRegisterData):
        data = telegram_data.model_dump(mode="json")
        return HashCheck(data).check_hash()

    def check_webapp_telegram_authorization(self, telegram_data):
        return HashCheck(telegram_data).validate_web_app(telegram_data)

    async def create_telegram_user(self, telegram_data: TelegramRegisterData, username):
        try:
            password = bcrypt.hashpw(telegram_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = Users(firstname=telegram_data.first_name,
                         lastname=telegram_data.last_name if telegram_data.last_name else "",
                         username=username if username else telegram_data.username,
                         telegram_id=telegram_data.id,
                         telegram=telegram_data.username,
                         password=password,
                         role="user")
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as error:
            raise HTTPException(status_code=400, detail=f'Username already exist')

    async def connect_telegram(self, telegram_data: TelegramAuthData, user):
        user = await self.get(by="email", value=user.email)
        user.telegram_id = telegram_data.id
        user.telegram = telegram_data.username
        await self.session.commit()
        return user

    async def filter_users(self, role=None, name=None, email=None, telegram_id=None):
        query = select(Users)
        if role:
            query = query.where(Users.role == role)
        if name:
            names = name.split(" ") if " " in name else name
            for name in names:
                query = query.where(or_(Users.firstname.ilike(f"%{name}%"), Users.lastname.ilike(f"%{name}%")))
        if email:
            query = query.where(Users.email.ilike(f"%{email}%"))
        if telegram_id:
            query = query.where(Users.telegram_id == telegram_id)

        return (await self.session.scalars(query)).all()


async def get_user_service(session=Depends(AsyncDatabase.get_session)):
    return UsersService(session)


user_service: UsersService = Depends(get_user_service)
