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
from src.router.weights import ROUTING_WEIGHTS

from src.telemetry.manager import TelemetryManager


class ProviderScorer:

    def __init__(self):

        self.telemetry = TelemetryManager()

    def score(
        self,
        provider: Provider,
        model: ModelName,
        plan: ExecutionPlan,
    ) -> ProviderScore:
        """
        Calculates the final provider score.
        """

        capability = self._capability_score(
            provider,
            model,
            plan,
        )

        reasoning = self._reasoning_score(
            provider,
            model,
            plan,
        )

        performance = self._performance_score(
            provider,
            model,
        )

        cost = self._cost_score(
            provider,
            model,
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
    ) -> float:

        caps = self._capabilities(provider, model)

        weights = ROUTING_WEIGHTS

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
    ) -> float:

        caps = self._capabilities(provider, model)

        complexity = plan.complextiy_scores

        return (
            caps["reasoning"]
            * complexity
            * 0.5
        )

    # ----------------------------------------------------
    # Performance Score
    # ----------------------------------------------------

    def _performance_score(
        self,
        provider: Provider,
        model: ModelName,
    ) -> float:

        try:

            stats = self.telemetry.statistics(provider)

        except Exception:

            return 0.0

        weights = ROUTING_WEIGHTS

        score = 0.0

        # Lower latency = Higher score
        if stats.average_latency_ms > 0:

            latency_score = max(
                0,
                10 - (stats.average_latency_ms / 500),
            )

            score += (
                latency_score
                * weights["performance"]
            )

        # Success rate

        score += (
            stats.success_rate
            * 10
            * weights["performance"]
        )

        return score

    # ----------------------------------------------------
    # Cost Score
    # ----------------------------------------------------

    def _cost_score(
        self,
        provider: Provider,
        model: ModelName,
    ) -> float:

        caps = self._capabilities(provider, model)

        return (
            caps["cost_efficiency"]
            * ROUTING_WEIGHTS["cost"]
        )