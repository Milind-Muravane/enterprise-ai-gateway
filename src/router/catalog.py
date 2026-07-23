"""
Provider Capability Catalog

Static capabilities of each provider/model.
"""

from src.schemas import Provider, ModelName

PROVIDER_CATALOG = {
    (Provider.GROQ, ModelName.LLAMA_3_1_8B): {
        "reasoning": 6,
        "speed": 10,
        "cost": 10,
        "context": 4,
        "freshness": 5,
    },

    (Provider.GEMINI, ModelName.GEMINI_FLASH): {
        "reasoning": 8,
        "speed": 8,
        "cost": 7,
        "context": 8,
        "freshness": 10,
    },

    (Provider.GEMINI, ModelName.GEMINI_PRO): {
        "reasoning": 10,
        "speed": 5,
        "cost": 4,
        "context": 10,
        "freshness": 10,
    },

}