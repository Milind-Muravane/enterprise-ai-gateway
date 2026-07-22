from src.gateway import Gateway

gateway = Gateway()

response = gateway.process(
    "Compare today's AI news with last week's announcements."
)

print("=" * 60)

print("Answer")
print(response.answer)

print()

print("Execution Plan")
print(response.execution_plan.model_dump_json(indent=2))

print()

print("Routing Decision")
print(response.routing_decision.model_dump_json(indent=2))