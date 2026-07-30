"""
Telemetry Manager

High-level interface for telemetry.

Owns:
- Collector
- Statistics Manager
- Provider Ranker
"""

from src.schemas import (AIResponse,Provider,TelemetryRecord)
from src.telemetry.collector import TelemetryCollector
from src.telemetry.statistics import StatisticsManager
from src.telemetry.ranker import ProviderRanker

class TelemetryManager:
    def __init__(self):
        self.collector = TelemetryCollector()
        self.statistics = StatisticsManager(self.collector)
        self.ranker = ProviderRanker(self.statistics)

    def record(self,response : AIResponse)->None:
        self.collector.add_record(
             TelemetryRecord(
                provider=response.provider,
                model_name=response.model_name,
                latency_ms=response.latency_ms,
                prompt_tokens=response.prompt_tokens,
                completion_tokens=response.completion_tokens,
                total_tokens=response.total_tokens,
                success=True,
            )
        )
    
    def get_fastest_provider(self,)->Provider:
        return self.ranker.get_fastest_provider()

    def get_statistics(self, provider : Provider):
        return self.statistics.get_provider_statistics(provider)

    def predict_latency(self,provider: Provider,model_name: ModelName,) -> float:

        return self.statistics.predict_latency(
            provider=provider,
            model_name=model_name,
        )