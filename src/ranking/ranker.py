import numpy as np

from src.scoring.scorer import calculate_final_score
from src.reasoning.reason_generator import generate_reason


def cosine_similarity(a, b):
    """
    Compute cosine similarity between two embedding vectors.
    """
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def rank_candidates(
    df,
    job_embedding,
    parsed_jd,
    top_k=100,
):

    scores = []
    reasons = []

    for _, candidate in df.iterrows():

        semantic_score = cosine_similarity(
            job_embedding,
            candidate["embedding"]
        )

        final_score = calculate_final_score(
            candidate,
            semantic_score,
            parsed_jd
        )

        reason = generate_reason(candidate)

        scores.append(final_score)
        reasons.append(reason)

    ranked = df.copy()

    ranked["score"] = scores
    ranked["reasoning"] = reasons

    ranked = ranked.sort_values(
        by="score",
        ascending=False
    )

    ranked = ranked.reset_index(drop=True)
    ranked["rank"] = ranked.index + 1

    return ranked.head(top_k)