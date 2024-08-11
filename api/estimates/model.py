import uuid
from utils.base.db_model import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Service(Base):
    __tablename__ = 'estimates'

    position_number: Mapped[str]
    title: Mapped[str]
    quantity: Mapped[int]
    unit_work_price: Mapped[int]
    unit_operation_price: Mapped[int]
    unit_material_price: Mapped[int]
    work_price: Mapped[int] = mapped_column(nullable=True)
    operation_price: Mapped[int] = mapped_column(nullable=True)
    material_price: Mapped[int] = mapped_column(nullable=True)
    total_price: Mapped[int] = mapped_column(nullable=True)

    chapter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chapters.id"))


class Chapters(Base):
    __tablename__ = 'chapters'

    title: Mapped[str]
    total_price: Mapped[int] = mapped_column(nullable=True)
    total_work_price: Mapped[int] = mapped_column(nullable=True)
    total_operation_price: Mapped[int] = mapped_column(nullable=True)
    total_material_price: Mapped[int] = mapped_column(nullable=True)

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
