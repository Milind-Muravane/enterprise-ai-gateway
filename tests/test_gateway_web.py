from src.gateway import Gateway

gateway = Gateway()

response = gateway.process(
    "What are today's latest AI news?"
)

print()

print("=" * 80)

print(response.answer)

print()

print(response.routing_decision)