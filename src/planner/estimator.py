"""
Request Estimator

Uses the analysis results to estimate:
- Cost tier
- Expected latency
- Expected output tokens
- Execution priority

No LLM calls are made here.
"""
from src.schemas import (AnalysisResult, EstimateResult, CostTier)

class RequestEstimator:
    """
    Estimates execution characteristics for a request.
    """

    def estimate(self, analysis : AnalysisResult) -> EstimateResult:
        #Estimating output tokens 
        estimated_output_tokens = max(50, analysis.estimated_input_tokens * 2)

        #deciding cost tier of the model based on the estimated cost
        if analysis.complexity_score <= 2:
            estimated_cost = CostTier.LOW
        elif analysis.complexity_score <= 4:
            estimated_cost = CostTier.MEDIUM
        else:
            estimated_cost = CostTier.HIGH
        
        #Estimate latency in ms
        if estimated_cost == CostTier.LOW:
            estimated_latency_ms = 500
        elif estimated_cost == CostTier.MEDIUM:
            estimated_latency_ms = 1500
        else:
            estimated_latency_ms = 3000
            
        #Deciding priority 
        if analysis.requires_reasoning:
            priority = "QUALITY"
        elif analysis.requires_web_search:
            priority = "BALANCED"
        else:
            priority = "FAST"
        
        #returning estimated results
        return EstimateResult(
            estimated_cost=estimated_cost,
            estimated_latency_ms=estimated_latency_ms,
            estimated_output_tokens=estimated_output_tokens,
            priority=priority

        )
        
