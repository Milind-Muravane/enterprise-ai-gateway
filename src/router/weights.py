"""
Routing Weights

Defines the importance of each capability
when calculating the final provider score.
"""

ROUTING_WEIGHTS = {
    # Ability to solve complex problems
    "reasoning" : 3.0,
    # Performance
    "performance" : 2.5,
    # Lower API cost
    "cost" : 2.0,
    # Ability to handle long context
    "context" : 2.5,
    # Ability to answer current events
    "freshness" : 2.5,
}