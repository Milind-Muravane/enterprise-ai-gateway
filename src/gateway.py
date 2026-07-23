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

from src.schemas import (
    AIResponse,
    TelemetryRecord,
    Provider, ModelName,CostTier
)

from src.rag.retriever import DocumentRetriever
from src.rag.prompt_builder import PromptBuilder

from src.websearch.tavily import TavilySearch


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

        # Cache
        self.cache = ChromaCache()

        # Document Retriever
        self.retriever = DocumentRetriever()

        # Prompt Builder
        self.prompt_builder = PromptBuilder()

    def _fallback_provider(self,provider : Provider)->Provider:
        """
        Returns the fallback provider.
        """
        if provider == Provider.GEMINI:
            return Provider.GROQ
        return Provider.GEMINI





    def process(
        self,
        question: str,
    ) -> AIResponse:

        # Checking if question is present in cache or not
        cache_result = self.cache.search(question)
        
        if cache_result.hit:
            print("Cache HIT!")
            return AIResponse(
                answer = cache_result.answer,
                provider=Provider.CACHE, 
                model_name=None, 
                latency_ms=0,
                prompt_tokens = 0,
                completion_tokens = 0,
                total_tokens = 0,
                estimated_cost=CostTier.LOW,
                cache_hit=True,
            )
        
        print("Cache MISS!")

        # Analyze
        analysis = self.analyzer.analyze(question)


        # Estimate
        estimate = self.estimator.estimate(analysis)


        # Planning
        plan = self.planner.create_plan(
            analysis=analysis,
            estimate=estimate,
        )

        # RAG Part Prompt Building
        prompt  = question 
        if plan.use_rag:
            print("Retrieving company documents...please wait!")

            retrieval = self.retriever.retrieve(question)

            prompt = self.prompt_builder.build(question= question, retrieval=retrieval,)

        # Web Search
        elif plan.use_web_search:
            print("Searching on the web... Please wait!")
            search_result = self.web_search.search(question)

            prompt = self.prompt_builder.build_web_prompt(question = question,search_result=search_result)

        # Routing
        decision = self.router.select_provider(plan)


        # Provider
        provider = get_provider(decision.provider)


        # Generate Response (Using fallback provider strategy that gives response from another model if one fails)
        try:
            response = provider.generate(prompt = prompt, model = decision.model_name,)
        except Exception as e:
            print(f"Primary model failed!!! {e}")
            fallback_provider = self._fallback_provider(decision.provider)
            print(f"Switching now to {fallback_provider.value}")
            provider = get_provider(fallback_provider
            )

        if fallback_provider == Provider.GEMINI:
            fallback_model = ModelName.GEMINI_FLASH
        else:
            fallback_model = ModelName.LLAMA_3_1_8B
        
        response = provider.generate(prompt = prompt, model = fallback_model,)
        response.provider = fallback_provider
        response.model_name = fallback_model
         
        # Saving new responses
        self.cache.add(
            question = question,
            answer = response.answer,
        )


        # Update the response
        response.provider = decision.provider
        response.model_name = decision.model_name

        # Attach Metadata
        response.execution_plan = plan
        response.routing_decision = decision


        # Store Telemetry
        self.telemetry.record(response)
        
        return response