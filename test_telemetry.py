from src.schemas import (
    TelemetryRecord,
    Provider,
    ModelName,
)

from src.telemetry.collector import TelemetryCollector
from src.telemetry.statistics import StatisticsManager

collector = TelemetryCollector()

collector.add_record(

    TelemetryRecord(

        provider=Provider.GROQ,

        model_name=ModelName.LLAMA_3_1_8B,

        latency_ms=180,

        prompt_tokens=30,

        completion_tokens=70,

        total_tokens=100,

        success=True,
    )
)

collector.add_record(

    TelemetryRecord(

        provider=Provider.GROQ,

        model_name=ModelName.LLAMA_3_1_8B,

        latency_ms=220,

        prompt_tokens=40,

        completion_tokens=80,

        total_tokens=120,

        success=True,
    )
)

stats = StatisticsManager(collector)

result = stats.get_provider_statistics(
    Provider.GROQ
)

print(result.model_dump_json(indent=2))