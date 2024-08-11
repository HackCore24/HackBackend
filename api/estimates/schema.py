import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    position_number: str
    title: str
    quantity: int
    unit_work_price: int
    unit_operation_price: int
    unit_material_price: int
    work_price: Optional[int] = None
    operation_price: Optional[int] = None
    material_price: Optional[int] = None
    total_price: Optional[int] = None

    chapter_id: uuid.UUID


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    position_number: Optional[str] = None
    title: Optional[str] = None
    quantity: Optional[int] = None
    unit_work_price: Optional[int] = None
    unit_operation_price: Optional[int] = None
    unit_material_price: Optional[int] = None
    work_price: Optional[int] = None
    operation_price: Optional[int] = None
    material_price: Optional[int] = None
    total_price: Optional[int] = None

    chapter_id: Optional[uuid.UUID] = None


class ServiceRead(ServiceBase):
    id: uuid.UUID
    active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ChapterBase(BaseModel):
    title: str
    total_price: Optional[int] = None
    total_work_price: Optional[int] = None
    total_operation_price: Optional[int] = None
    total_material_price: Optional[int] = None

    project_id: uuid.UUID

class ChapterCreate(ChapterBase):
    pass


class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    total_price: Optional[int] = None
    total_work_price: Optional[int] = None
    total_operation_price: Optional[int] = None
    total_material_price: Optional[int] = None


class ChapterRead(ChapterBase):
    id: uuid.UUID
    active: bool
    created_at: datetime
    updated_at: datetime

    services: Optional[List[ServiceRead]] = None

    model_config = ConfigDict(from_attributes=True)
