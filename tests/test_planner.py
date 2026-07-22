from src.planner.analyzer import QueryAnalyzer
from src.planner.estimator import RequestEstimator
from src.planner.planner import ExecutionPlanner

query = (
    "Compare today's AI news with last week's announcements "
    "and recommend which LLM should be used."
)

analyzer = QueryAnalyzer()
estimator = RequestEstimator()
planner = ExecutionPlanner()

analysis = analyzer.analyze(query)

estimate = estimator.estimate(analysis)

plan = planner.create_plan(
    analysis=analysis,
    estimate=estimate,
)

print(plan.model_dump_json(indent=2))