from app.domain.repositories.task_repository import TaskRepository
from app.domain.schemas.task import ReportResponseSchema


class UploadArchiveUseCase:
    def __init__(
        self,
        task_repo: TaskRepository,
    ):
        self.task_repo = task_repo

    async def execute(self, file_id: int) -> ReportResponseSchema:
        task = await self.task_repo.get_task_by_id(file_id)
        return task
