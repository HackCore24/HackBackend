import uuid
from datetime import datetime
from typing import Optional

import phonenumbers
from fastapi import HTTPException
from pydantic import BaseModel, Field, EmailStr, field_validator

ALLOWED_COUNTRY = ['375', '7', '374', '994', '995', '380', '371', '373', '996', '993', '998']


class UserBase(BaseModel):
    firstname: str = Field(max_length=40)
    lastname: Optional[str] = Field(default=None, max_length=40)
    username: str = Field(max_length=40)
    email: Optional[EmailStr] = Field(default=None, max_length=64)
    phone: Optional[str] = Field(default=None, max_length=20)
    avatar: Optional[str] = None
    telegram: Optional[str] = None
    telegram_id: Optional[int] = None

    @field_validator("email")
    def email_to_lower(cls, v):
        if v is not None:
            return v.lower()
        return v

    @field_validator("phone")
    def check_phone(cls, v):
        if v is None:
            return v
        try:
            v = v.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            number = phonenumbers.parse(v, None)
            code = number.__dict__
            code = str(code.get('country_code'))
            len_code = len(code)
        except Exception:
            raise HTTPException(400, 'phone not valid')
        if code not in ALLOWED_COUNTRY:
            raise HTTPException(400, 'phone not valid')
        if phonenumbers.is_valid_number(number):
            number = phonenumbers.format_number(numobj=number, num_format=len_code)
            if 'tel:' in number:
                return number[len_code + 1:]
            else:
                return number
        else:
            raise HTTPException(400, 'phone not valid')


class UserCreate(UserBase):
    role: str
    password: Optional[str] = None

    @field_validator("role")
    def validate_role(cls, v):
        return v.lower()


class UserUpdate(BaseModel):
    firstname: Optional[str] = Field(default=None, max_length=40)
    lastname: Optional[str] = Field(default=None, max_length=40)
    username: Optional[str] = Field(default=None, max_length=40)
    email: Optional[EmailStr] = Field(default=None, max_length=64)
    phone: Optional[str] = Field(default=None, max_length=20)
    avatar: Optional[str] = None
    telegram: Optional[str] = None
    telegram_id: Optional[int] = None


class UserRead(UserBase):
    id: uuid.UUID
    active: bool
    created_at: datetime
    updated_at: datetime
    role: str


class TelegramAuthData(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str
    webapp_data: Optional[str] = None


class TelegramRegisterData(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: str = ""
    auth_date: int
    hash: str
    password: str
    webapp_data: Optional[str] = None
