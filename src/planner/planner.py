"""
Execution Planner

Combines:
- AnalysisResult
- EstimateResult

into a single ExecutionPlan.

The planner DOES NOT choose providers.
The planner only decides what the request needs.
"""

from src.schemas import ( 
    AnalysisResult, EstimateResult, ExecutionPlan,
)

class ExecutionPlanner:
    def create_plan(self, analysis : AnalysisResult, estimate: EstimateResult,)-> ExecutionPlan:
        return ExecutionPlan(
            user_cache = True,
            user_web_search = analysis.requires_web_search,
            use_rag = analysis.requires_rag,
            estimated_cost=estimate.estimated_cost,
            estimated_input_tokens=analysis.estimated_input_tokens,
            estimated_output_tokens=estimate.estimated_output_tokens,
            estimated_latency_ms=estimate.estimated_latency_ms,
            priority=estimate.priority,
            complexity_score=analysis.complexity_score,
            requires_reasoning=analysis.requires_reasoning,
            reasoning_trace=analysis.reasoning_trace,
        )