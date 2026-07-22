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

        print("="* 80)
        print("RAG Context")
        print("="* 80)
        print(context)
        print("="* 80)

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

                You MUST answer ONLY using the web search results below.

                Do NOT say you don't have internet access.

                Do NOT mention knowledge cutoff.

                Treat the search results as the latest available information.

                If the answer is not contained in the search results,
                respond with:
                "I could not find this information in the retrieved web results."

                ----------------------------------------
                WEB SEARCH RESULTS

                {context}

                ----------------------------------------

                QUESTION

                {question}

                ----------------------------------------

                Provide a concise answer.
                """
        print("=" * 80)
        print("WEB PROMPT")
        print("=" * 80)
        print(prompt)
        print("=" * 80)

        return prompt