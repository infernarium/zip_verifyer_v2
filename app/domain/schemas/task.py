import uuid
from pydantic import BaseModel
from typing import Optional, Dict
from app.domain.models.task import TaskStatusEnum


class UploadResponseSchema(BaseModel):
    task_id: uuid.UUID


class TestResults(BaseModel):
    overall_coverage: float
    bugs: Dict[str, int]
    code_smells: Dict[str, int]
    vulnerabilities: Dict[str, int]


class TaskUpdateSchema(BaseModel):
    status: Optional[TaskStatusEnum] = None
    results: Optional[TestResults] = None


class ReportResponseSchema(BaseModel):
    status: TaskStatusEnum
    results: Optional[TestResults] = None
