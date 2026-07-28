"""
Routing Strategy

Generates routing weights based on
the execution plan.
"""
from src.schemas import ExecutionPlan
from src.schemas import Priority

class WeightStrategy:
    def generate(self,plan:ExecutionPlan,)->dict:
        weights = {
            "reasoning" : 1.0,
            "performance" : 2.0,
            "cost" : 2.0,
            "context" : 1.0,
            "freshness" : 1.0,
        }
        # Complex questions
        if plan.requires_reasoning:
            weights['reasoning'] = 5.0
        
        # Enterprise RAG
        if plan.use_rag:
            weights['context'] = 5.0
        
        # Current info
        if plan.use_web_search:
            weights['freshness'] = 5.0
        
        # Highly imp request
        if plan.priority == Priority.QUALITY:
            weights['performance'] = 4.0
        return weights
