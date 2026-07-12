"""
Pydantic schemas for the Smart Enterprise AI Gateway.

These schemas define the typed contracts exchanged between
the Gateway, Router, Providers, Cache, Search, and UI.
"""
from enum import Enum
from typing import Optional 
from pydantic import BaseModel,Field
from enum import Enum


class ComplexityLevel(str,Enum):
    SIMPLE = "SIMPLE"
    MEDIUM = "MEDIUM"
    COMPLEX = "COMPLEX"

class CostTier(str,Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Provider(str, Enum):
    GEMINI = "Gemini"
    GROQ = "Groq"

class UserRequest(BaseModel):
    question : str  = Field(..., min_length = 1)


class IntentClassification(BaseModel):
    complexity: ComplexityLevel
    estimated_cost: CostTier
    reasoning : str

# Execution plan of query
class ExecutionPlan(BaseModel):
    provider: Provider
    model_name: str
    use_cache: bool = True
    use_web_search: bool = False
    use_rag: bool = False
    estimated_cost: CostTier
    complexity: ComplexityLevel
    reasoning: str

# AI response

class AIResponse(BaseModel):
    answer: str
    provider: Provider
    model_name: str
    latency_ms: float

    #for finding the token usage
    prompt_tokens : int  = 0
    completion_tokens : int = 0
    total_tokens : int = 0
    
    #provider info

    finish_reason : Optional[str] = None
    estimated_cost: CostTier
    cache_hit: bool = False
    execution_plan: Optional[ExecutionPlan] = None

#this is creating to store different model names
class ModelName(str, Enum):
    # gemini models
    GEMINI_FLASH = "gemini-2.5-flash"
    GEMINI_PRO = "gemini-2.5-pro"

    #groq models
    LLAMA_3_3_70B = "llama-3.3-70b-versatile"
    LLAMA_3_1_8B = "llama-3.1-8b-instant"


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
    
