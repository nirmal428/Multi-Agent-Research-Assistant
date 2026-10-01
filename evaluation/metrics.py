def relevance_score(topic: str, answer: str) -> float:
    """
    Checks whether important words from the topic
    appear in the generated answer.
    """

    topic_words = set(topic.lower().split())
    answer_words = set(answer.lower().split())

    if not topic_words:
        return 0.0

    matched = topic_words.intersection(answer_words)

    return len(matched) / len(topic_words)


def completeness_score(answer: str) -> float:
    """
    Basic completeness check based on answer length.
    """

    words = len(answer.split())

    if words >= 300:
        return 1.0
    elif words >= 150:
        return 0.8
    elif words >= 50:
        return 0.6
    elif words > 0:
        return 0.3

    return 0.0


def source_usage_score(answer: str, sources) -> float:
    """
    Checks whether retrieved source information
    is actually present in the final answer.
    """

    if not sources:
        return 0.0

    matched = 0

    for source in sources:
        source_text = str(source).lower()

        # Check whether some source words appear in answer
        source_words = set(source_text.split())
        answer_words = set(answer.lower().split())

        if source_words.intersection(answer_words):
            matched += 1

    return matched / len(sources)


def calculate_final_score(
    relevance: float,
    completeness: float,
    source_usage: float
) -> float:

    return (
        relevance * 0.4
        + completeness * 0.3
        + source_usage * 0.3
    )