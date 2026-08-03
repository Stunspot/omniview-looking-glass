"""Capture and verify OmniView behavioral-evidence custody, using only stdlib.

This tool deliberately verifies provenance and byte integrity, not prompt quality.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "plugins" / "omniview-looking-glass" / "skills" / "omniview-looking-glass"
EVAL_SUITE = PACKAGE / "evals" / "omniview-cases.yaml"
EVAL_MANIFEST = PACKAGE / "evals" / "eval-manifest.yaml"
CORPUS = REPO / "development" / "corpus"
FORMAT = "omniview-behavioral-evidence/v2"
HEADER = re.compile(
    r"^READ_OK; TURN=([^;\r\n]+); HEAD=([0-9a-f]{40}); FILE_HASHES=(.+)$"
)
HASH_ITEM = re.compile(r"^([A-Za-z0-9._-]+)=([0-9a-f]{64})$")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"unreadable JSON: {path}: {exc}") from exc


def git_head() -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True, encoding="utf-8",
    )
    head = result.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError("git did not return a full HEAD hash")
    return head


def git_file_bytes(commit: str, repo_relative_path: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{commit}:{repo_relative_path}"],
        check=False,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"cannot read {repo_relative_path} at {commit}: {detail}")
    return result.stdout


def ensure_snapshot_clean() -> None:
    paths = [rel(PACKAGE), rel(CORPUS)]
    result = subprocess.run(
        ["git", "-C", str(REPO), "status", "--porcelain", "--untracked-files=all", "--", *paths],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.stdout.strip():
        raise ValueError("canonical package or corpus differs from HEAD; commit the runtime snapshot before prepare")


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def write_identical(path: Path, payload: bytes) -> None:
    if path.exists():
        current = path.read_bytes()
        if current != payload:
            raise ValueError(f"refusing overwrite with different bytes: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def package_files() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(PACKAGE.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            result[path.relative_to(PACKAGE).as_posix()] = {"sha256": digest(data), "bytes": len(data)}
    if len(result) != 13:
        raise ValueError(f"expected 13 canonical package files, found {len(result)}")
    return result


def corpus_files() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not CORPUS.is_dir():
        raise ValueError(f"development corpus is missing: {CORPUS}")
    for path in sorted(CORPUS.glob("*.json")):
        data = path.read_bytes()
        result[rel(path)] = {"sha256": digest(data), "bytes": len(data)}
    return result


def allowed_runtime(case_id: str) -> list[str]:
    files = {
        "OV-NEMO-PROMPT-001": ["SKILL.md", "references/grounding-and-precision.md", "references/wormhole-optics.md", "references/render-language.md"],
        "OV-PRECISION-NAP-001": ["SKILL.md", "references/grounding-and-precision.md", "references/wormhole-optics.md", "references/render-language.md"],
        "OV-URUK-DENSE-001": ["SKILL.md", "references/grounding-and-precision.md", "references/render-language.md"],
        "OV-PRIPYAT-COMPARE-001": ["SKILL.md", "references/grounding-and-precision.md", "references/comparison-and-traversal.md", "references/render-language.md"],
        "OV-PATAGONIA-SUPPORT-001": ["SKILL.md", "references/grounding-and-precision.md", "references/wormhole-optics.md", "references/render-language.md"],
        "OV-SAHARA-HUMID-001": ["SKILL.md", "references/grounding-and-precision.md", "references/render-language.md"],
        "OV-FUTURE-SCENARIO-001": ["SKILL.md", "references/grounding-and-precision.md", "references/render-language.md"],
        "OV-APOLLO-EXACT-001": ["SKILL.md", "references/grounding-and-precision.md", "references/wormhole-optics.md", "references/render-language.md"],
        "OV-RENDER-DEGRADE-001": ["SKILL.md", "references/wormhole-optics.md", "references/render-language.md"],
        "OV-TRAVERSE-AUTHORITY-001": ["SKILL.md", "references/grounding-and-precision.md", "references/wormhole-optics.md", "references/comparison-and-traversal.md", "references/render-language.md"],
        "OV-STYLE-MEDIUM-001": ["SKILL.md", "references/grounding-and-precision.md", "references/render-language.md"],
        "OV-GEOGRAPHY-CCTV-001": ["SKILL.md", "references/grounding-and-precision.md"],
        "OV-IDENTITY-001": ["SKILL.md", "NOTICE.md"],
    }
    try:
        return files[case_id]
    except KeyError as exc:
        raise ValueError(f"no allowed-runtime map for case: {case_id}") from exc


def load_cases() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    suite = read_json(EVAL_SUITE)
    cases = suite.get("cases")
    if not isinstance(cases, list) or len(cases) != 13:
        raise ValueError("canonical eval suite must contain exactly 13 cases")
    if any(not isinstance(item, dict) or not isinstance(item.get("id"), str) for item in cases):
        raise ValueError("canonical eval suite contains an invalid case")
    ids = [item["id"] for item in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("canonical eval suite has duplicate case IDs")
    return suite, cases


def run_path(run_dir: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"evidence paths must be run-relative: {value}")
    return run_dir / path


def cmd_prepare(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    ensure_snapshot_clean()
    suite, cases = load_cases()
    runtime = package_files()
    prepared_at = utc_now()
    runtime_commit = git_head()
    isolation_contract = {
        "episode_mode": "one fresh turn per selected case on a reused collaboration agent",
        "freshness_state": "attributed harness assertion; unique turn labels are mechanically checked",
        "context_boundary": "The harness thread limit prevented thirteen new blank-context agents. Each credited turn is assigned a case different from that agent's retained prior case; unrelated relay or prior-case content may remain in context.",
        "exclusions": ["eval oracles", "development corpus", "same-case prior outputs", "behavioral reviews", "browsing", "image tools", "providers", "durable state", "external actions"],
    }
    host = {"label": args.host, "attributed": True}
    adapter = {"label": args.adapter, "attributed": True}
    metadata = {
        "format": FORMAT,
        "run_id": run_dir.name,
        "prepared_at": prepared_at,
        "runtime_commit": runtime_commit,
        "requested_model_route": args.requested_model_route,
        "observed_model_identity": None,
        "host": host,
        "adapter": adapter,
        "isolation_contract": isolation_contract,
        "eval": {
            "suite_path": rel(EVAL_SUITE), "suite_sha256": digest(EVAL_SUITE.read_bytes()),
            "manifest_path": rel(EVAL_MANIFEST), "manifest_sha256": digest(EVAL_MANIFEST.read_bytes()),
            "case_count": len(cases), "suite": suite.get("suite"),
        },
        "canonical_package_files": runtime,
        "development_corpus_files": corpus_files(),
        "cases": [],
    }
    for case in cases:
        case_id = case["id"]
        text = case.get("input")
        if not isinstance(text, str):
            raise ValueError(f"case {case_id} lacks an exact string input")
        input_rel = f"inputs/{case_id}.txt"
        input_bytes = text.encode("utf-8")
        write_identical(run_path(run_dir, input_rel), input_bytes)
        allowed = allowed_runtime(case_id)
        allowed_files = {name: runtime[name] for name in allowed}
        packet_rel = f"packets/{case_id}.json"
        packet = {
            "format": FORMAT,
            "run_id": run_dir.name,
            "prepared_at": prepared_at,
            "case_id": case_id,
            "input": {"path": input_rel, "text": text, "sha256": digest(input_bytes), "bytes": len(input_bytes)},
            "eval_case": {
                "source_path": rel(EVAL_SUITE),
                "canonical_json_sha256": digest(canonical_bytes(case)),
                "canonicalization": "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=False)",
            },
            "runtime": {"commit": runtime_commit, "allowed_files": allowed_files},
            "route": {"requested_model_route": args.requested_model_route, "observed_model_identity": None},
            "host": host,
            "adapter": adapter,
            "isolation_contract": isolation_contract,
        }
        packet_bytes = canonical_bytes(packet) + b"\n"
        write_identical(run_path(run_dir, packet_rel), packet_bytes)
        metadata["cases"].append({
            "id": case_id,
            "eval_case_canonical_json_sha256": digest(canonical_bytes(case)),
            "input": {"path": input_rel, "sha256": digest(input_bytes), "bytes": len(input_bytes)},
            "allowed_runtime": allowed_files,
            "packet": {"path": packet_rel, "sha256": digest(packet_bytes), "bytes": len(packet_bytes)},
            "raw_path": f"raw/{case_id}.md",
            "output_path": f"outputs/{case_id}.md",
            "execution_path": f"executions/{case_id}.json",
        })
    write_identical(run_dir / "run.json", canonical_bytes(metadata) + b"\n")
    print(json.dumps({"check": "prepare", "status": "PREPARED", "run_dir": str(run_dir), "cases": len(cases), "runtime_commit": runtime_commit}))
    return 0


def parse_header(raw: bytes, allowed: dict[str, dict[str, Any]]) -> tuple[str, str, dict[str, str], bytes]:
    first, separator, visible = raw.partition(b"\n")
    if not separator:
        raise ValueError("raw receipt has no first-line terminator")
    if first.endswith(b"\r"):
        first = first[:-1]
    try:
        line = first.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ValueError("raw receipt first line must be ASCII") from exc
    match = HEADER.fullmatch(line)
    if not match:
        raise ValueError("raw receipt first line does not match required READ_OK header")
    turn, head, items = match.groups()
    hashes: dict[str, str] = {}
    for item in items.split(","):
        parsed = HASH_ITEM.fullmatch(item.strip())
        if not parsed:
            raise ValueError(f"invalid FILE_HASHES item: {item}")
        name, value = parsed.groups()
        normalized_name = name.lower()
        if normalized_name in hashes:
            raise ValueError(f"duplicate FILE_HASHES basename: {name}")
        hashes[normalized_name] = value
    expected = {Path(name).name.lower(): record["sha256"] for name, record in allowed.items()}
    if hashes != expected:
        raise ValueError("FILE_HASHES must exactly match this case's allowed runtime subset")
    return turn, head, hashes, visible


def cmd_finalize(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    run = read_json(run_dir / "run.json")
    turns: set[str] = set()
    executions: list[dict[str, Any]] = []
    finalized_at = utc_now()
    for case in run["cases"]:
        raw_path = run_path(run_dir, case["raw_path"])
        if not raw_path.is_file():
            raise ValueError(f"missing raw receipt: {raw_path}")
        raw = raw_path.read_bytes()
        turn, head, header_hashes, visible = parse_header(raw, case["allowed_runtime"])
        if turn in turns:
            raise ValueError(f"duplicate fresh turn ID: {turn}")
        turns.add(turn)
        if head != run["runtime_commit"]:
            raise ValueError(f"raw receipt HEAD differs from runtime commit: {case['id']}")
        output_path = run_path(run_dir, case["output_path"])
        write_identical(output_path, visible)
        first_line = raw.partition(b"\n")[0].removesuffix(b"\r")
        execution = {
            "format": FORMAT, "case_id": case["id"], "finalized_at": finalized_at,
            "fresh_turn": {"id": turn, "assertion": "one fresh turn for this case", "state": "attributed"},
            "runtime": {"commit": head, "files": case["allowed_runtime"]},
            "input": case["input"],
            "packet": case["packet"],
            "route": {"requested_model_route": run["requested_model_route"], "observed_model_identity": None},
            "host": run["host"],
            "adapter": run["adapter"],
            "isolation_contract": run["isolation_contract"],
            "transport_receipt": {"path": case["raw_path"], "sha256": digest(raw), "bytes": len(raw), "header_sha256": digest(first_line)},
            "header_file_hashes": header_hashes,
            "user_visible_output": {"path": case["output_path"], "sha256": digest(visible), "bytes": len(visible)},
            "eval_case_canonical_json_sha256": case["eval_case_canonical_json_sha256"],
        }
        execution_path = run_path(run_dir, case["execution_path"])
        execution_bytes = canonical_bytes(execution) + b"\n"
        write_identical(execution_path, execution_bytes)
        executions.append({"case_id": case["id"], "path": case["execution_path"], "sha256": digest(execution_bytes)})
    receipt = {
        "format": FORMAT, "run_id": run["run_id"], "finalized_at": finalized_at,
        "runtime_commit": run["runtime_commit"], "requested_model_route": run["requested_model_route"],
        "observed_model_identity": None, "case_count": len(executions), "executions": executions,
        "run_manifest_sha256": digest((run_dir / "run.json").read_bytes()),
        "aggregate_projection": {
            "case_ids": [item["case_id"] for item in executions],
            "packet_sha256": [case["packet"]["sha256"] for case in run["cases"]],
            "execution_sha256": [item["sha256"] for item in executions],
        },
        "claim_boundary": "Evidence-integrity custody only; no behavioral-quality, installation, discovery, invocation, provider, rendering, or observed-model-identity claim.",
    }
    receipt["aggregate_sha256"] = digest(canonical_bytes(receipt["aggregate_projection"]))
    write_identical(run_dir / "suite-receipt.json", canonical_bytes(receipt) + b"\n")
    print(json.dumps({"check": "finalize", "status": "FINALIZED", "cases": len(executions)}))
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    run = read_json(run_dir / "run.json")
    suite, canonical_cases = load_cases()
    errors: list[str] = []
    def expect(condition: bool, message: str) -> None:
        if not condition: errors.append(message)
    expect(run.get("format") == FORMAT, "run format mismatch")
    runtime_commit = run.get("runtime_commit")
    expect(isinstance(runtime_commit, str) and re.fullmatch(r"[0-9a-f]{40}", runtime_commit) is not None, "invalid runtime Git commit")
    expect(isinstance(run.get("requested_model_route"), str) and bool(run["requested_model_route"].strip()), "requested model route is missing")
    expect(run.get("observed_model_identity") is None, "run observed model identity must remain null")
    expect(run.get("host", {}).get("attributed") is True, "host label must remain attributed")
    expect(run.get("adapter", {}).get("attributed") is True, "adapter label must remain attributed")
    expect(run.get("eval", {}).get("suite_sha256") == digest(EVAL_SUITE.read_bytes()), "eval suite hash mismatch")
    expect(run.get("eval", {}).get("manifest_sha256") == digest(EVAL_MANIFEST.read_bytes()), "eval manifest hash mismatch")
    expect(run.get("canonical_package_files") == package_files(), "canonical package file hashes mismatch")
    expect(run.get("development_corpus_files") == corpus_files(), "development corpus file hashes mismatch")
    if isinstance(runtime_commit, str) and re.fullmatch(r"[0-9a-f]{40}", runtime_commit):
        for name, record in run.get("canonical_package_files", {}).items():
            try:
                historic = git_file_bytes(runtime_commit, f"{rel(PACKAGE)}/{name}")
            except ValueError as exc:
                errors.append(str(exc))
            else:
                expect(record == {"sha256": digest(historic), "bytes": len(historic)}, f"runtime commit package bytes mismatch: {name}")
        for name, record in run.get("development_corpus_files", {}).items():
            try:
                historic = git_file_bytes(runtime_commit, name)
            except ValueError as exc:
                errors.append(str(exc))
            else:
                expect(record == {"sha256": digest(historic), "bytes": len(historic)}, f"runtime commit corpus bytes mismatch: {name}")
    canonical_by_id = {case["id"]: case for case in canonical_cases}
    run_cases = run.get("cases", [])
    ids = [item.get("id") for item in run_cases if isinstance(item, dict)]
    expect(len(ids) == 13 and set(ids) == set(canonical_by_id), "case set/count differs from canonical full suite")
    turns: set[str] = set()
    execution_hashes: list[str] = []
    packet_hashes: list[str] = []
    expected_executions: list[dict[str, str]] = []
    for case in run_cases:
        case_id = case.get("id")
        if case_id not in canonical_by_id: continue
        expected_case_hash = digest(canonical_bytes(canonical_by_id[case_id]))
        expect(case.get("eval_case_canonical_json_sha256") == expected_case_hash, f"{case_id}: canonical case hash mismatch")
        input_path = run_path(run_dir, case["input"]["path"])
        input_bytes = input_path.read_bytes() if input_path.is_file() else b""
        expect(input_bytes == canonical_by_id[case_id].get("input", "").encode("utf-8"), f"{case_id}: exact input bytes mismatch")
        expect(case["input"].get("sha256") == digest(input_bytes), f"{case_id}: input hash mismatch")
        expect(case["input"].get("bytes") == len(input_bytes), f"{case_id}: input byte count mismatch")
        expected_allowed = {name: run["canonical_package_files"][name] for name in allowed_runtime(case_id)}
        expect(case.get("allowed_runtime") == expected_allowed, f"{case_id}: allowed runtime subset mismatch")
        packet_path = run_path(run_dir, case["packet"]["path"])
        packet_bytes = packet_path.read_bytes() if packet_path.is_file() else b""
        packet_hashes.append(digest(packet_bytes))
        expect(case["packet"].get("sha256") == digest(packet_bytes), f"{case_id}: packet hash mismatch")
        expect(case["packet"].get("bytes") == len(packet_bytes), f"{case_id}: packet byte count mismatch")
        if packet_path.is_file():
            packet = read_json(packet_path)
            expect(packet.get("case_id") == case_id, f"{case_id}: packet case mismatch")
            expect(packet.get("input", {}).get("text", "").encode("utf-8") == input_bytes, f"{case_id}: packet input text mismatch")
            expect(packet.get("eval_case", {}).get("canonical_json_sha256") == expected_case_hash, f"{case_id}: packet eval hash mismatch")
            expect(packet.get("runtime", {}).get("commit") == runtime_commit, f"{case_id}: packet runtime commit mismatch")
            expect(packet.get("runtime", {}).get("allowed_files") == expected_allowed, f"{case_id}: packet runtime files mismatch")
            expect(packet.get("route", {}).get("requested_model_route") == run["requested_model_route"], f"{case_id}: packet requested route mismatch")
            expect(packet.get("route", {}).get("observed_model_identity") is None, f"{case_id}: packet observed model identity must be null")
            expect(packet.get("host") == run["host"] and packet.get("adapter") == run["adapter"], f"{case_id}: packet host or adapter mismatch")
        execution_path = run_path(run_dir, case["execution_path"])
        if not execution_path.is_file(): errors.append(f"{case_id}: missing execution"); continue
        execution_bytes = execution_path.read_bytes(); execution = read_json(execution_path)
        execution_hashes.append(digest(execution_bytes))
        expected_executions.append({"case_id": case_id, "path": case["execution_path"], "sha256": digest(execution_bytes)})
        raw_path = run_path(run_dir, case["raw_path"]); raw = raw_path.read_bytes() if raw_path.is_file() else b""
        try: turn, head, hashes, visible = parse_header(raw, expected_allowed)
        except ValueError as exc: errors.append(f"{case_id}: {exc}"); continue
        expect(turn not in turns, f"{case_id}: duplicate fresh turn ID"); turns.add(turn)
        expect(head == runtime_commit, f"{case_id}: runtime commit mismatch")
        expect(execution.get("fresh_turn", {}).get("id") == turn, f"{case_id}: execution turn mismatch")
        expect(execution.get("runtime") == {"commit": head, "files": expected_allowed}, f"{case_id}: execution runtime mismatch")
        expect(execution.get("input") == case["input"], f"{case_id}: execution input mismatch")
        expect(execution.get("packet") == case["packet"], f"{case_id}: execution packet mismatch")
        expect(execution.get("route") == {"requested_model_route": run["requested_model_route"], "observed_model_identity": None}, f"{case_id}: execution route mismatch")
        expect(execution.get("host") == run["host"] and execution.get("adapter") == run["adapter"], f"{case_id}: execution host or adapter mismatch")
        expect(execution.get("isolation_contract") == run["isolation_contract"], f"{case_id}: execution isolation contract mismatch")
        expect(execution.get("eval_case_canonical_json_sha256") == expected_case_hash, f"{case_id}: execution eval hash mismatch")
        expect(execution.get("transport_receipt", {}).get("path") == case["raw_path"], f"{case_id}: transport path mismatch")
        expect(execution.get("transport_receipt", {}).get("sha256") == digest(raw), f"{case_id}: raw hash mismatch")
        expect(execution.get("transport_receipt", {}).get("bytes") == len(raw), f"{case_id}: raw byte count mismatch")
        first_line = raw.partition(b"\n")[0].removesuffix(b"\r")
        expect(execution.get("transport_receipt", {}).get("header_sha256") == digest(first_line), f"{case_id}: header hash mismatch")
        expect(execution.get("header_file_hashes") == hashes, f"{case_id}: execution header hashes mismatch")
        output_path = run_path(run_dir, case["output_path"]); output = output_path.read_bytes() if output_path.is_file() else b""
        expect(output == visible, f"{case_id}: visible output does not equal raw remainder")
        expect(execution.get("user_visible_output", {}).get("path") == case["output_path"], f"{case_id}: output path mismatch")
        expect(execution.get("user_visible_output", {}).get("sha256") == digest(output), f"{case_id}: output hash mismatch")
        expect(execution.get("user_visible_output", {}).get("bytes") == len(output), f"{case_id}: output byte count mismatch")
    expect(len(turns) == 13, "fresh turn set is incomplete")
    receipt_path = run_dir / "suite-receipt.json"
    if not receipt_path.is_file(): errors.append("missing suite receipt")
    else:
        receipt = read_json(receipt_path)
        expected_projection = {"case_ids": ids, "packet_sha256": packet_hashes, "execution_sha256": execution_hashes}
        expect(receipt.get("format") == FORMAT and receipt.get("run_id") == run.get("run_id"), "receipt identity mismatch")
        expect(receipt.get("case_count") == 13, "receipt case count mismatch")
        expect(receipt.get("executions") == expected_executions, "receipt execution list mismatch")
        expect(receipt.get("run_manifest_sha256") == digest((run_dir / "run.json").read_bytes()), "receipt run manifest hash mismatch")
        expect(receipt.get("aggregate_projection") == expected_projection, "receipt aggregate projection mismatch")
        expect(receipt.get("aggregate_sha256") == digest(canonical_bytes(expected_projection)), "receipt aggregate hash mismatch")
        expect(receipt.get("runtime_commit") == run["runtime_commit"], "receipt runtime commit mismatch")
        expect(receipt.get("requested_model_route") == run["requested_model_route"], "requested model route mismatch")
        expect(receipt.get("observed_model_identity") is None, "observed model identity must be null without raw transport evidence")
    if errors:
        print(json.dumps({"check": "evidence-integrity", "status": "FAIL", "errors": errors}, indent=2)); return 1
    print(json.dumps({"check": "evidence-integrity", "status": "PASS", "cases": 13, "claim_boundary": "Byte custody and declared isolation metadata only; no behavioral-quality claim."}, indent=2)); return 0


def cmd_seal(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if cmd_verify(argparse.Namespace(run_dir=str(run_dir))) != 0: return 1
    receipt = run_dir / "suite-receipt.json"; receipt_rel = rel(receipt)
    result = subprocess.run(["git", "-C", str(REPO), "show", f"{args.evidence_commit}:{receipt_rel}"], capture_output=True)
    if result.returncode or result.stdout != receipt.read_bytes():
        raise ValueError("supplied evidence commit does not contain byte-identical suite receipt")
    run = read_json(run_dir / "run.json")
    custody = {"format": FORMAT, "sealed_at": utc_now(), "runtime_commit": run["runtime_commit"], "evidence_payload_commit": args.evidence_commit, "later_custody_commit_state": {"current_head": git_head(), "state": "observed at seal time"}, "suite_receipt": {"path": receipt_rel, "sha256": digest(receipt.read_bytes())}}
    write_identical(run_dir / "evidence-custody.json", canonical_bytes(custody) + b"\n")
    print(json.dumps({"check": "seal", "status": "SEALED", "evidence_payload_commit": args.evidence_commit}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    prepare = subs.add_parser("prepare"); prepare.add_argument("--run-dir", required=True); prepare.add_argument("--requested-model-route", required=True); prepare.add_argument("--host", default="Codex"); prepare.add_argument("--adapter", default="unspecified")
    for name in ("finalize", "verify"):
        sub = subs.add_parser(name); sub.add_argument("--run-dir", required=True)
    seal = subs.add_parser("seal"); seal.add_argument("--run-dir", required=True); seal.add_argument("--evidence-commit", required=True)
    args = parser.parse_args()
    try:
        return {"prepare": cmd_prepare, "finalize": cmd_finalize, "verify": cmd_verify, "seal": cmd_seal}[args.command](args)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"check": args.command, "status": "FAIL", "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
