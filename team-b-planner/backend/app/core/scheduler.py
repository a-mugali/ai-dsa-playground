import heapq
from typing import Dict, List


def generate_plan(
    problems: List[Dict],
    time_limit: int,
    min_d: int,
    max_d: int,
) -> List[Dict]:
    """
    Generate a daily practice plan using greedy + heap scheduling.

    Args:
        problems: List of problem dictionaries.
        time_limit: Daily time budget in minutes.
        min_d: Minimum difficulty.
        max_d: Maximum difficulty.

    Returns:
        List of selected problems.

    Raises:
        ValueError: If time_limit is invalid.
    """

    if time_limit <= 0:
        raise ValueError("Time limit must be positive")

    heap = []
    topic_count = {}

    target = (min_d + max_d) / 2

    # Build priority queue
    for p in problems:

        if min_d <= p["difficulty"] <= max_d:

            topic = p["topics"][0]

            penalty = topic_count.get(topic, 0)

            score = abs(p["difficulty"] - target) + penalty

            heapq.heappush(heap, (score, p["id"], p))

    plan = []
    total_time = 0

    # Greedy selection
    while heap and total_time < time_limit:

        _, _, problem = heapq.heappop(heap)

        duration = problem["duration"]

        if total_time + duration <= time_limit:

            plan.append(problem)
            total_time += duration

            # Update topic balance
            for t in problem["topics"]:
                topic_count[t] = topic_count.get(t, 0) + 1

    return plan
