from src.gateway import Gateway

gateway = Gateway()

questions = [

    # ============================================================
    # FAST
    # ============================================================
    "What is one interesting fact about Saturn?",

    # ============================================================
    # RAG
    # ============================================================
    "According to our employee handbook, are meals during official business travel reimbursable, and are there any spending limits?",

    # ============================================================
    # WEB
    # ============================================================
    "What are the latest developments in quantum computing announced this week?",

    # ============================================================
    # HYBRID (RAG + WEB + REASONING)
    # ============================================================
    "Compare our company's international travel policy with the latest Schengen visa requirements for Indian citizens travelling for business.",

    # ============================================================
    # REASONING
    # ============================================================
    "Recommend improvements to our remote work policy based on the latest cybersecurity best practices.",

    # ============================================================
    # STRESS TEST
    # ============================================================
    "An employee is travelling from Bengaluru to Germany for a two-week client engagement. Using our company travel policy together with the latest visa requirements, baggage regulations and reimbursement rules, prepare a complete travel plan and justify every recommendation."
]


for i, question in enumerate(questions, start=1):

    print("\n")
    print("=" * 100)
    print(f"TEST {i}")
    print("=" * 100)

    print("\nQuestion:")
    print(question)

    print("\nProcessing...\n")

    response = gateway.process(question)

    print("=" * 100)

    print("Provider:")
    print(response.provider)

    print("\nModel:")
    print(response.model_name)

    print("\nCache Hit:")
    print(response.cache_hit)

    print("\nLatency (ms):")
    print(response.latency_ms)

    print("\nExecution Plan:")
    print(response.execution_plan)

    print("\nRouting Decision:")
    print(response.routing_decision)

    print("\nAnswer:")
    print(response.answer)

    print("\n" + "-" * 100)
    print("DEBUG INFORMATION")
    print("-" * 100)

    print(f"Provider      : {response.provider}")
    print(f"Model         : {response.model_name}")
    print(f"Cache Hit     : {response.cache_hit}")
    print(f"Latency (ms)  : {response.latency_ms}")

    if response.cache_hit:
        print("\nPipeline:")
        print("User")
        print("  ↓")
        print("Semantic Cache")
        print("  ↓")
        print("Returned Cached Response")

    elif response.routing_decision is not None:

        rd = response.routing_decision

        print("\nPipeline:")
        print("User")
        print("  ↓")
        print("Semantic Cache (MISS)")
        print("  ↓")
        print("Planner")
        print("  ↓")
        print("Router")
        print("  ↓")
        print(f"{rd.provider.value}")
        print("  ↓")
        print("Response")

        print("\nPlanned Provider:")
        print(rd.provider)

        print("\nActual Provider:")
        print(rd.actual_provider)

        print("\nFallback Used:")
        print(rd.fallback_used)

        print("\nExpected Latency:")
        print(rd.expected_latency_ms)

        print("\nRouting Score:")
        print(rd.score)

        print("\nScore Breakdown:")
        for key, value in rd.score_breakdown.items():
            print(f"  {key:15}: {value:.2f}")

        print("\nRouting Reason:")
        for reason in rd.routing_reason:
            print(f"  • {reason}")

    else:
        print("\nRouting Decision: None")

    print("\n")