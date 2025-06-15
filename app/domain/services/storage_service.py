from abc import ABC, abstractmethod


class StorageService(ABC):
    @abstractmethod
    async def upload_file(self, file_data: bytes, file_hash: str) -> bool: ...

    @abstractmethod
    async def file_exists(self, file_hash: str) -> bool: ...

    @abstractmethod
    async def delete_file(self, file_hash: str) -> bool: ...
