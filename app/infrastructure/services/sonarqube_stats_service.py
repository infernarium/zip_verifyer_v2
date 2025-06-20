from app.domain.services.analytics_service import AnalyticsService


class SonarqubeAnalyticsService(AnalyticsService):
    def get_stats(self, filedata: bytes) -> dict: ...
