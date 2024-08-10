import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class ServiceCreate(BaseModel):
    name: str
    description: str
    price: float


class ServiceRead(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True


class EstimateItemCreate(BaseModel):
    service_id: int
    quantity: int


class EstimateCreate(BaseModel):
    items: List[EstimateItemCreate]


class EstimateRead(BaseModel):
    id: int
    total_cost: float
    items: List[EstimateItemCreate]

    model_config = ConfigDict(from_attributes=True)
