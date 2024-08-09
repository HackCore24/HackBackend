import uuid
from utils.base.db_model import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProjectDocumentations(Base):
    __tablename__ = 'project_documentation'

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('projects.id'), nullable=False)
    file_link: Mapped[str] = mapped_column(nullable=True)
    electronic_signature: Mapped[str] = mapped_column(nullable=True)
