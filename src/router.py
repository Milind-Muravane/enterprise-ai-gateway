"""
Adaptive Router

Chooses the most appropriate provider and model
based on the execution plan.

Version 1:
Rule-based routing with telemetry ranking.

Version 2:
Adaptive routing using live telemetry.
"""

from src.schemas import (
    ExecutionPlan,
    RoutingDecision,
    Provider,
    ModelName,
)


from src.telemetry.manager import TelemetryManager


class AdaptiveRouter:

    def __init__(
        self,
        telemetry : TelemetryManager,
    ):
        self.scorer = ProviderScorer(telemertry)
        self.ranker = ProviderRanker()

    def select_provider(
        self,
        plan: ExecutionPlan,
    ) -> RoutingDecision:

        reasons = []

        # For the Complex Requests
        if (
            plan.requires_reasoning
            or plan.priority == "QUALITY"
            or plan.complexity_score >= 4
        ):

            reasons.append("Complex reasoning request.")
            reasons.append("Using Gemini Flash (Free Tier).")

            return RoutingDecision(
                provider=Provider.GEMINI,
                model_name=ModelName.GEMINI_FLASH,
                routing_reason=reasons,
                expected_latency_ms=900,
            )

        # Web Search
        if plan.use_web_search:

            reasons.append("Requires current information.")
            reasons.append("Using Gemini Flash.")

            return RoutingDecision(
                provider=Provider.GEMINI,
                model_name=ModelName.GEMINI_FLASH,
                routing_reason=reasons,
                expected_latency_ms=900,
            )

       
        # Simple Request
        best_provider = self.telemetry.get_fastest_provider()

        if best_provider == Provider.GROQ:

            reasons.append("Simple request.")
            reasons.append("Groq currently has the lowest average latency.")

            return RoutingDecision(
                provider=Provider.GROQ,
                model_name=ModelName.LLAMA_3_1_8B,
                routing_reason=reasons,
                expected_latency_ms=300,
            )

        reasons.append("Simple request.")
        reasons.append("Gemini currently has the lowest average latency.")

        return RoutingDecision(
            provider=Provider.GEMINI,
            model_name=ModelName.GEMINI_FLASH,
            routing_reason=reasons,
            expected_latency_ms=900,
        )