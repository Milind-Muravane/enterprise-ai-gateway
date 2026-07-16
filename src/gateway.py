"""
Enterprise AI Gateway

Coordinates the complete request lifecycle.
"""

from src.planner.analyzer import QueryAnalyzer
from src.planner.estimator import RequestEstimator
from src.planner.planner import ExecutionPlanner

from src.router import AdaptiveRouter

from src.providers.factory import get_provider

from src.telemetry.manager import TelemetryManager

from src.schemas import (
    AIResponse,
    TelemetryRecord,
)


class Gateway:

    def __init__(self):
        """Initialize all gateway components."""

        # Planner components
        self.analyzer = QueryAnalyzer()
        self.estimator = RequestEstimator()
        self.planner = ExecutionPlanner()

        # Telemetry
        self.telemetry = TelemetryManager()

        # Router
        self.router = AdaptiveRouter(self.telemetry)

    def process(
        self,
        question: str,
    ) -> AIResponse:

        # Analyze
        analysis = self.analyzer.analyze(question)


        # Estimate
        estimate = self.estimator.estimate(analysis)


        # Planning
        plan = self.planner.create_plan(
            analysis=analysis,
            estimate=estimate,
        )


        # Routing
        decision = self.router.select_provider(plan)


        # Provider
        provider = get_provider(decision.provider)


        # Generate Response
        response = provider.generate(
            prompt=question,
            model=decision.model_name,
        )


        # Attach Metadata
        response.execution_plan = plan
        response.routing_decision = decision


        # Store Telemetry
        self.telemetry.record(response)
        
        return response