"""
Debug Printer

Formats and displays gateway execution information.

This module contains NO business logic.
It only presents data in a readable format.
"""

from src.schemas import (
    AnalysisResult,
    ExecutionPlan,
    RoutingDecision,
)


class DebugPrinter:

    WIDTH = 70

    @staticmethod
    def line(char: str = "─"):
        print(char * DebugPrinter.WIDTH)

    @staticmethod
    def title(text: str):
        print()
        print("═" * DebugPrinter.WIDTH)
        print(text.center(DebugPrinter.WIDTH))
        print("═" * DebugPrinter.WIDTH)

    @staticmethod
    def section(text: str):
        print()
        DebugPrinter.line()
        print(text)
        DebugPrinter.line()

    @staticmethod
    def field(name: str, value):
        print(f"{name:<25} {value}")

    @staticmethod
    def bullet(text: str):
        print(f"• {text}")

    @staticmethod
    def check(text: str):
        print(f"✓ {text}")

    @staticmethod
    def cross(text: str):
        print(f"✗ {text}")

    @staticmethod
    def print_analysis(analysis: AnalysisResult):

        DebugPrinter.section("Query Analysis")

        DebugPrinter.field("Prompt Length", f"{analysis.prompt_length} chars")
        DebugPrinter.field("Estimated Tokens", analysis.estimated_input_tokens)
        DebugPrinter.field("Sentences", analysis.sentence_count)
        DebugPrinter.field("Questions", analysis.question_count)

        print()

        DebugPrinter.field(
            "Reasoning",
            "YES" if analysis.requires_reasoning else "NO",
        )

        DebugPrinter.field(
            "Web Search",
            "YES" if analysis.requires_web_search else "NO",
        )

        DebugPrinter.field(
            "Enterprise RAG",
            "YES" if analysis.requires_rag else "NO",
        )

        print()

        if analysis.detected_topics:
            print("Topics:")
            for topic in analysis.detected_topics:
                DebugPrinter.bullet(topic)

        print()

        print("Analysis Trace:")

        for step in analysis.reasoning_trace:
            DebugPrinter.check(step)
    
    @staticmethod
    def print_execution_plan(plan: ExecutionPlan):

        DebugPrinter.section("Execution Plan")

        DebugPrinter.field("Priority", plan.priority)
        DebugPrinter.field("Complexity", plan.complexity_score)

        DebugPrinter.field(
            "Reasoning",
            "YES" if plan.requires_reasoning else "NO",
        )

        DebugPrinter.field(
            "Web Search",
            "YES" if plan.use_web_search else "NO",
        )

        DebugPrinter.field(
            "Enterprise RAG",
            "YES" if plan.use_rag else "NO",
        )

        print()

        DebugPrinter.field(
            "Input Tokens",
            plan.estimated_input_tokens,
        )

        DebugPrinter.field(
            "Output Tokens",
            plan.estimated_output_tokens,
        )

        DebugPrinter.field(
            "Estimated Cost",
            plan.estimated_cost,
        )

        DebugPrinter.field(
            "Expected Latency",
            f"{plan.estimated_latency_ms} ms",
        )

    @staticmethod
    def print_routing_summary(routing: RoutingDecision):

        DebugPrinter.section("Routing Summary")

        DebugPrinter.field("Selected Provider", routing.provider.value)
        DebugPrinter.field("Selected Model", routing.model_name.value)

        DebugPrinter.field(
            "Expected Latency",
            f"{routing.expected_latency_ms:.0f} ms",
        )

        DebugPrinter.field(
            "Routing Score",
            f"{routing.score:.2f}",
        )

        print()

        print("Score Breakdown")

        for name, value in routing.score_breakdown.items():
            DebugPrinter.field(
                name.title(),
                f"{value:.2f}",
            )

        print()

        print("Routing Reason")

        for reason in routing.routing_reason:
            DebugPrinter.check(reason)

        if routing.fallback_used:

            print()

            DebugPrinter.field(
                "Actual Provider",
                routing.actual_provider.value,
            )

            DebugPrinter.field(
                "Actual Model",
                routing.actual_model.value,
            )

    
    @staticmethod
    def print_cache_summary(cache_hit: bool):

        DebugPrinter.section("Semantic Cache")

        if cache_hit:
            DebugPrinter.check("Cache HIT")
            DebugPrinter.field("Response Source", "Semantic Cache")

        else:
            DebugPrinter.cross("Cache MISS")
            DebugPrinter.field("Response Source", "LLM Provider")
            
    
    @staticmethod
    def print_final_report(response):

        DebugPrinter.title("REQUEST COMPLETED")

        status = "SUCCESS"

        provider = (
            response.routing_decision.actual_provider
            if response.routing_decision.fallback_used
            else response.routing_decision.provider
        )

        model = (
            response.routing_decision.actual_model
            if response.routing_decision.fallback_used
            else response.routing_decision.model_name
        )

        DebugPrinter.field("Status", status)

        DebugPrinter.field(
            "Provider",
            provider.value if provider else "N/A",
        )

        DebugPrinter.field(
            "Model",
            model.value if model else "N/A",
        )

        DebugPrinter.field(
            "Fallback Used",
            "YES" if response.routing_decision.fallback_used else "NO",
        )

        DebugPrinter.field(
            "Cache Hit",
            "YES" if response.cache_hit else "NO",
        )

        DebugPrinter.field(
            "Latency",
            f"{response.latency_ms:.0f} ms",
        )

        if response.execution_plan:

            DebugPrinter.field(
                "Priority",
                response.execution_plan.priority.value,
            )

            DebugPrinter.field(
                "Estimated Cost",
                response.execution_plan.estimated_cost.value,
            )

    @staticmethod
    def print_execution_timeline(
        cache_hit: bool,
        fallback_used: bool,
        telemetry_updated: bool = True,
    ):

        DebugPrinter.section("Execution Timeline")

        DebugPrinter.check("Query Analyzed")
        DebugPrinter.check("Request Estimated")
        DebugPrinter.check("Execution Planned")

        if cache_hit:
            DebugPrinter.check("Semantic Cache Hit")
            DebugPrinter.check("Response Generated")
        else:
            DebugPrinter.check("Semantic Cache Miss")
            DebugPrinter.check("Provider Selected")

        if fallback_used:
            DebugPrinter.check("Provider Fallback Triggered")

        DebugPrinter.check("Response Generated")

        if telemetry_updated:
            DebugPrinter.check("Telemetry Updated")