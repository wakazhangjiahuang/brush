#!/usr/bin/env python3
"""
Binary materialization bridge for $brush-creator-studio V2.0.0.

Purpose:
- turn a locally available GitHub checkout / GitHub Actions artifact into usable Procreate binary paths;
- extract standalone .brush packages from a native .brushset;
- prepare branch-scoped runtime bundles for cartoon / vintage;
- write a machine-readable native asset manifest.

Acceptance remains in runtime/native_runtime.py + knowledge/RUNTIME-CONTRACT.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set

RUNTIME_DIR = Path(__file__).resolve().parent
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from native_runtime import inspect_brush, inspect_brushset  # noqa: E402

LFS_HEADER = b"version https://git-lfs.github.com/spec/v1"


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _safe_filename(name: str, fallback: str) -> str:
    value = (name or "").strip() or fallback
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    value = value.rstrip(". ")
    return value or fallback


def _is_lfs_pointer(path: Path) -> bool:
    try:
        return path.read_bytes()[:1024].startswith(LFS_HEADER)
    except Exception:
        return False


def extract_brush_from_brushset(
    brushset_path: str,
    output_path: str,
    *,
    member_id: Optional[str] = None,
    internal_name: Optional[str] = None,
) -> Dict[str, Any]:
    """Extract exactly one brushset member into a standalone native .brush."""
    source = Path(brushset_path)
    output = Path(output_path)

    set_check = inspect_brushset(source)
    if set_check.get("status") != "NATIVE_STRUCTURE_PASS":
        return {
            "status": "NATIVE_OUTPUT_BLOCKED",
            "reason_code": "SOURCE_BRUSHSET_VALIDATION_FAILED",
            "errors": set_check.get("errors", []),
            "source": str(source),
        }

    if bool(member_id) == bool(internal_name):
        return {
            "status": "NATIVE_OUTPUT_BLOCKED",
            "reason_code": "BRUSHSET_MEMBER_SELECTOR_INVALID",
            "errors": ["Provide exactly one of member_id or internal_name."],
            "source": str(source),
        }

    matches = []
    for member in set_check.get("members", []):
        if member_id and member.get("member_id") == member_id:
            matches.append(member)
        elif internal_name and member.get("internal_name") == internal_name:
            matches.append(member)

    if not matches:
        return {
            "status": "NATIVE_OUTPUT_BLOCKED",
            "reason_code": "BRUSHSET_MEMBER_NOT_FOUND",
            "errors": ["Requested brushset member was not found."],
            "source": str(source),
            "member_id": member_id,
            "internal_name": internal_name,
        }
    if len(matches) > 1:
        return {
            "status": "NATIVE_OUTPUT_BLOCKED",
            "reason_code": "BRUSHSET_MEMBER_AMBIGUOUS",
            "errors": ["Requested internal name matched more than one brushset member; use member_id."],
            "source": str(source),
            "internal_name": internal_name,
            "matches": matches,
        }

    selected = matches[0]
    selected_id = str(selected["member_id"])
    prefix = f"{selected_id}/"
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(source, "r") as src, zipfile.ZipFile(
            output, "w", compression=zipfile.ZIP_DEFLATED
        ) as dst:
            member_files = [
                info for info in src.infolist()
                if not info.is_dir() and info.filename.startswith(prefix)
            ]
            if not member_files:
                raise ValueError(f"No packaged files found for brushset member {selected_id}")
            for info in member_files:
                relative_name = info.filename[len(prefix):]
                if relative_name:
                    dst.writestr(relative_name, src.read(info.filename))

        checked = inspect_brush(output)
        checked.update({
            "source_brushset": str(source),
            "source_brushset_sha256": _sha256_file(source),
            "source_member_id": selected_id,
            "source_internal_name": selected.get("internal_name"),
            "materialized_path": str(output),
        })
        return checked
    except Exception as exc:
        return {
            "status": "NATIVE_OUTPUT_BLOCKED",
            "reason_code": "BRUSHSET_MEMBER_EXTRACTION_FAILED",
            "errors": [str(exc)],
            "source": str(source),
            "member_id": selected_id,
        }


def extract_all_brushes_from_brushset(brushset_path: str, output_dir: str) -> Dict[str, Any]:
    """Extract all declared brushset members into validated standalone .brush files."""
    source = Path(brushset_path)
    out_dir = Path(output_dir)
    set_check = inspect_brushset(source)
    if set_check.get("status") != "NATIVE_STRUCTURE_PASS":
        return {
            "status": "NATIVE_OUTPUT_BLOCKED",
            "reason_code": "SOURCE_BRUSHSET_VALIDATION_FAILED",
            "errors": set_check.get("errors", []),
            "source": str(source),
        }

    out_dir.mkdir(parents=True, exist_ok=True)
    used_names: Set[str] = set()
    results: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []

    for index, member in enumerate(set_check.get("members", []), start=1):
        member_id = str(member.get("member_id"))
        display_name = str(member.get("internal_name") or member_id)
        stem = _safe_filename(display_name, f"brush-{index:03d}")
        candidate = stem
        suffix_index = 2
        while candidate.casefold() in used_names:
            candidate = f"{stem}__{suffix_index}"
            suffix_index += 1
        used_names.add(candidate.casefold())
        output = out_dir / f"{candidate}.brush"
        result = extract_brush_from_brushset(
            str(source), str(output), member_id=member_id
        )
        results.append(result)
        if result.get("status") != "NATIVE_STRUCTURE_PASS":
            failures.append(result)

    return {
        "status": "NATIVE_STRUCTURE_PASS" if not failures else "NATIVE_OUTPUT_BLOCKED",
        "reason_code": "BRUSHSET_ALL_MEMBERS_EXTRACTED" if not failures else "BRUSHSET_MEMBER_EXTRACTION_PARTIAL",
        "source_brushset": str(source),
        "source_sha256": _sha256_file(source),
        "member_count": len(results),
        "failure_count": len(failures),
        "results": results,
        "errors": [error for item in failures for error in item.get("errors", [])],
    }


def _copy_file(source: Path, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def write_asset_manifest(bundle_root: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    root = Path(bundle_root)
    if not root.exists():
        raise FileNotFoundError(root)

    records = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        record: Dict[str, Any] = {
            "path": rel,
            "size_bytes": path.stat().st_size,
            "sha256": _sha256_file(path),
        }
        if path.suffix == ".brush":
            check = inspect_brush(path)
            record.update({
                "native_type": "brush",
                "native_status": check.get("status"),
                "native_name": check.get("internal_name"),
                "reason_code": check.get("reason_code"),
            })
        elif path.suffix == ".brushset":
            check = inspect_brushset(path)
            record.update({
                "native_type": "brushset",
                "native_status": check.get("status"),
                "native_name": check.get("internal_name"),
                "member_count": check.get("member_count"),
                "reason_code": check.get("reason_code"),
            })
        elif path.suffix.lower() == ".xlsx":
            record["native_type"] = "xlsx_template"
        records.append(record)

    manifest = {
        "schema_version": "2.0",
        "bundle_root": str(root),
        "file_count": len(records),
        "files": records,
    }
    target = Path(output_path) if output_path else root / "native-asset-manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def prepare_branch_bundle(profile: str, repo_root: str, output_dir: str) -> Dict[str, Any]:
    if profile not in {"cartoon", "vintage"}:
        raise ValueError("profile must be cartoon or vintage")

    repo = Path(repo_root).resolve()
    output = Path(output_dir).resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    manifest_path = repo / "KB-MANIFEST.json"
    registry_path = repo / "knowledge/BRUSH-REGISTRY.json"
    capability_path = repo / "knowledge/BRUSH-CAPABILITY-REGISTRY.json"
    template_readme = repo / "templates/README.md"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    registry = json.loads(registry_path.read_text(encoding="utf-8"))

    routing = manifest["routing"][profile]
    preferred_set = repo / routing["preferred_brushset"]
    template = repo / manifest["entrypoints"]["procreate_workflow_template"]

    if not preferred_set.exists():
        raise FileNotFoundError(preferred_set)
    if _is_lfs_pointer(preferred_set):
        raise RuntimeError(f"Preferred brushset is still a Git LFS pointer: {preferred_set}")
    if not template.exists():
        raise FileNotFoundError(template)

    family_id = f"{profile}-single"
    family = next(
        (item for item in registry.get("families", []) if item.get("family_id") == family_id),
        None,
    )
    if not family:
        raise RuntimeError(f"Registry family missing: {family_id}")

    copied_singles = []
    for asset in family.get("assets", []):
        source = repo / asset["path"]
        if not source.exists():
            continue
        target = output / "笔刷" / family_id / source.name
        _copy_file(source, target)
        copied_singles.append(str(target.relative_to(output)))

    set_target = output / "笔刷" / "preferred-brushset" / preferred_set.name
    _copy_file(preferred_set, set_target)

    extraction = extract_all_brushes_from_brushset(
        str(set_target),
        str(output / "笔刷" / "preferred-brushset-members"),
    )
    if extraction.get("status") != "NATIVE_STRUCTURE_PASS":
        raise RuntimeError("Preferred brushset extraction failed: " + json.dumps(extraction, ensure_ascii=False))

    template_target = output / "templates" / "Procreate" / template.name
    _copy_file(template, template_target)
    _copy_file(manifest_path, output / "KB-MANIFEST.json")
    _copy_file(registry_path, output / "knowledge" / registry_path.name)
    if capability_path.exists():
        _copy_file(capability_path, output / "knowledge" / capability_path.name)
    if template_readme.exists():
        _copy_file(template_readme, output / "templates" / template_readme.name)

    runtime_target = output / "runtime"
    runtime_target.mkdir(parents=True, exist_ok=True)
    _copy_file(repo / "runtime/native_runtime.py", runtime_target / "native_runtime.py")
    _copy_file(Path(__file__).resolve(), runtime_target / "binary_materialization.py")

    summary = {
        "schema_version": "2.0",
        "profile": profile,
        "preferred_brushset": str(set_target.relative_to(output)),
        "preferred_brushset_sha256": _sha256_file(set_target),
        "individual_brush_count": len(copied_singles),
        "extracted_preferred_set_member_count": extraction.get("member_count"),
        "template": str(template_target.relative_to(output)),
        "binary_materialization_ready": True,
    }
    (output / "bundle-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_asset_manifest(str(output))
    return summary


def _cli() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    cmd = sub.add_parser("extract-one")
    cmd.add_argument("brushset")
    cmd.add_argument("output")
    selector = cmd.add_mutually_exclusive_group(required=True)
    selector.add_argument("--member-id")
    selector.add_argument("--internal-name")

    cmd = sub.add_parser("extract-all")
    cmd.add_argument("brushset")
    cmd.add_argument("output_dir")

    cmd = sub.add_parser("prepare-bundle")
    cmd.add_argument("--profile", choices=["cartoon", "vintage"], required=True)
    cmd.add_argument("--repo-root", default=".")
    cmd.add_argument("--output", required=True)

    cmd = sub.add_parser("manifest")
    cmd.add_argument("bundle_root")
    cmd.add_argument("--output")

    args = parser.parse_args()

    try:
        if args.cmd == "extract-one":
            result = extract_brush_from_brushset(
                args.brushset,
                args.output,
                member_id=args.member_id,
                internal_name=args.internal_name,
            )
        elif args.cmd == "extract-all":
            result = extract_all_brushes_from_brushset(args.brushset, args.output_dir)
        elif args.cmd == "prepare-bundle":
            result = prepare_branch_bundle(args.profile, args.repo_root, args.output)
            result = {"status": "NATIVE_METADATA_PASS", "reason_code": "BUNDLE_READY", **result}
        else:
            result = write_asset_manifest(args.bundle_root, args.output)
            result = {"status": "NATIVE_METADATA_PASS", "reason_code": "ASSET_MANIFEST_WRITTEN", **result}
    except Exception as exc:
        result = {
            "status": "NATIVE_OUTPUT_BLOCKED",
            "reason_code": "BINARY_MATERIALIZATION_FAILED",
            "errors": [str(exc)],
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") in {"NATIVE_METADATA_PASS", "NATIVE_STRUCTURE_PASS"} else 2


if __name__ == "__main__":
    raise SystemExit(_cli())
