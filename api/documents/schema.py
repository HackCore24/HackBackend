import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class DocumentsBase(BaseModel):
    title: str
    filename: str
    html: str


class DocumentsCreate(DocumentsBase):
    pass


class DocumentsRead(DocumentsBase):
    id: uuid.UUID
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentsUpdate(BaseModel):
    title: Optional[str] = None
    filename: Optional[str] = None
    html: Optional[str] = None
