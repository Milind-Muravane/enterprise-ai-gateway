"""
Adaptive Router
Selects the best provider using the
Provider Scorer and Provider Ranker.
"""
from src.router.scorer import ProviderScorer
from src.router.ranking import ProviderRanker

from src.schemas import (ExecutionPlan, RoutingDecision, Provider, ModelName,)
from src.telemetry.manager import TelemetryManager

class AdaptiveRouter:
    def __init__(self,telemetry: TelemetryManager,):
        self.scorer = ProviderScorer(telemetry)
        self.ranker = ProviderRanker()

    def select_provider(self, plan: ExecutionPlan,)-> RoutingDecision:
        # Candidate provider-model pairs
        candidates = [
            (Provider.GROQ, ModelName.LLAMA_3_1_8B),
            (Provider.GEMINI, ModelName.GEMINI_FLASH),
            (Provider.GEMINI, ModelName.GEMINI_PRO)
        ]

        # Score each candidate
        scores = []

        for provider, model in candidates:
            provider_score = self.scorer.score(provider = provider, model = model, plan = plan,)
            scores.append(provider_score)

        # Rank candidates
        ranking = self.ranker.rank(scores)

        # Select best provider
        best = ranking.rankings[0]

        # Convert into RoutingDecision
        return RoutingDecision(
            provider = best.provider,
            model_name = best.model_name,
            routing_reason = ["Selected by adaptive scoring engine."],
            expected_latency_ms = 0,
            score = best.total_score,
            score_breakdown = best.score_breakdown,
        )