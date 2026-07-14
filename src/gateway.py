"""
Enterprise AI Gateway

Orchestrates the complete request lifecycle.
"""
from src.planner.analyzer import QueryAnalyzer
from src.planner.estimator import RequestEstimator
from src.planner.planner import ExecutionPlanner 
from src.router import AdaptiveRouter

from src.providers.factory import get_provider
from src.schemas import (AIResponse,)


class Gateway:
    def __init__(self):
        """Initialize the gateway with all components"""

        self.analyzer = QueryAnalyzer()
        self.estimator = RequestEstimator()
        self.planner = ExecutionPlanner()
        self.router = AdaptiveRouter()

    
    def process(self, question : str, )-> AIResponse:
        #analyse the request
        analysis = self.analyzer.analyze(question)

        #estimate the cost and other params
        estimate = self.estimator.estimate(analysis)

        #creating plan for the execution of the query
        plan = self.planner.create_plan(analysis= analysis, estimate= estimate)

        #routing 
        decision = self.router.select_provider(plan)

        #provider
        provider = get_provider(decision.provider)

        #generate response from provider
        response = provider.generate(prompt = question, model = decision.model_name)

        #attach imp metadata
        response.execution_plan = plan
        response.routing_decision = decision
        
        return response