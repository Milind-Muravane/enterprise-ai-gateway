"""
Provider Scorer

Calculates a numerical score for each provider-model pair.
"""

from src.schemas import (
    ExecutionPlan,
    Provider,
    ModelName,
    ProviderScore,
)

from src.router.catalog import PROVIDER_CATALOG
from src.router.strategy import WeightStrategy

from src.telemetry.manager import TelemetryManager


class ProviderScorer:

    def __init__(self,telemetry : TelemetryManager,):

        self.telemetry = telemetry

        self.strategy = WeightStrategy()

    def score(
        self,
        provider: Provider,
        model: ModelName,
        plan: ExecutionPlan,
    ) -> ProviderScore:
        """
        Calculates the final provider score.
        """

        # Generate routing weights once
        weights = self.strategy.generate(plan)

        capability = self._capability_score(
            provider,
            model,
            plan,
            weights,
        )

        reasoning = self._reasoning_score(
            provider,
            model,
            plan,
            weights,
        )

        performance = self._performance_score(
            provider,
            model,
            plan,
            weights,
        )

        cost = self._cost_score(
            provider,
            model,
            plan,
            weights,
        )

        breakdown = {
            "capability": capability,
            "reasoning": reasoning,
            "performance": performance,
            "cost": cost,
        }

        total = sum(breakdown.values())

        return ProviderScore(
            provider=provider,
            model_name=model,
            total_score=total,
            score_breakdown=breakdown,
        )

    # ----------------------------------------------------
    # Helper
    # ----------------------------------------------------

    def _capabilities(
        self,
        provider: Provider,
        model: ModelName,
    ) -> dict:

        return PROVIDER_CATALOG[(provider, model)]

    # ----------------------------------------------------
    # Capability Score
    # ----------------------------------------------------

    def _capability_score(
        self,
        provider: Provider,
        model: ModelName,
        plan: ExecutionPlan,
        weights: dict,
    ) -> float:

        caps = self._capabilities(provider, model)

        score = 0.0

        if plan.requires_reasoning:
            score += (
                caps["reasoning"]
                * weights["reasoning"]
            )

        if plan.use_web_search:
            score += (
                caps["freshness"]
                * weights["freshness"]
            )

        if plan.use_rag:
            score += (
                caps["context"]
                * weights["context"]
            )

        return score

    # ----------------------------------------------------
    # Reasoning Score
    # ----------------------------------------------------

    def _reasoning_score(
        self,
        provider: Provider,
        model: ModelName,
        plan: ExecutionPlan,
        weights: dict,
    ) -> float:

        caps = self._capabilities(provider, model)

        complexity = plan.complexity_score

        return (
            caps["reasoning"]
            * complexity
            * weights["reasoning"]
            * 0.1
        )

    # ----------------------------------------------------
    # Performance Score
    # ----------------------------------------------------

    def _performance_score(
        self,
        provider: Provider,
        model: ModelName,
        plan: ExecutionPlan,
        weights: dict,
    ) -> float:
        """
        Calculates a telemetry-based performance score.

        Factors:
        - Average latency
        - Success rate
        - Confidence (based on request count)
        """

        try:
            stats = self.telemetry.get_statistics(provider)

        except Exception:
            return 0.0

        if stats.request_count == 0:
            return 0.0

        score = 0.0

        # ----------------------------------------------------
        # Latency Score (0-10)
        # ----------------------------------------------------

        latency = stats.average_latency_ms

        if latency <= 500:
            latency_score = 10

        elif latency <= 1000:
            latency_score = 8

        elif latency <= 1500:
            latency_score = 6

        elif latency <= 2500:
            latency_score = 3

        else:
            latency_score = 0

        # ----------------------------------------------------
        # Success Rate Score (0-10)
        # ----------------------------------------------------

        success_score = stats.success_rate * 10

        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        if stats.request_count >= 20:
            confidence = 1.0

        elif stats.request_count >= 10:
            confidence = 0.8

        elif stats.request_count >= 5:
            confidence = 0.6

        else:
            confidence = 0.4

        # ----------------------------------------------------
        # Final Performance Score
        # ----------------------------------------------------

        score = (
            latency_score * 0.4
            + success_score * 0.6
        )

        return round(
            score * confidence * weights["performance"],
            2,
        )
    # ----------------------------------------------------
    # Cost Score
    # ----------------------------------------------------

    def _cost_score(
        self,
        provider: Provider,
        model: ModelName,
        plan: ExecutionPlan,
        weights: dict,
    ) -> float:

        caps = self._capabilities(provider, model)

        return (
            caps["cost_efficiency"]
            * weights["cost"]
        )