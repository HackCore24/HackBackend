import uuid
from utils.base.db_model import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Variables(Base):
    __tablename__ = 'variables'

    title: Mapped[str]
    key: Mapped[str]
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("documents.id"))
