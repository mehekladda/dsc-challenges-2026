"""Week 0: Python Fundamentals Bootcamp — Beginner Practice Tasks."""

import csv
import json
from typing import Dict, List, Tuple, Any

def evaluate_attendance_status(attended: int, total: int) -> str:
    if total <= 0:
        return 'NO_SESSIONS'
    percent = (attended / total) * 100
    if percent >= 75:
        return 'ELIGIBLE'
    elif percent >= 65 and percent < 75:
        return 'WARNING'
    else:
        return 'SHORTAGE'

def safe_parse_float(raw_value: Any, default: float = 0.0) -> float:
    """Convert raw_value to float safely using try/except. Return default on failure."""
    try:
        return float(raw_value)
    except (ValueError, TypeError):
        return float(default)

def analyze_pod_scores(records: List[Tuple[str, str, float]]) -> Dict[str, Any]:
    unique_usns = {usn for usn, _, _ in records}
    high_scorers = [usn for usn, _, score in records if score >= 80]

    scores_by_pod: Dict[str, List[float]] = {}
    for _, pod_name, score in records:
        scores_by_pod.setdefault(pod_name, []).append(score)

    pod_averages = {
        pod_name: round(sum(scores) / len(scores), 2)
        for pod_name, scores in scores_by_pod.items()
    }

    return {
        "unique_student_count": len(unique_usns),
        "high_scorers": high_scorers,
        "pod_averages": pod_averages,
    }
    
def summarize_csv_to_json(csv_path: str, json_path: str) -> Dict[str, Any]:
    with open(csv_path, mode="r", newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    total_students = len(rows)
    branches = sorted({row["branch"].strip() for row in rows if row.get("branch")})

    scores = [float(row["score"]) for row in rows if row.get("score") not in (None, "")]
    average_score = round(sum(scores) / len(scores), 2) if scores else 0.0

    summary: Dict[str, Any] = {
        "total_students": total_students,
        "branches": branches,
        "average_score": average_score,
    }

    with open(json_path, mode="w", encoding="utf-8") as json_file:
        json.dump(summary, json_file, indent=2)

    return summary
class StudentRecord:
    """Tracks weekly evaluation scores for a single DSC recruit."""

    def __init__(self, usn: str, name: str):
        """Initialize record with uppercase USN, name, and empty scores list."""
        self.usn = usn.strip().upper()
        self.name = name.strip()
        self.scores: List[float] = []

    def add_score(self, score: float) -> None:
        """Append a score (must be between 0 and 100; raise ValueError otherwise)."""
        if not (0.0 <= score <= 100.0):
            raise ValueError("Score must be between 0 and 100")
        self.scores.append(float(score))

    def average(self) -> float:
        """Return average score rounded to 2 decimals, or 0.0 if no scores exist."""
        if not self.scores:
            return 0.0
        return round(sum(self.scores) / len(self.scores), 2)

    def is_passing(self, threshold: float = 50.0) -> bool:
        """Return True if average() >= threshold, else False."""
        return self.average() >= threshold