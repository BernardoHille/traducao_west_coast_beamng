"""Update rows of docs/localization/LOCALIZATION_MASTER.csv from a JSON list (Phase 6).

    python tools/production/matrix_update.py updates.json

updates.json: [{"id": ..., "status"?: ..., "ptbr_text"?: ..., "wcusa_usage"?: ..., "note"?: "prepended to notes"},
               {"new": {...full row...}}]
Only declared fields change; new rows must carry every column. Statuses follow LOCALIZATION_RULES.md section 18.
"""
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
P = REPO / "docs/localization/LOCALIZATION_MASTER.csv"
STATUSES = {"inventory", "needs_context", "rule_defined", "needs_implementation", "approved_rule", "preserve_original",
            "implemented", "qa_passed"}


def main(path):
    ups = json.loads(Path(path).read_text(encoding="utf8"))
    rows = list(csv.DictReader(open(P, encoding="utf-8")))
    fields = list(rows[0].keys())
    by = {r["id"]: r for r in rows}
    for u in ups:
        if "new" in u:
            r = {k: "" for k in fields}
            r.update(u["new"])
            if r["id"] in by:
                raise SystemExit(f"{r['id']} exists")
            assert r["status"] in STATUSES, r["status"]
            rows.append(r)
            by[r["id"]] = r
            continue
        r = by[u["id"]]
        if "status" in u:
            assert u["status"] in STATUSES, u["status"]
            r["status"] = u["status"]
        for k in ("ptbr_text", "wcusa_usage", "localization_type", "original_text"):
            if k in u:
                r[k] = u[k]
        if u.get("note"):
            r["notes"] = (u["note"] + " " + r["notes"]).strip()
    with open(P, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(ups)} updates -> {P.relative_to(REPO)}")


if __name__ == "__main__":
    main(sys.argv[1])
