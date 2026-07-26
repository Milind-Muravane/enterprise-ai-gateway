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

from src.cache.chroma import ChromaCache

from src.retrieval.hybrid import HybridRetriever
from src.prompt_builder import PromptBuilder

from src.schemas import (
    AIResponse,
    Provider,
    ModelName,
    CostTier,
)


class Gateway:

    def __init__(self):
        """Initialize all gateway components."""

        # Planning
        self.analyzer = QueryAnalyzer()
        self.estimator = RequestEstimator()
        self.planner = ExecutionPlanner()

        # Telemetry
        self.telemetry = TelemetryManager()

        # Router
        self.router = AdaptiveRouter(self.telemetry)

        # Cache
        self.cache = ChromaCache()

        # Hybrid Retrieval
        self.retriever = HybridRetriever()

        # Prompt Builder        
        self.prompt_builder = PromptBuilder()

    def _fallback_provider(self,provider: Provider,) -> Provider:
        """
        Returns the fallback provider.
        """

        if provider == Provider.GEMINI:
            return Provider.GROQ

        return Provider.GEMINI


    def process(self,question: str,) -> AIResponse:
        # Semantic Cache
        cache_result = self.cache.search(question)

        if cache_result.hit:

            print("Cache HIT!!!")

            return AIResponse(

                answer=cache_result.answer,

                provider=Provider.CACHE,

                model_name=None,

                latency_ms=0,

                prompt_tokens=0,

                completion_tokens=0,

                total_tokens=0,

                estimated_cost=CostTier.LOW,

                cache_hit=True,

            )

        print("Cache MISS!!!")

        # Analyze
        analysis = self.analyzer.analyze(question)
        # Estimate
        estimate = self.estimator.estimate(analysis)


        # Planning
        plan = self.planner.create_plan(  analysis=analysis,estimate=estimate,)

        # Hybrid Retrieval
        prompt = question

        if plan.use_rag or plan.use_web_search:

            print("Retrieving knowledge...")

            context = self.retriever.retrieve(
                question=question,
                plan=plan,
            )

            prompt = self.prompt_builder.build(
                question=question,
                context=context,
            )

        # Routing
        decision = self.router.select_provider(plan)

        provider = get_provider(decision.provider)

    
        # Provider Execution
        try:

            response = provider.generate(
                prompt=prompt,
                model=decision.model_name,
            )

        except Exception as e:

            print(f"Primary provider failed: {e}")

            fallback_provider = self._fallback_provider(
                decision.provider
            )

            provider = get_provider(
                fallback_provider
            )

            if fallback_provider == Provider.GEMINI:

                fallback_model = ModelName.GEMINI_FLASH

            else:

                fallback_model = ModelName.LLAMA_3_1_8B

            print(
                f"Switching to {fallback_provider.value}"
            )

            response = provider.generate(
                prompt=prompt,
                model=fallback_model,
            )

            response.provider = fallback_provider

            response.model_name = fallback_model
    
        # Cache New Response
        self.cache.add(
            question=question,
            answer=response.answer,
        )

        # Attach Metadata
        if response.provider is None:
            response.provider = decision.provider

        if response.model_name is None:
            response.model_name = decision.model_name

        response.execution_plan = plan

        response.routing_decision = decision

      
        # Store Telemetry
        self.telemetry.record(response)

        return response