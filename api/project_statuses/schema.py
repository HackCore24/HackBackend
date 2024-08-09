import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class StatusBase(BaseModel):
    title: str
    order: int


class StatusCreate(StatusBase):
    pass


class StatusRead(StatusBase):
    id: uuid.UUID
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StatusUpdate(BaseModel):
    title: Optional[str] = None
    order: Optional[int] = None
