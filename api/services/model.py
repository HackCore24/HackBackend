import uuid
from utils.base.db_model import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Service(Base):
    __tablename__ = 'services'

    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int]


class Estimate(Base):
    __tablename__ = 'estimates'

    total_cost: Mapped[int]


class EstimateItem(Base):
    __tablename__ = 'estimate_items'

    estimate_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('estimates.id'))
    service_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('services.id'))
    quantity: Mapped[int]
