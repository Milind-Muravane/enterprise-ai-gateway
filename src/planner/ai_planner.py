"""
AI Planner

Uses a lightweight LLM to generate
an execution plan for the gateway.
"""

import json

from src.providers.factory import get_provider

from src.schemas import (
    Provider,
    ModelName,
    ExecutionPlan,
    PlanningDecision,
    CostTier,
)

class AIPlanner:
    def __init__(self):
        self.provider = get_provider(Provider.GEMINI)
        self.model = ModelName.GEMINI_FLASH

    def _build_prompt(self, question : str,)-> str:
        return f"""
            You are an AI Planning Engine.

            Your task is NOT to answer the user's question.

            Your task is to decide how the Enterprise AI Gateway should execute it.

            Return ONLY valid JSON.

            Schema:

            {{
                "use_rag": true,
                "use_web_search": false,
                "requires_reasoning": false,
                "complexity_score": 2,
                "priority": "FAST",
                "reasoning_trace": [
                    "Question refers to internal company policy."
                ]
            }}

            Rules:

            1. If the question is about company documents, policies, HR, travel policy,
            expenses, reimbursement, employees or internal information:
            -> use_rag = true

            2. If the question asks for latest/current/recent information, news, weather,
            visa rules, stock prices or other live information:
            -> use_web_search = true

            3. If the question requires comparison, recommendation, evaluation,
            analysis or decision making:
            -> requires_reasoning = true

            4. Complexity must be between 1 and 5.

            5. Priority must be one of:
            FAST
            BALANCED
            QUALITY

            Return ONLY JSON.

            Priority Guidelines

            FAST:
            - Simple factual questions
            - Greetings
            - Small requests

            BALANCED:
            - Uses RAG
            - Uses Web Search
            - Moderate reasoning

            QUALITY:
            - Uses both RAG and Web Search
            - Complex analysis
            - Comparisons
            - Recommendations
            - High reasoning

            Question:

            {question}
            """

    def plan(self, question : str,)-> ExecutionPlan:
        prompt = self._build_prompt(question)

        response = self.provider.generate(prompt=prompt, model=self.model,)
        
        try:
            cleaned = (response.answer.replace("```json", "").replace("```", "").strip())
            decision = PlanningDecision.model_validate_json(cleaned)
        except Exception as e:
            raise ValueError(f"Invalid planner response: {e}")

        return ExecutionPlan(
            use_cache=True,
            use_rag=decision.use_rag,
            use_web_search=decision.use_web_search,
            estimated_cost=CostTier.LOW,
            estimated_input_tokens=0,
            estimated_output_tokens=0,
            estimated_latency_ms=500,
            priority=decision.priority,
            complexity_score=decision.complexity_score,
            requires_reasoning=decision.requires_reasoning,
            reasoning_trace=decision.reasoning_trace,
        )