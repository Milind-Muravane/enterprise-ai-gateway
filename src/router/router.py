"""
Adaptive Router
Selects the best provider using the
Provider Scorer and Provider Ranker.
"""
from src.router.scorer import ProviderScorer
from src.router.ranking import ProviderRanker

from src.schemas import (ExecutionPlan, RoutingDecision, Provider, ModelName,Priority)
from src.telemetry.manager import TelemetryManager
from typing import List

class AdaptiveRouter:
    def __init__(self,telemetry: TelemetryManager,):
        self.telemetry = telemetry
        self.scorer = ProviderScorer(telemetry)
        self.ranker = ProviderRanker()


    def _build_routing_reason(self, provider: Provider,score: float,capability_score: float,reasoning_score: float, performance_score: float, cost_score: float,   plan: ExecutionPlan,) -> list[str]:
    
        reasons = []
        reasons.append(f"Selected {provider.value} with the highest overall score ({score:.2f}).")
        
        if plan.priority == Priority.FAST:
            reasons.append("FAST priority favoured lower latency providers.")

        elif plan.priority == Priority.BALANCED:
            reasons.append("BALANCED priority considered latency, capability and cost.")

        elif plan.priority == Priority.QUALITY:
            reasons.append("QUALITY priority increased the weight of reasoning and capability.")

        if plan.use_rag:
            reasons.append("Enterprise knowledge retrieval was required.")

        if plan.use_web_search:
            reasons.append("Live web information was required.")

        if plan.requires_reasoning:
            reasons.append("Complex reasoning was detected.")

        if performance_score > 0:
            reasons.append(
                f"Telemetry performance score: {performance_score:.2f}."
            )

        return reasons



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
           routing_reason=self._build_routing_reason(
                provider=best.provider,
                score=best.total_score,
                capability_score=best.score_breakdown.get("capability", 0.0),
                reasoning_score=best.score_breakdown.get("reasoning", 0.0),
                performance_score=best.score_breakdown.get("performance", 0.0),
                cost_score=best.score_breakdown.get("cost", 0.0),
                plan=plan,
            ),
            expected_latency_ms = self.telemetry.predict_latency(best.provider,best.model_name,),
            score = best.total_score,
            score_breakdown = best.score_breakdown,
        )