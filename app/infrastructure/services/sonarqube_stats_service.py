import random
import time
from app.domain.services.analytics_service import AnalyticsService


class SonarqubeAnalyticsService(AnalyticsService):
    async def get_stats(self, file: bytes) -> dict:
        if random.random() < 0.2:  # эмуляция ошибки
            raise Exception("Ошибка в получении характеристик файла")

        time.sleep(random.uniform(0.1, 5))  # эмуляция обработки во внешнеми api

        return {
            "coverage": round(random.uniform(0, 100), 2),
            "bugs": {
                "total": random.randint(5, 20),
                "critical": random.randint(0, 5),
                "major": random.randint(0, 10),
                "minor": random.randint(0, 15),
            },
            "code_smells": {
                "total": random.randint(5, 20),
                "critical": random.randint(0, 5),
                "major": random.randint(0, 10),
                "minor": random.randint(0, 15),
            },
            "vulnerabilities": {
                "total": random.randint(5, 20),
                "critical": random.randint(0, 5),
                "major": random.randint(0, 10),
                "minor": random.randint(0, 15),
            },
        }
