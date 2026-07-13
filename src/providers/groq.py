"""
Groq Provider implementation.
"""

import time

from litellm import completion

from src.config import settings
from src.schemas import (
    AIResponse,
    CostTier,
    Provider,
)
from src.providers.base import BaseProvider


class GroqProvider(BaseProvider):

    def generate(
        self,
        prompt: str,
        model: ModelName,
    ) -> AIResponse:

        start = time.perf_counter()

        response = completion(
            model=f"groq/{model.value}",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            api_key=settings.groq_api_key,
        )

        latency = (time.perf_counter() - start) * 1000

        answer = response.choices[0].message.content

        return AIResponse(
            answer=answer,
            provider=Provider.GROQ,
            model_name=ModelName(model),
            latency_ms=round(latency, 2),
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            finish_reason=response.choices[0].finish_reason,
            estimated_cost=CostTier.LOW,
            cache_hit=False,
        )