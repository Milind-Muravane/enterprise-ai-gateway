"""
Provider Ranker

Ranks providers using telemetry statistics.

Version 1:
Uses average latency.

Future Versions:
- Success rate
- Cost
- Token efficiency
"""
from src.schemas import (
    Provider,
)

from src.telemetry.statistics import StatisticsManager

class ProviderRanker:
    def __init__(self, statistics : StatisticsManager):
        self.statistics = statistics
    
    def get_fastest_provider(self)->Provider:
        groq_stats = self.statistics.get_provider_statistics(Provider.GROQ)
        gemini_stats = self.statistics.get_provider_statistics(Provider.GEMINI)

        # If one provider has never been used,
        # prefer the other provider.

        if groq_stats.request_count == 0:
            return Provider.GEMINI
        
        if gemini_stats.request_count == 0:
            return Provider.GROQ

        if (groq_stats.average_latency_ms <= gemini_stats.average_latency_ms):
            return Provider.GROQ
        else:
            return Provider.GEMINI