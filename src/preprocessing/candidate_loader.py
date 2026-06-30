"""
candidate_loader.py

Streaming loader for the IndiaRun Candidate Discovery Challenge.

Responsibilities:
- Read candidates.jsonl one record at a time
- Validate required fields
- Skip malformed records
- Never load the whole dataset into memory
"""

import json
import logging
from pathlib import Path
from typing import Dict, Generator

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = [
    "candidate_id",
    "profile",
    "career_history",
    "skills",
    "redrob_signals"
]


def _is_valid(candidate: Dict) -> bool:
    """
    Validate that a candidate contains all required fields.
    """

    for field in REQUIRED_FIELDS:
        if field not in candidate:
            logger.warning(
                "Candidate %s skipped: missing '%s'",
                candidate.get("candidate_id", "UNKNOWN"),
                field,
            )
            return False

    return True


def load_candidates(file_path: str | Path) -> Generator[Dict, None, None]:
    """
    Stream candidates from a JSONL file.

    Parameters
    ----------
    file_path : str | Path

    Yields
    ------
    dict
        One validated candidate at a time.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")

    logger.info("Loading candidates from %s", file_path)

    with file_path.open("r", encoding="utf-8") as f:

        for line_number, line in enumerate(f, start=1):

            line = line.strip()

            if not line:
                continue

            try:
                candidate = json.loads(line)

            except json.JSONDecodeError as e:
                logger.error(
                    "Invalid JSON at line %d (%s)",
                    line_number,
                    e,
                )
                continue

            if not _is_valid(candidate):
                continue

            yield candidate

    logger.info("Candidate loading completed.")