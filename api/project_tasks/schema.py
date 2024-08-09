import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class TasksBase(BaseModel):
    project_id: uuid.UUID
    deadline: datetime
    priority: int
    responsible_user_id: uuid.UUID
    plan: str
    checkbox_tasks: dict | list
    necessary_resources: Optional[str]
    desired_result: Optional[str] = None
    comments: Optional[str] = None
    status: str


class TasksCreate(TasksBase):
    pass


class TasksRead(TasksBase):
    id: uuid.UUID
    active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TasksUpdate(BaseModel):
    project_id: Optional[uuid.UUID] = None
    deadline: Optional[datetime] = None
    priority: Optional[int] = None
    responsible_user_id: Optional[uuid.UUID] = None
    plan: Optional[str] = None
    checkbox_tasks: Optional[dict | list] = None
    necessary_resources: Optional[str] = None
    desired_result: Optional[str] = None
    comments: Optional[str] = None
    status: Optional[str] = None
