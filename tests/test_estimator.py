from src.planner.analyzer import QueryAnalyzer
from src.planner.estimator import RequestEstimator

analyzer = QueryAnalyzer()
estimator = RequestEstimator()

queries = [
    "What is Python?",
    "What's the latest AI news today?",
    "Compare Gemini Flash and Groq Llama.",
    "Calculate the total travel cost for 20 employees with hotel and flight options.",
    "Compare today's AI news with last week's announcements and recommend which LLM should be used."
]

for i, query in enumerate(queries, start=1):

    print("=" * 70)
    print(f"Test Case {i}")
    print(query)

    analysis = analyzer.analyze(query)
    estimate = estimator.estimate(analysis)

    print("\nAnalysis")
    print(analysis.model_dump_json(indent=2))

    print("\nEstimate")
    print(estimate.model_dump_json(indent=2))

    print()