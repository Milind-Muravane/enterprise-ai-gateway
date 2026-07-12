"""
Base provider interface.

Every LLM provider must implement this interface.
"""

from abc import ABC, abstractmethod
from src.schemas import AIResponse
from src.schemas import ModelName

class BaseProvider(ABC):
    """
    This is the abstract interface for all LLM providers.
    """
    @abstractmethod
    def generate(self,prompt : str, model :ModelName,)-> AIResponse:
        """
        Generate a response from an LLM.

        Args:
            prompt: User prompt.
            model: Model identifier.

        Returns:
            AIResponse
        """   
        pass 