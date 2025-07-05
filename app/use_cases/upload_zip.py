import hashlib
import uuid
from app.domain.schemas.task import TaskStatusEnum, TestResults
from app.domain.repositories.task_repository import TaskRepository
from app.domain.services.analytics_service import AnalyticsService
from app.domain.services.storage_service import StorageService
from fastapi import HTTPException, UploadFile


class UploadArchiveUseCase:
    def __init__(
        self,
        task_repo: TaskRepository,
        storage_service: StorageService,
        analysis_service: AnalyticsService,
    ):
        self.task_repo = task_repo
        self.storage_service = storage_service
        self.analytics_service = analysis_service

    async def execute(self, file: UploadFile, filename: str) -> uuid.UUID:
        if not (filename.endswith(".zip")):
            raise HTTPException(status_code=400, detail="Только ZIP-архивы разрешены")

        file_hash = self._calculate_file_hash(file)

        if await self.storage_service.file_exists(file_hash):
            raise HTTPException(status_code=409, detail="Файл уже загружен")

        upload_result = await self.storage_service.upload_file(file, file_hash)
        if not upload_result:
            raise HTTPException(status_code=500, detail="Ошибка при загрузке файла")

        task = TestResults(task_id=file_hash, status=TaskStatusEnum.PENDING)

        try:
            task_id = await self.task_repo.create_task(task)
        except Exception:
            await self.storage_service.delete_file(file_hash)
            raise HTTPException(
                status_code=500, detail="Ошибка при добавлении файла в бд"
            )

        return task_id

    def _calculate_file_hash(self, file: UploadFile) -> str:
        """Вычисляет SHA-256 хеш файла"""
        hasher = hashlib.sha256()
        file.file.seek(0)
        while chunk := file.file.read(4096):
            hasher.update(chunk)
        file.file.seek(0)
        return hasher.hexdigest()
