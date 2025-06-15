import uuid
from fastapi.routing import APIRouter
from app.domain.schemas.task import ReportAnswerSchema


task_router = APIRouter(tags=["report"])


@task_router.get("/report/{id}", response_model=ReportAnswerSchema)
def get_report(id: uuid.UUID) -> ReportAnswerSchema:
    return {"id": id}
