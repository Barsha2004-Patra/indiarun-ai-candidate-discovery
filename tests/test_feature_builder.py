import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing.candidate_loader import load_candidates
from src.feature_engineering.feature_builder import build_candidate_features

candidate = next(load_candidates("data/candidates.jsonl"))

features = build_candidate_features(candidate)

print("\nGenerated Features:\n")

for key, value in features.items():
    print(f"{key}: {value}")