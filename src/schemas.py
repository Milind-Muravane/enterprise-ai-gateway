"""
Pydantic schemas for the Smart Enterprise AI Gateway.

These schemas define the typed contracts exchanged between
the Gateway, Router, Providers, Cache, Search, and UI.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field



# Enums
class ComplexityLevel(str, Enum):
    SIMPLE = "SIMPLE"
    MEDIUM = "MEDIUM"
    COMPLEX = "COMPLEX"


class CostTier(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Provider(str, Enum):
    GEMINI = "Gemini"
    GROQ = "Groq"


class ModelName(str, Enum):
    # Gemini Models
    GEMINI_FLASH = "gemini-2.5-flash"
    GEMINI_PRO = "gemini-2.5-pro"

    # Groq Models
    LLAMA_3_3_70B = "llama-3.3-70b-versatile"
    LLAMA_3_1_8B = "llama-3.1-8b-instant"



# Request Models
class UserRequest(BaseModel):
    question: str = Field(..., min_length=1)


class IntentClassification(BaseModel):
    complexity: ComplexityLevel
    estimated_cost: CostTier
    reasoning: str


# Planner Models

class AnalysisResult(BaseModel):
    prompt_length: int
    estimated_input_tokens: int
    sentence_count: int
    question_count: int
    requires_web_search: bool
    requires_rag: bool
    requires_reasoning: bool
    complexity_score: int
    detected_topics: list[str]
    reasoning_trace: list[str]


class EstimateResult(BaseModel):
    estimated_cost: CostTier
    estimated_latency_ms: int
    estimated_output_tokens: int
    priority: str


class ExecutionPlan(BaseModel):
    """
    Defines WHAT the gateway should do.
    Created by the Planner.
    """

    use_cache: bool = True
    use_web_search: bool = False
    use_rag: bool = False
    estimated_cost: CostTier
    estimated_input_tokens: int
    estimated_output_tokens: int
    estimated_latency_ms: int
    priority: str
    complexity_score: int
    requires_reasoning: bool
    reasoning_trace: list[str]


# Router Models
class RoutingDecision(BaseModel):
    """
    Defines WHO should execute the request.
    Created by the Adaptive Router.
    """

    provider: Provider
    model_name: ModelName
    routing_reason: list[str]
    expected_latency_ms: int



# Provider Response
class AIResponse(BaseModel):
    answer: str
    provider: Provider
    model_name: ModelName
    latency_ms: float
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    finish_reason: Optional[str] = None
    estimated_cost: CostTier
    cache_hit: bool = False
    execution_plan: Optional[ExecutionPlan] = None
    routing_decision: Optional[RoutingDecision] = None