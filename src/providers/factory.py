"""
Provider Factory.

Returns the correct LLM provider.
"""

from src.providers.gemini import GeminiProvider
from src.providers.groq import GroqProvider
from src.schemas import Provider


def get_provider(provider: Provider):

    if provider == Provider.GEMINI:
        return GeminiProvider()

    if provider == Provider.GROQ:
        return GroqProvider()

    raise ValueError(f"Unsupported provider: {provider}")