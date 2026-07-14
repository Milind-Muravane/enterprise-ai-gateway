from src.planner.analyzer import QueryAnalyzer
from src.planner.estimator import RequestEstimator
from src.planner.planner import ExecutionPlanner
from src.router import AdaptiveRouter

query = (
    "Compare today's AI news with last week's announcements "
    "and recommend which LLM should be used."
)

analyzer = QueryAnalyzer()
estimator = RequestEstimator()
planner = ExecutionPlanner()
router = AdaptiveRouter()

analysis = analyzer.analyze(query)

estimate = estimator.estimate(analysis)

plan = planner.create_plan(
    analysis=analysis,
    estimate=estimate,
)

decision = router.select_provider(plan)

print("=" * 60)

print("Execution Plan")
print(plan.model_dump_json(indent=2))

print()

print("Routing Decision")
print(decision.model_dump_json(indent=2))