from src.schemas import (
    Provider,
    ModelName,
    TelemetryRecord,
)

from src.telemetry.collector import TelemetryCollector
from src.telemetry.statistics import StatisticsManager
from src.telemetry.ranker import ProviderRanker

collector = TelemetryCollector()

# -----------------------------
# Groq
# -----------------------------

collector.add_record(

    TelemetryRecord(
        provider=Provider.GROQ,
        model_name=ModelName.LLAMA_3_1_8B,
        latency_ms=170,
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
        latency_ms=190,
        prompt_tokens=40,
        completion_tokens=80,
        total_tokens=120,
        success=True,
    )
)

# -----------------------------
# Gemini
# -----------------------------

collector.add_record(

    TelemetryRecord(
        provider=Provider.GEMINI,
        model_name=ModelName.GEMINI_FLASH,
        latency_ms=900,
        prompt_tokens=30,
        completion_tokens=70,
        total_tokens=100,
        success=True,
    )
)

collector.add_record(

    TelemetryRecord(
        provider=Provider.GEMINI,
        model_name=ModelName.GEMINI_FLASH,
        latency_ms=1000,
        prompt_tokens=35,
        completion_tokens=85,
        total_tokens=120,
        success=True,
    )
)

statistics = StatisticsManager(collector)

ranker = ProviderRanker(statistics)

provider = ranker.get_fastest_provider()

print("=" * 50)

print(f"Fastest Provider: {provider.value}")