from abc import ABC, abstractmethod


class StorageService(ABC):
    @abstractmethod
    async def upload_file(self, file_data: bytes, file_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def file_exists(self, file_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete_file(self, file_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def get_file(self, file_id: str) -> bytes:
        raise NotImplementedError()
