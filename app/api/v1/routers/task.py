from fastapi.routing import APIRouter
from app.domain.schemas.task import ReportAnswerSchema


archive_router = APIRouter(tags=["report"])


@archive_router.get("/report/{id}", response_model=ReportAnswerSchema)
def get_report(id: int) -> ReportAnswerSchema:
    return {"id": id}
