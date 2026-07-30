"""
Telemetry Statistics

Computes provider statistics from telemetry records.
"""

from src.schemas import (
    Provider,
    ProviderStatistics,
    ModelName
)

from src.telemetry.collector import TelemetryCollector


class StatisticsManager:

    def __init__(
        self,
        collector: TelemetryCollector,
    ):

        self.collector = collector

    def get_provider_statistics(
        self,
        provider: Provider,
    ) -> ProviderStatistics:

        records = [

            record

            for record in self.collector.get_records()

            if record.provider == provider

        ]

        if not records:

            return ProviderStatistics(
                provider=provider,
                request_count=0,
                average_latency_ms=0,
                average_total_tokens=0,
                success_rate=0,
            )

        request_count = len(records)

        average_latency = sum(

            r.latency_ms

            for r in records

        ) / request_count

        average_tokens = sum(

            r.total_tokens

            for r in records

        ) / request_count

        success_rate = (

            sum(

                r.success

                for r in records

            )

            / request_count

        )

        return ProviderStatistics(

            provider=provider,

            request_count=request_count,

            average_latency_ms=round(average_latency, 2),

            average_total_tokens=round(average_tokens, 2),

            success_rate=round(success_rate, 2),
        )

    def predict_latency(self, provider : Provider, model_name : ModelName, history_size : int = 10,) -> float:
        """
            Predict the expected latency for a provider/model combination
            using the average latency of the most recent successful requests.
        """

        records = [record for record in self.collector.get_records()
        if (
            record.provider == provider and record.model_name == model_name and record.success
            )
        ]

        if not records:
            DEFAULT_PROVIDER_LATENCIES = {
            Provider.GROQ: 800.0,
            Provider.GEMINI: 1800.0,
            Provider.OPENAI: 1200.0,
            }

            return DEFAULT_PROVIDER_LATENCIES.get(provider, 1000.0)

        recent_records = records[-history_size:]

        average_latency = (
            sum(record.latency_ms for record in recent_records)
            / len(recent_records)
        )

        return round(average_latency, 2)
