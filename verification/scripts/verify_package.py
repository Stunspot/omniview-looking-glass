"""Verify OmniView package closure, parity, and publishable boundaries."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NAME = "omniview-looking-glass"
APPROVED_DESCRIPTION = "🌀 Evidence-grounded images across place and time."
VERSION = "0.1.0"
PLUGIN = REPO / "plugins" / NAME
CANONICAL = PLUGIN / "skills" / NAME
CLAUDE = REPO / "dist" / "claude-code" / NAME
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml"}
RUNTIME_REFERENCE = re.compile(
    r"(?<![\w.-])((?:references|assets|evals)/[A-Za-z0-9][A-Za-z0-9._/-]*)"
)
PRIVATE_MARKERS = (
    "c:\\users\\",
    "c:/users/",
    "e:\\indranet\\",
    "e:/indranet/",
    "e:\\github\\",
    "e:/github/",
    "\\.work\\gl4ss",
    "/.work/gl4ss",
)
PUBLISHABLE = (
    REPO / ".agents",
    REPO / "plugins",
    REPO / "dist",
    REPO / "docs",
    REPO / "README.md",
    REPO / "release",
)


def load_json(path: Path, errors: list[str], label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label} is unreadable JSON: {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{label} must contain a JSON object: {path}")
        return {}
    return value


def iter_files(root: Path):
    if root.is_file():
        yield root
    elif root.is_dir():
        yield from (path for path in sorted(root.rglob("*")) if path.is_file())


def portable_files(root: Path) -> dict[str, bytes]:
    result = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if "agents" in relative.parts:
            continue
        result[relative.as_posix()] = path.read_bytes()
    return result


def validate_frontmatter(errors: list[str]) -> None:
    skill = CANONICAL / "SKILL.md"
    try:
        lines = skill.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"canonical SKILL.md is unreadable: {exc}")
        return
    if not lines or lines[0].strip() != "---":
        errors.append("SKILL.md lacks opening YAML frontmatter")
        return
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        errors.append("SKILL.md lacks closing YAML frontmatter")
        return
    fields = {}
    for line in lines[1:end]:
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip("\"'")
    if fields.get("name") != NAME:
        errors.append(f"SKILL.md frontmatter name must be {NAME}")
    description = fields.get("description", "")
    if description != APPROVED_DESCRIPTION:
        errors.append(
            "SKILL.md description must match the approved injection text exactly"
        )


def validate_runtime_references(errors: list[str]) -> None:
    for path in iter_files(CANONICAL):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"cannot read runtime text {path}: {exc}")
            continue
        for raw in RUNTIME_REFERENCE.findall(text):
            target = (CANONICAL / raw).resolve()
            try:
                target.relative_to(CANONICAL.resolve())
            except ValueError:
                errors.append(f"runtime reference escapes skill root: {raw}")
                continue
            if not target.is_file():
                errors.append(
                    f"missing runtime reference from {path.relative_to(CANONICAL)}: {raw}"
                )


def validate_manifests(errors: list[str]) -> None:
    marketplace = load_json(
        REPO / ".agents" / "plugins" / "marketplace.json",
        errors,
        "marketplace manifest",
    )
    entries = marketplace.get("plugins", [])
    entry = next(
        (
            item
            for item in entries
            if isinstance(item, dict) and item.get("name") == NAME
        ),
        None,
    )
    if entry is None:
        errors.append("marketplace lacks the OmniView plugin entry")
    else:
        source = entry.get("source", {})
        if source.get("path") != "./plugins/" + NAME:
            errors.append("marketplace source path is not repository-relative")
        if entry.get("policy", {}).get("installation") != "AVAILABLE":
            errors.append("marketplace installation policy must be AVAILABLE")

    plugin = load_json(
        PLUGIN / ".codex-plugin" / "plugin.json",
        errors,
        "plugin manifest",
    )
    if plugin.get("name") != NAME:
        errors.append("plugin manifest name mismatch")
    if plugin.get("version") != VERSION:
        errors.append("plugin manifest version mismatch")
    if plugin.get("skills") != "./skills/":
        errors.append("plugin skills path must be ./skills/")

    for root, label in ((CANONICAL, "canonical"), (CLAUDE, "Claude")):
        package = load_json(
            root / "package-manifest.yaml",
            errors,
            f"{label} package manifest",
        )
        if package.get("name") != NAME or package.get("version") != VERSION:
            errors.append(f"{label} package manifest identity/version mismatch")
        eval_manifest = load_json(
            root / "evals" / "eval-manifest.yaml",
            errors,
            f"{label} eval manifest",
        )
        if eval_manifest.get("package_version") != VERSION:
            errors.append(f"{label} eval version mismatch")
        suite = load_json(
            root / "evals" / "omniview-cases.yaml",
            errors,
            f"{label} eval suite",
        )
        if suite.get("package_version") != VERSION:
            errors.append(f"{label} eval suite version mismatch")

        dimensions = set(eval_manifest.get("indispensable_dimensions", []))
        cases = suite.get("cases", [])
        ids = [
            case.get("id")
            for case in cases
            if isinstance(case, dict)
        ]
        if len(ids) != len(set(ids)):
            errors.append(f"{label} eval suite has duplicate case ids")
        for case in cases:
            if not isinstance(case, dict):
                errors.append(f"{label} eval suite contains a non-object case")
                continue
            unknown = set(case.get("dimensions", [])) - dimensions
            if unknown:
                errors.append(
                    f"{label} eval case {case.get('id')} uses unknown dimensions: "
                    + ", ".join(sorted(unknown))
                )

    openai = CANONICAL / "agents" / "openai.yaml"
    try:
        openai_text = openai.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"agents/openai.yaml is unreadable: {exc}")
    else:
        for key in ("display_name", "short_description", "default_prompt"):
            if not re.search(rf"^\s*{key}:\s*[\"'].+[\"']\s*$", openai_text, re.MULTILINE):
                errors.append(f"agents/openai.yaml lacks quoted {key}")
        if "$" + NAME not in openai_text:
            errors.append("agents/openai.yaml default prompt does not invoke the skill")


def validate_parity(errors: list[str]) -> None:
    if not (CLAUDE / "SKILL.md").is_file():
        errors.append("Claude distribution lacks root SKILL.md")
        return
    expected = portable_files(CANONICAL)
    actual = portable_files(CLAUDE)
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed = sorted(
        name for name in set(expected) & set(actual) if expected[name] != actual[name]
    )
    if missing:
        errors.append("Claude distribution is missing: " + ", ".join(missing))
    if extra:
        errors.append("Claude distribution has extras: " + ", ".join(extra))
    if changed:
        errors.append("Claude distribution differs: " + ", ".join(changed))


def validate_publishable_boundaries(errors: list[str]) -> None:
    for root in PUBLISHABLE:
        if not root.exists():
            continue
        for path in iter_files(root):
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                errors.append(f"cannot inspect publishable text {path}: {exc}")
                continue
            lowered = text.lower()
            for marker in PRIVATE_MARKERS:
                if marker in lowered:
                    errors.append(
                        "private path marker in "
                        + path.relative_to(REPO).as_posix()
                        + ": "
                        + marker
                    )
            if "[todo" in lowered or "todo:" in lowered:
                errors.append(
                    "unfinished scaffold marker in "
                    + path.relative_to(REPO).as_posix()
                )

    notice = (CANONICAL / "NOTICE.md").read_text(encoding="utf-8").lower()
    required = (
        "collaborative dynamics",
        "stunspot and nova",
        "pliny the liberator",
        "not an official",
        "generates its own output",
    )
    for phrase in required:
        if phrase not in notice:
            errors.append("NOTICE.md lacks required attribution language: " + phrase)


def main() -> int:
    errors: list[str] = []
    for directory in ("references", "assets", "evals"):
        target = CANONICAL / directory
        if not target.is_dir() or not any(target.iterdir()):
            errors.append(f"canonical runtime directory is missing or empty: {target}")

    validate_frontmatter(errors)
    validate_runtime_references(errors)
    validate_manifests(errors)
    validate_parity(errors)
    validate_publishable_boundaries(errors)

    if errors:
        print(json.dumps({"check": "package", "status": "FAIL", "errors": errors}, indent=2))
        return 1

    print(
        json.dumps(
            {
                "check": "package",
                "status": "PASS",
                "version": VERSION,
                "portable_files": len(portable_files(CANONICAL)),
                "claude_parity": True,
                "claim_boundary": (
                    "Static package closure and byte parity only; no installation, "
                    "discovery, invocation, image-tool, or live-host claim."
                ),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

