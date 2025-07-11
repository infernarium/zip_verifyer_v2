# app/use_cases/upload_zip.py
import hashlib
import uuid
from app.domain.models.task import TaskResult
from app.domain.schemas.task import (
    TaskStatusEnum,
    TaskUpdateSchema,
    TestResults,
)
from app.domain.repositories.task_repository import TaskRepository
from app.domain.services.analytics_service import AnalyticsService
from app.domain.services.storage_service import StorageService
from fastapi import BackgroundTasks, HTTPException, UploadFile


class UploadArchiveUseCase:
    def __init__(
        self,
        task_repo: TaskRepository,
        storage_service: StorageService,
        analysis_service: AnalyticsService,
        background_tasks: BackgroundTasks,
    ):
        self.task_repo = task_repo
        self.storage_service = storage_service
        self.analytics_service = analysis_service
        self.background_tasks = background_tasks

    async def execute(self, file: UploadFile) -> uuid.UUID:
        # Предварительные проверки
        if not (file.filename.endswith(".zip")):
            raise HTTPException(status_code=400, detail="Только ZIP-архивы разрешены")

        file_hash = self._calculate_file_hash(file)

        exist_task_result = await self.task_repo.task_exists(file_hash)
        if exist_task_result:
            raise HTTPException(status_code=409, detail="Файл уже загружен")

        # Загрузка в S3
        file_id = str(uuid.uuid4())
        file_data = await file.read()
        upload_result = await self.storage_service.upload_file(file_data, file_id)
        if not upload_result:
            raise HTTPException(status_code=500, detail="Ошибка при загрузке файла")

        # Загрузка в бд
        task = TaskResult(
            task_id=file_id, task_hash=file_hash, status=TaskStatusEnum.PENDING
        )
        try:
            task_upload_result = await self.task_repo.create_task(task)
            task_id = task_upload_result.task_id
        except Exception:
            await self.storage_service.delete_file(file_hash)
            raise HTTPException(
                status_code=500, detail="Ошибка при добавлении файла в бд"
            )

        # Обрабатываем ошибки архива в фоне
        self.background_tasks.add_task(self._process_archive, task_id)

        return task_upload_result

    def _calculate_file_hash(self, file: UploadFile) -> str:
        """Вычисляет SHA-256 хеш файла"""
        hasher = hashlib.sha256()
        file.file.seek(0)
        while chunk := file.file.read(4096):
            hasher.update(chunk)
        file.file.seek(0)
        return hasher.hexdigest()

    async def _process_archive(self, task_id: uuid, attempt=1, max_retries=4) -> None:
        task_id = str(task_id)
        try:
            update_data = TaskUpdateSchema(status=TaskStatusEnum.IN_PROGRESS)
            await self.task_repo.update_task(task_id, update_data)

            file = await self.storage_service.get_file(task_id)
            if not (file):
                raise HTTPException(
                    status_code=500, detail="Ошибка при получении файла из S3"
                )

            analytic_result = await self.analytics_service.get_stats(file)
            test_results = TestResults(
                overall_coverage=analytic_result["coverage"],
                bugs=analytic_result["bugs"],
                code_smells=analytic_result["code_smells"],
                vulnerabilities=analytic_result["vulnerabilities"],
            )

            update_data = TaskUpdateSchema(results=test_results)
            await self.task_repo.update_task(task_id, update_data)

        except Exception as e:
            if attempt < max_retries:
                self.background_tasks.add_task(
                    self._process_archive, task_id, attempt + 1
                )
            else:
                update_data = TaskUpdateSchema(status=TaskStatusEnum.FAILED)
                await self.task_repo.update_task(task_id, update_data)
                raise f"Ошибка при обработке архива: {e}"
