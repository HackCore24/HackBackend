import uuid
from utils.base.db_model import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Projects(Base):
    __tablename__ = 'projects'

    title: Mapped[str]
    company_name: Mapped[str]
    caver: Mapped[str] = mapped_column(nullable=True)

    creator_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=True)


class RelatedProject(Base):
    __tablename__ = 'related_projects'

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('projects.id'), nullable=False)
    related_project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('projects.id'), nullable=False)
