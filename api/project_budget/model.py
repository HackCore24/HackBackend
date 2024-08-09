import uuid
from datetime import datetime
from typing import List

import bcrypt
from sqlalchemy.dialects.postgresql import BIGINT

from utils.base.db_model import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProjectBudget(Base):
    __tablename__ = 'project_budget'

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('projects.id'), nullable=False)
    budget: Mapped[float]
    credit_limit: Mapped[float]
