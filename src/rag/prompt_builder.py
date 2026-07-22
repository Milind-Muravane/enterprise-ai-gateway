"""
Prompt Builder

Builds an augmented prompt using
retrieved RAG context.
"""

from src.schemas import (RetrievalResult, WebSearchResult,)

class PromptBuilder:
    def build(self,question:str,retrieval: RetrievalResult)->str:
        context = "\n\n".join(chunk.text for chunk in retrieval.chunks)

        prompt = f"""
                You are an enterprise AI assistant.

                Answer ONLY using the provided context.

                If the answer is not present in the context,
                say that the information is unavailable.

                -------------------------
                Context

                {context}

                -------------------------

                Question:

                {question}
        """

        print("-"* 50)
        print("RAG Context")
        print("-"* 50)
        print(context)
        print("-"* 50)

        return prompt
    
    def build_web_prompt(self,question: str, search_result: WebSearchResult,)-> str:
        context = "\n\n".join(
                f"""
                Title: {result.title}
                URL: {result.url}
                Content:
                {result.content}
                """
                for result in search_result.results
        )

        prompt = f"""
                You are an AI assistant.

                Answer ONLY using the web search results below.

                If the answer cannot be found,
                say that the information is unavailable.

                ----------------------------------------

                Web Search Results

                {context}

                ----------------------------------------

                Question:

                {question}
                """

        return prompt