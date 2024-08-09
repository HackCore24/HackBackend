import uuid
from datetime import datetime

from utils.base.db_model import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProjectStatuses(Base):
    __tablename__ = 'project_statuses'

    title: Mapped[str]
    order: Mapped[int]


class ProjectStatusReach(Base):
    __tablename__ = 'projects_statuses'

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    status_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("project_statuses.id"))
    date_reach: Mapped[datetime]
