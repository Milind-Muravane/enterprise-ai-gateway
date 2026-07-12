from src.planner.analyzer import QueryAnalyzer

analyzer = QueryAnalyzer()

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
    print(f"Query: {query}\n")

    result = analyzer.analyze(query)

    print(result.model_dump_json(indent=2))
    print()