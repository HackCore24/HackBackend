import uuid
from utils.base.db_model import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Documents(Base):
    __tablename__ = 'documents'

    title: Mapped[str]
    filename: Mapped[str]
    html: Mapped[str]


class DocumentsProjects(Base):
    __tablename__ = 'documents_projects'

    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id"))
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
