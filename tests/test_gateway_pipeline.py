from src.gateway import Gateway


gateway = Gateway()

questions = [

    # ----------------------------
    # Simple Question
    # ----------------------------
    "Hello!",

    # ----------------------------
    # Enterprise RAG
    # ----------------------------
    "Who is allowed to travel in Business Class according to company policy?",

    # ----------------------------
    # Web Search
    # ----------------------------
    "Latest AI news today",

    # ----------------------------
    # Hybrid Retrieval
    # ----------------------------
    "According to our travel policy, can I travel Business Class to Germany and are there any recent visa changes?",

]

for i, question in enumerate(questions, start=1):

    print("\n")
    print("=" * 90)
    print(f"TEST {i}")
    print("=" * 90)

    print()
    print("Question:")
    print(question)

    print("\nProcessing...\n")

    response = gateway.process(question)

    print("=" * 90)

    print("Provider")
    print(response.provider)

    print()

    print("Model")
    print(response.model_name)

    print()

    print("Cache Hit")
    print(response.cache_hit)

    print()

    print("Latency")
    print(response.latency_ms)

    print()

    print("Execution Plan")
    print(response.execution_plan)

    print()

    print("Routing Decision")
    print(response.routing_decision)

    print()

    print("Answer")
    print(response.answer)

    print()