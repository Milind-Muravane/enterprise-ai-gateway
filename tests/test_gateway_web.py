from src.gateway import Gateway

gateway = Gateway()

response = gateway.process(
    "Latest NVIDIA Blackwell GPU announcements"
)

print()

print("=" * 80)

print(response.answer)

print()

print(response.routing_decision)