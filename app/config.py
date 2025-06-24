# app\config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class MinioSettings(BaseSettings):
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ROOT_USER: str = "minioadmin"
    MINIO_ROOT_PASSWORD: str = "minioadminpassword"
    MINIO_BUCKET_NAME: str = "zip-archives"

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"
    )


class PostgresSettings(BaseSettings):
    POSTGRES_DB: str = "zip_verifier"
    POSTGRES_USER: str = "zip_admin"
    POSTGRES_PASSWORD: str = "supersecurepassword"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:5432/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"
    )


class RedisSettings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"
    )


class ProjectSettings(BaseSettings):
    minio_settings: MinioSettings = MinioSettings()
    postgres_settings: PostgresSettings = PostgresSettings()
    redis_settings: RedisSettings = RedisSettings()


project_settings = ProjectSettings()
