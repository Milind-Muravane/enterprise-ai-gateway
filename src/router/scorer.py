"""
Provider Scorer

Assigns a numerical score to every candidate provider.
"""
from src.schemas import(ExecutionPlan, Provider, ModelName, ProviderScore)
from src.router.catalog import PROVIDER_CATALOG


class ProviderScorer:
    def score(self, provider: Provider, model : ModelName, plan : ExecutionPlan, )-> ProviderScore:
        """
            It returns the score for one provider.
        """
        
        reasoning = self._reasoning_score(provider, model, plan)
        latency = self._latency_score(provider, model, plan)
        cost = self._cost_score(provider, model, plan)
        telemetry = self._telemetry_score(provider, model, plan)
        capability = self._capability_score(provider, model, plan)


        breakdown = {
            "reasoning" : reasoning,
            "latency" : latency,
            "cost" : cost, 
            "telemetry" : telemetry,
            "capability" : capability,
        }

        total = sum(breakdown.values())

        return ProviderScore(
            provider= provider, 
            model_name = model,
            total_score = total,
            score_breakdown = breakdown,
        )

    def _capabilities(self,provider: Provider, model: ModelName,)-> dict:
        return PROVIDER_CATALOG[(provider, model)]

    def _capability_score(self, provider : Provider, model : ModelName, plan : ExecutionPlan,)->float:
        caps = self._capabilities(provider , model)
        score = 0.0

        # Reasoning capability
        if plan.requires_reasoning:
            score += caps['reasoninig']*2
        
        # Web search capability
        if plan.use_web_search:
            score += caps['freshness']

        # Enterprise RAG Capability
        if plan.use_rag:
            score += caps['context']
        
        return score

    def _reasoning_score(self,provider,model,plan,)->float:
        return 0.0

    def _latency_score(self,provider,model,plan,)->float:
        return 0.0

    def _cost_score(self,provider,model,plan,)->float:
        return 0.0

    def _telemetry_score(self,provider,model,plan,)->float:
        return 0.0

    def _capability_score(self,provider,model,plan,)->float:
        return 0.0