"""
Hybrid Retriever
Combines enterprise RAG and live web search.
"""

from src.rag.retriever import DocumentRetriever
from src.websearch.tavily import TavilySearch

from src.schemas import (
    ExecutionPlan,
    HybridContext,
)


class HybridRetriever:

    def __init__(self):

        self.rag = DocumentRetriever()
        self.web = TavilySearch()

    def retrieve(
        self,
        question: str,
        plan: ExecutionPlan,
    ) -> HybridContext:

        context = HybridContext()


        # Enterprise RAG
        if plan.use_rag:

            rag_results = self.rag.retrieve(question)

            enterprise_text = "\n\n".join(
                chunk.text
                for chunk in rag_results.chunks
            )

            enterprise_sources = list(
                {
                    chunk.source
                    for chunk in rag_results.chunks
                }
            )

            context.enterprise_context = enterprise_text
            context.enterprise_sources = enterprise_sources

        # Live Web Search
        if plan.use_web_search:

            web_results = self.web.search(question)

            web_text = "\n\n".join(
                result.content
                for result in web_results.results
            )

            web_sources = [
                result.url
                for result in web_results.results
            ]

            context.web_context = web_text
            context.web_sources = web_sources

        return context