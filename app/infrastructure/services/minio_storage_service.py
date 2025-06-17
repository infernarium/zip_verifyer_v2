from minio import Minio
from app.domain.services.storage_service import StorageService


class MinioStorageService(StorageService):
    def __init__(self, minio_client: Minio):
        self.client = minio_client

    async def upload_file(self, file_data: bytes, file_hash: str) -> bool: ...

    async def file_exists(self, file_hash: str) -> bool: ...

    async def delete_file(self, file_hash: str) -> bool: ...
