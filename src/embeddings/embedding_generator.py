"""
Generate semantic embeddings for all candidates.

Reads features.parquet
Creates an enriched text document for every candidate
Generates embeddings in batches
Saves embeddings.parquet
"""

from sentence_transformers import SentenceTransformer

from pathlib import Path
import pandas as pd
from tqdm import tqdm


MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 256


def build_document(row):
    return f"""
Candidate Profile

Current Title:
{row.current_title}

Industry:
{row.current_industry}

Experience:
{row.years_of_experience} years

Profile:
{row.profile_text}

Career:
{row.career_text}

Skills:
{row.skills_text}

Profile Completeness:
{row.profile_completeness}

GitHub Activity:
{row.github_activity_score}

Recruiter Response Rate:
{row.recruiter_response_rate}

Interview Completion:
{row.interview_completion_rate}

Offer Acceptance:
{row.offer_acceptance_rate}
"""


def generate_embeddings():

    print("Loading feature dataset...")

    df = pd.read_parquet("data/features.parquet")

    print(f"Loaded {len(df):,} candidates")

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Building candidate documents...")

    documents = [build_document(row) for row in df.itertuples()]

    print("Generating embeddings...")

    embeddings = model.encode(
        documents,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    df["embedding"] = list(embeddings)

    output = Path("data/embeddings.parquet")

    df.to_parquet(output, index=False)

    print()

    print("Done!")

    print(f"Saved to {output}")


if __name__ == "__main__":
    generate_embeddings()