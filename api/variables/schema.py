import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class VariablesBase(BaseModel):
    title: str
    key: str
    document_id: uuid.UUID


class VariablesCreate(VariablesBase):
    pass


class VariablesRead(VariablesBase):
    id: uuid.UUID
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VariablesUpdate(BaseModel):
    title: Optional[str] = None
    key: Optional[str] = None
    document_id: Optional[uuid.UUID] = None
