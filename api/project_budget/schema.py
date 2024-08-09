import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class BudgetBase(BaseModel):
    project_id: uuid.UUID
    budget: float
    credit_limit: float


class BudgetCreate(BudgetBase):
    pass


class BudgetRead(BudgetBase):
    id: uuid.UUID
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BudgetUpdate(BaseModel):
    project_id: Optional[uuid.UUID] = None
    budget: Optional[float] = None
    credit_limit: Optional[float] = None
