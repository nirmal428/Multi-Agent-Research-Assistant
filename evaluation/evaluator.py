import json

from metrics import (
    relevance_score,
    completeness_score,
    source_usage_score,
    calculate_final_score
)


def evaluate_result(topic: str, result: dict):

    # Get final answer from pipeline
    answer = result.get("answer", "")

    # Get retrieved sources
    sources = result.get("sources", [])

    # -------------------------
    # Calculate metrics
    # -------------------------

    relevance = relevance_score(
        topic,
        answer
    )

    completeness = completeness_score(
        answer
    )

    source_usage = source_usage_score(
        answer,
        sources
    )

    final_score = calculate_final_score(
        relevance,
        completeness,
        source_usage
    )

    evaluation = {
        "topic": topic,
        "metrics": {
            "relevance": round(relevance, 3),
            "completeness": round(completeness, 3),
            "source_usage": round(source_usage, 3),
            "final_score": round(final_score, 3)
        }
    }

    return evaluation


def save_evaluation(evaluation):

    with open(
        "evaluation/results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            evaluation,
            file,
            indent=4,
            ensure_ascii=False
        )