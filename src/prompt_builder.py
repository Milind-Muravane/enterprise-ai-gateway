"""
Prompt Builder

Builds the final prompt for the language model.
"""
from src.schemas import HybridContext

class PromptBuilder:
    def build(self,question: str, context : HybridContext,)-> str:
        
        prompt = f"""
        You are an Enterprise AI Assistant.

        Follow these rules:

        1. Prefer Enterprise Context whenever it answers the question.
        2. Use Web Context only for recent or external information.
        3. If both contexts are available, combine them.
        4. If neither context contains the answer, answer using your own knowledge.

        ==================================================
        ENTERPRISE CONTEXT
        ==================================================

        {context.enterprise_context}

        ==================================================
        WEB CONTEXT
        ==================================================

        {context.web_context}

        ==================================================
        QUESTION
        ==================================================

        {question}

        ==================================================
        ANSWER
        ==================================================
        """
        return prompt
