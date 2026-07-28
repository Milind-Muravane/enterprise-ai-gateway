from src.gateway import Gateway


gateway = Gateway()

questions = [

    # ----------------------------
    # Simple Question
    # ----------------------------
    "Hie Namaste!!! how's your day?",

    # ----------------------------
    # Enterprise RAG
    # ----------------------------
    "Does our internal travel handbook permit reimbursement for overnight accommodation booked through third-party websites?",
    # ----------------------------
    # Web Search
    # ----------------------------
    "What significant cybersecurity incidents were reported worldwide in the last 48 hours?",

    # ----------------------------
    # Hybrid Retrieval
    # ----------------------------
    "Our procurement policy explains laptop purchasing rules. Are there any newly announced import regulations affecting laptop purchases in India?",

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

    print("\n--- DEBUG ---")
    print("Provider:", response.provider)
    print("Cache Hit:", response.cache_hit)
    print("Routing Decision:", response.routing_decision)
    print("--------------")

    print("Planned Provider:", response.routing_decision.provider)
    
    print()

    print("Actual Provider:", response.routing_decision.actual_provider)
   
    print()
   
    print("Fallback Used:", response.routing_decision.fallback_used)
    
    print()