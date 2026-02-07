"""
Difficulty adaptation module.

Updates problem difficulty based on user feedback
using simple rule-based logic.
"""

def update_difficulty(old: int, feedback: str) -> int:
    """
    Update difficulty score based on user feedback.

    Args:
        old: Current difficulty (1-10).
        feedback: 'too_easy', 'too_hard', or 'just_right'.

    Returns:
        Updated difficulty score between 1 and 10.

    Raises:
        ValueError: If feedback is invalid.
    """

    if feedback == "too_easy":
        return min(old + 1, 10)

    if feedback == "too_hard":
        return max(old - 1, 1)

    if feedback == "just_right":
        return old

    raise ValueError("Invalid feedback value")
