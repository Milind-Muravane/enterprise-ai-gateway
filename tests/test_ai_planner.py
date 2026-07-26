from src.planner.ai_planner import AIPlanner


planner = AIPlanner()

question = (
    "According to our travel policy, "
    "can I travel Business Class to Germany "
    "and are there any recent visa changes?"
)

plan = planner.plan(question)

print("\nExecution Plan")
print("-" * 50)
print(plan)