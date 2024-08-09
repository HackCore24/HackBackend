import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import JSON

from utils.base.db_model import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProjectTasks(Base):
    __tablename__ = 'project_tasks'

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('projects.id'), nullable=False)
    deadline: Mapped[datetime]
    priority: Mapped[int]
    responsible_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    plan: Mapped[str]
    checkbox_tasks: Mapped[dict | list] = mapped_column(type_=JSON, nullable=False)
    necessary_resources: Mapped[str] = mapped_column(nullable=True)
    desired_result: Mapped[str] = mapped_column(nullable=True)
    comments: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default='in progress')
