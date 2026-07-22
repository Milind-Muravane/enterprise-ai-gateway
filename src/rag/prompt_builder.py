"""
Prompt Builder

Builds an augmented prompt using
retrieved RAG context.
"""

from src.schemas import RetrievalResult

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