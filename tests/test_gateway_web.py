from src.gateway import Gateway

gateway = Gateway()

response = gateway.process(
    ""
)

print()

print("=" * 80)

print(response.answer)

print()

print(response.routing_decision)