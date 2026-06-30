import sys
from pathlib import Path
import logging

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing.candidate_loader import load_candidates

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

count = 0

for candidate in load_candidates("data/candidates.jsonl"):
    count += 1

    if count <= 3:
        print(candidate["candidate_id"])

print(f"\nLoaded {count} candidates successfully.")