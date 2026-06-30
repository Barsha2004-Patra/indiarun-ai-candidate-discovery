import os

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from sentence_transformers import SentenceTransformer

from pathlib import Path
import argparse
import pandas as pd

from src.job_parser.job_parser import parse_job_description
from src.ranking.ranker import rank_candidates


def load_job_description(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_search_text(parsed_jd):
    """
    Convert parsed JD into a clean semantic search query.
    """

    skills = " ".join(parsed_jd["required_skills"])

    text = f"""
    {parsed_jd['title']}

    Required Skills:
    {skills}

    Minimum Experience:
    {parsed_jd['experience']} years
    """

    return text.strip()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data",
        default="data/embeddings.parquet",
        help="Embeddings parquet file",
    )

    parser.add_argument(
        "--jd",
        required=True,
        help="Job description txt file",
    )

    parser.add_argument(
        "--output",
        default="data/team_submission.csv",
        help="Submission csv",
    )

    args = parser.parse_args()

    print("Loading candidate dataset...")

    df = pd.read_parquet(args.data)

    print(f"Loaded {len(df):,} candidates")

    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Reading Job Description...")

    jd = load_job_description(args.jd)

    print("Parsing Job Description...")

    parsed_jd = parse_job_description(jd)

    print(parsed_jd)

    search_text = build_search_text(parsed_jd)

    print("Embedding Parsed Job Description...")

    jd_embedding = model.encode(
        search_text,
        normalize_embeddings=True,
    )

    print("Ranking candidates...")

    ranked = rank_candidates(
        df,
        jd_embedding,
        parsed_jd,
    )

    submission = ranked[
        [
            "rank",
            "candidate_id",
            "score",
            "reasoning",
        ]
    ]

    Path(args.output).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    submission.to_csv(
        args.output,
        index=False,
    )

    print()
    print("Done!")
    print(f"Top 100 saved to {args.output}")


if __name__ == "__main__":
    main()