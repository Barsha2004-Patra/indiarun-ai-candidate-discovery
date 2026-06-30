"""
Offline preprocessing pipeline.

Reads all candidates from candidates.jsonl,
extracts structured features,
and saves them as a Parquet file for fast loading
during online ranking.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pathlib import Path
import pandas as pd

from src.preprocessing.candidate_loader import load_candidates
from src.feature_engineering.feature_builder import build_candidate_features


def build_feature_dataset(input_file: str, output_file: str):
    features = []

    print("Loading candidates...")

    for i, candidate in enumerate(load_candidates(input_file), start=1):
        features.append(build_candidate_features(candidate))

        if i % 5000 == 0:
            print(f"Processed {i:,} candidates")

    print("Creating DataFrame...")
    df = pd.DataFrame(features)

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    print("Saving Parquet...")
    df.to_parquet(output_file, index=False)

    print(f"\nDone!")
    print(f"Candidates processed : {len(df):,}")
    print(f"Output file          : {output_file}")


if __name__ == "__main__":
    build_feature_dataset(
        "data/candidates.jsonl",
        "data/features.parquet"
    )