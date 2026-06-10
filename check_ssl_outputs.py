import json
from pathlib import Path
from collections import Counter

base = Path("experiments/synthetic_student_lab/outputs/ssl_v0_3_minimal")
judge_file = base / "judge_results.jsonl"

required_fields = {
    "run_id",
    "node_id",
    "condition",
    "student_persona",
    "rule_score",
    "rule_passed",
    "judge_score",
    "judge_passed",
    "matched_reasoning_points",
    "missing_reasoning_points",
    "conflict_type",
}

rows = []
with judge_file.open("r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if not line.strip():
            continue
        obj = json.loads(line)
        missing = required_fields - obj.keys()
        if missing:
            print(f"Line {i} missing fields: {missing}")
        rows.append(obj)

print("total rows:", len(rows))
print("conflict types:", Counter(r.get("conflict_type") for r in rows))
print("judge passed:", Counter(r.get("judge_passed") for r in rows))
print("rule passed:", Counter(r.get("rule_passed") for r in rows))