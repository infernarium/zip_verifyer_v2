from sqlalchemy import String, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.models.Base import Base
from typing import Optional
import enum
import uuid


class TaskStatusEnum(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class TaskResult(Base):
    __tablename__ = "task_results"

    task_id: Mapped[uuid.UUID] = mapped_column(String, primary_key=True, index=True)
    status: Mapped[TaskStatusEnum] = mapped_column(
        Enum(TaskStatusEnum), default=TaskStatusEnum.PENDING, nullable=False
    )
    results: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
