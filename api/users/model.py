import uuid

import bcrypt
from sqlalchemy.dialects.postgresql import BIGINT

from utils.base.db_model import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Users(Base):
    __tablename__ = "users"

    firstname: Mapped[str]
    lastname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(unique=True, nullable=True)
    role: Mapped[str]
    avatar: Mapped[str] = mapped_column(nullable=True)
    telegram: Mapped[str] = mapped_column(nullable=True)
    telegram_id: Mapped[int] = mapped_column(type_=BIGINT, nullable=True)

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
