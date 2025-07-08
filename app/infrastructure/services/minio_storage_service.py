from io import BytesIO
from minio import Minio
from minio.error import S3Error
from app.config import MinioSettings
from app.domain.services.storage_service import StorageService


class MinioStorageService(StorageService):
    def __init__(self, minio_client: Minio, settings: MinioSettings):
        self.settings = settings
        self.client = minio_client

        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET_NAME):
                self.client.make_bucket(settings.MINIO_BUCKET_NAME)
        except S3Error as e:
            print(f"ERROR: {e}")
            exit(1)

    async def upload_file(self, file_data: bytes, file_id: str) -> bool:
        file_stream = BytesIO(file_data)

        try:
            self.client.put_object(
                bucket_name=self.settings.MINIO_BUCKET_NAME,
                object_name=file_id,
                data=file_stream,
                length=len(file_data),
                content_type="application/zip",
            )
        except S3Error as e:
            raise e

        return True

    async def file_exists(self, file_id: str) -> bool:
        try:
            self.client.stat_object(self.settings.MINIO_BUCKET_NAME, file_id)
            return True
        except S3Error as e:
            raise e

    async def delete_file(self, file_id: str) -> bool:
        try:
            self.client.remove_object(self.settings.MINIO_BUCKET_NAME, file_id)
            return True
        except S3Error as e:
            raise e
