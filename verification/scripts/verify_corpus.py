"""Validate OmniView development source cards and their internal source links."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


REPO = Path(__file__).resolve().parents[2]
CORPUS = REPO / "development" / "corpus"


def main() -> int:
    schema = json.loads((CORPUS / "source-card.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    case_ids: set[str] = set()
    cards = 0

    for path in sorted(CORPUS.glob("*.json")):
        if path.name == "source-card.schema.json":
            continue
        cards += 1
        try:
            card = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: unreadable JSON: {exc}")
            continue

        for issue in sorted(validator.iter_errors(card), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in issue.path) or "<root>"
            errors.append(f"{path.name}:{location}: {issue.message}")

        case_id = card.get("caseId")
        if case_id in case_ids:
            errors.append(f"{path.name}: duplicate caseId {case_id}")
        if isinstance(case_id, str):
            case_ids.add(case_id)

        source_ids = {
            source.get("id")
            for source in card.get("sources", [])
            if isinstance(source, dict)
        }
        for index, claim in enumerate(card.get("visibleGroundTruth", [])):
            if not isinstance(claim, dict):
                continue
            missing = set(claim.get("sourceIds", [])) - source_ids
            if missing:
                errors.append(
                    f"{path.name}:visibleGroundTruth.{index}: unknown source ids "
                    + ", ".join(sorted(missing))
                )

    if errors:
        print(json.dumps({"check": "corpus", "status": "FAIL", "errors": errors}, indent=2))
        return 1

    print(
        json.dumps(
            {
                "check": "corpus",
                "status": "PASS",
                "cards": cards,
                "schema": "draft-2020-12",
                "claim_boundary": (
                    "Schema and internal-link validation only; domain correctness "
                    "remains bounded by each card's sources and review state."
                ),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

