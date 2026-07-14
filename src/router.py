"""
Adaptive Router

Chooses the most appropriate provider and model
based on the execution plan.

Version 1:
Rule-based routing.

Version 2:
Telemetry-aware adaptive routing.
"""

from src.schemas import(
    ExecutionPlan, RoutingDecision, Provider, ModelName,
)

class AdaptiveRouter:
    def select_provider(self, plan: ExecutionPlan) -> RoutingDecision:
        reasons = []

        #for the complex requests
        if (plan.requires_reasoning or plan.priority == "QUALITY" or plan.complextiy_scores >= 4):
            reasons.append("Complex reasoning request.")
            reasons.append("Using Gemini Pro.")

            return RoutingDecision(
                provider = Provider.GEMINI,
                model_name = ModelName.GEMINI_PRO,
                routing_reason = reasons,
                expected_latency_ms = 2500,
            )

        # for the web search
        if plan.use_web_search:
            reasons.append("Requires current information.")
            reasons.append("Using Gemini Flash.")

            return RoutingDecision(
                provider=Provider.GEMINI,
                model_name=ModelName.GEMINI_FLASH,
                routing_reason=reasons,
                expected_latency_ms=900,
            )
        
        #for the  default conditions
        reasons.append("Simple request.")
        reasons.append("Using Groq for lowest latency.")

        return RoutingDecision(
            provider=Provider.GROQ,
            model_name=ModelName.LLAMA_3_1_8B,
            routing_reason=reasons,
            expected_latency_ms=300,
        )