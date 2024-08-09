import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class DocumentationBase(BaseModel):
    project_id: uuid.UUID
    file_link: Optional[str] = None
    electronic_signature: Optional[str] = None


class DocumentationCreate(DocumentationBase):
    pass


class DocumentationRead(DocumentationBase):
    id: uuid.UUID
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentationUpdate(BaseModel):
    project_id: Optional[uuid.UUID] = None
    file_link: Optional[str] = None
    electronic_signature: Optional[str] = None
