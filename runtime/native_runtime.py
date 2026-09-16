#!/usr/bin/env python3
"""
$brush-creator-studio V2.0.0 compatible Procreate native runtime.

This module provides evidence-safe structural inspection/build/package validation for
`.brush` / `.brushset` files. It deliberately distinguishes package-local resources
from Procreate/system preset identifiers: a bare preset/image name that is not
packaged is recorded as an external/system reference, not automatically treated as
package corruption.

Structural PACKAGE_PASS is not a real Procreate import/drawing test.
FULL_PASS requires target-software validation outside this module.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
import plistlib
import shutil
import subprocess
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Sequence, Set, Tuple, Union

PathLike = Union[str, os.PathLike]

LFS_HEADER = b"version https://git-lfs.github.com/spec/v1"
LFS_OID_PREFIX = b"oid sha256:"
LFS_SIZE_PREFIX = b"size "
REQUIRED_BRUSH_MEMBER = "Brush.archive"

PASS_STATUSES = {"NATIVE_METADATA_PASS", "NATIVE_STRUCTURE_PASS", "PACKAGE_PASS"}

SAFE_ARCHIVE_PATCH_FIELDS = {
    "plotSpacing", "plotJitter", "plotJitterLongitudinal", "plotSmoothing",
    "maxSize", "minSize", "maxOpacity", "minOpacity",
    "dynamicsPressureSize", "dynamicsPressureOpacity", "dynamicsPressureResponse",
    "dynamicsTiltSize", "wetEdgesAmount", "dynamicsWetAccumulation",
    "dynamicsWetnessJitter", "dynamicsLoad", "dynamicsPressureMix",
    "dynamicsSmudgeAccumulation", "grainDepth", "textureScale",
    "textureContrast", "paintSize", "paintOpacity", "smudgeSize", "smudgeOpacity",
}

RESOURCE_KEYWORDS = ("shape", "grain", "texture")
RESOURCE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".gif", ".heic",
    ".dat", ".bin", ".archive", ".plist",
}


def _result(
    status: str,
    *,
    reason_code: Optional[str] = None,
    evidence_state: str = "UNVERIFIED",
    internal_name: Optional[str] = None,
    sha256: Optional[str] = None,
    member_count: Optional[int] = None,
    missing_members: Optional[Sequence[str]] = None,
    extra_members: Optional[Sequence[str]] = None,
    errors: Optional[Sequence[str]] = None,
    **extra: Any,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "status": status,
        "reason_code": reason_code,
        "evidence_state": evidence_state,
        "internal_name": internal_name,
        "sha256": sha256,
        "member_count": member_count,
        "missing_members": list(missing_members or []),
        "extra_members": list(extra_members or []),
        "errors": list(errors or []),
    }
    out.update(extra)
    return out


def _read_bytes(value: Union[PathLike, bytes, bytearray]) -> bytes:
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)
    return Path(value).read_bytes()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: PathLike) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def detect_lfs_pointer(path_or_bytes: Union[PathLike, bytes, bytearray]) -> Dict[str, Any]:
    try:
        data = _read_bytes(path_or_bytes)
    except Exception as exc:
        return _result("NATIVE_OUTPUT_BLOCKED", reason_code="READ_FAILED", errors=[str(exc)])

    head = data[:1024]
    if not head.startswith(LFS_HEADER):
        return _result(
            "NATIVE_METADATA_PASS",
            reason_code="NOT_LFS_POINTER",
            evidence_state="VERIFIED_METADATA",
            sha256=_sha256_bytes(data),
            is_lfs_pointer=False,
        )

    oid = None
    size = None
    for line in head.splitlines():
        if line.startswith(LFS_OID_PREFIX):
            candidate = line[len(LFS_OID_PREFIX):].strip().decode("ascii", errors="ignore")
            if len(candidate) == 64:
                oid = candidate
        elif line.startswith(LFS_SIZE_PREFIX):
            try:
                size = int(line[len(LFS_SIZE_PREFIX):].strip())
            except ValueError:
                pass

    return _result(
        "LFS_POINTER",
        reason_code="GIT_LFS_POINTER_DETECTED",
        evidence_state="VERIFIED_METADATA",
        sha256=_sha256_bytes(data),
        is_lfs_pointer=True,
        lfs_oid_sha256=oid,
        lfs_size=size,
    )


def _decode_archive(data: bytes) -> Tuple[Dict[str, Any], list, Dict[str, Any]]:
    payload = plistlib.loads(data)
    objects = payload.get("$objects")
    if not isinstance(objects, list) or len(objects) < 2 or not isinstance(objects[1], dict):
        raise ValueError("Unsupported Brush.archive keyed-archive structure")
    return payload, objects, objects[1]


def _uid_value(objects: list, value: Any) -> Any:
    if isinstance(value, plistlib.UID) and 0 <= value.data < len(objects):
        return objects[value.data]
    return value


def _brush_name_from_archive(data: bytes) -> Optional[str]:
    try:
        _, objects, root = _decode_archive(data)
        name = _uid_value(objects, root.get("name"))
        return name if isinstance(name, str) else None
    except Exception:
        return None


def _metadata_subset(root: Dict[str, Any]) -> Dict[str, Any]:
    keys = [
        "version", "plotSpacing", "plotJitter", "plotJitterLongitudinal", "plotSmoothing",
        "maxSize", "minSize", "maxOpacity", "minOpacity",
        "dynamicsPressureSize", "dynamicsPressureOpacity", "dynamicsPressureResponse",
        "dynamicsTiltSize", "wetEdgesAmount", "dynamicsWetAccumulation",
        "dynamicsWetnessJitter", "dynamicsLoad", "dynamicsPressureMix",
        "dynamicsSmudgeAccumulation", "grainDepth", "textureScale", "textureContrast",
        "textureMovement", "shapeCount", "shapeScatter", "shapeRandomise",
        "importedFromABR", "renderingRecursiveMixing", "paintSize", "paintOpacity",
        "smudgeSize", "smudgeOpacity",
    ]
    return {
        key: root[key]
        for key in keys
        if key in root and isinstance(root[key], (str, int, float, bool))
    }


def _looks_like_resource_name(value: str) -> bool:
    stripped = value.strip()
    if not stripped or len(stripped) > 512:
        return False
    suffix = Path(stripped.replace("\\", "/")).suffix.lower()
    return "/" in stripped or "\\" in stripped or suffix in RESOURCE_EXTENSIONS


def _collect_resource_refs(objects: list, root: Dict[str, Any]) -> Set[str]:
    """Collect filename/path-like Shape/Grain/Texture references from Brush.archive."""
    refs: Set[str] = set()
    seen_uids: Set[int] = set()
    seen_obj_ids: Set[int] = set()

    def walk(value: Any, key_hint: str = "") -> None:
        if isinstance(value, plistlib.UID):
            if value.data in seen_uids or not (0 <= value.data < len(objects)):
                return
            seen_uids.add(value.data)
            walk(objects[value.data], key_hint)
            return
        if isinstance(value, dict):
            object_id = id(value)
            if object_id in seen_obj_ids:
                return
            seen_obj_ids.add(object_id)
            for key, child in value.items():
                walk(child, str(key))
            return
        if isinstance(value, (list, tuple)):
            for child in value:
                walk(child, key_hint)
            return
        if isinstance(value, str):
            hint = key_hint.lower()
            if any(word in hint for word in RESOURCE_KEYWORDS) and _looks_like_resource_name(value):
                refs.add(value.replace("\\", "/"))

    walk(root)
    return refs


def _normalized_zip_names(zip_names: Iterable[str]) -> Set[str]:
    return {name.lstrip("./") for name in zip_names if name and not name.endswith("/")}


def _match_resource_ref(ref: str, zip_names: Sequence[str]) -> bool:
    normalized = ref.lstrip("./")
    names = _normalized_zip_names(zip_names)
    if normalized in names:
        return True
    basename = Path(normalized).name
    return any(Path(name).name == basename for name in names)


def _is_explicit_package_local_ref(ref: str) -> bool:
    """
    Only path-qualified references are hard package-local requirements.

    Procreate Brush.archive commonly stores bare names such as Brush-Preset-*.png,
    Brush-Artery-*.jpg, Brush-Pocket-*.png, Gouache-Wash.jpg, Acrylic-Square.jpg,
    etc. Those may identify Procreate/system/library resources and are not proof that
    the file must be embedded in the .brush ZIP. Bare names are therefore reported as
    external/system references unless the matching file is actually present.
    """
    raw = ref.strip().replace("\\", "/")
    return raw.startswith("./") or raw.startswith("../") or "/" in raw


def _classify_resource_refs(refs: Sequence[str], zip_names: Sequence[str]) -> Dict[str, Any]:
    embedded = []
    package_local = []
    external_or_system = []
    missing_package_local = []

    for ref in sorted(set(refs)):
        if _match_resource_ref(ref, zip_names):
            embedded.append(ref)
            continue
        if _is_explicit_package_local_ref(ref):
            package_local.append(ref)
            missing_package_local.append(ref)
        else:
            external_or_system.append(ref)

    return {
        "embedded_resource_refs": embedded,
        "explicit_package_local_resource_refs": package_local,
        "external_or_system_resource_refs": external_or_system,
        "missing_package_local_resource_refs": missing_package_local,
    }


def inspect_brush(file: PathLike) -> Dict[str, Any]:
    path = Path(file)
    if not path.exists():
        return _result("NATIVE_OUTPUT_BLOCKED", reason_code="BRUSH_NOT_FOUND", errors=[str(path)])

    lfs = detect_lfs_pointer(path)
    if lfs.get("status") == "LFS_POINTER":
        return _result(
            "NATIVE_OUTPUT_BLOCKED",
            reason_code="BRUSH_IS_LFS_POINTER",
            evidence_state="VERIFIED_METADATA",
            sha256=_sha256_file(path),
            errors=["Git LFS pointer is not a native .brush package"],
            lfs=lfs,
        )

    if not zipfile.is_zipfile(path):
        return _result(
            "NATIVE_OUTPUT_BLOCKED",
            reason_code="INVALID_BRUSH_STRUCTURE",
            sha256=_sha256_file(path),
            errors=[".brush is not a ZIP-based native package"],
        )

    try:
        with zipfile.ZipFile(path) as archive_zip:
            names = [name for name in archive_zip.namelist() if not name.endswith("/")]
            if REQUIRED_BRUSH_MEMBER not in names:
                return _result(
                    "NATIVE_OUTPUT_BLOCKED",
                    reason_code="INVALID_BRUSH_STRUCTURE",
                    sha256=_sha256_file(path),
                    missing_members=[REQUIRED_BRUSH_MEMBER],
                    errors=["Required Brush.archive missing"],
                )

            archive_bytes = archive_zip.read(REQUIRED_BRUSH_MEMBER)
            internal_name = _brush_name_from_archive(archive_bytes)
            try:
                _, objects, root = _decode_archive(archive_bytes)
                metadata = _metadata_subset(root)
            except Exception as exc:
                return _result(
                    "NATIVE_OUTPUT_BLOCKED",
                    reason_code="BRUSH_ARCHIVE_UNSUPPORTED",
                    internal_name=internal_name,
                    sha256=_sha256_file(path),
                    errors=[str(exc)],
                    zip_members=names,
                )

            refs = sorted(_collect_resource_refs(objects, root))
            ref_state = _classify_resource_refs(refs, names)
            missing_local = ref_state["missing_package_local_resource_refs"]

            if missing_local:
                return _result(
                    "NATIVE_OUTPUT_BLOCKED",
                    reason_code="MISSING_PACKAGE_LOCAL_NATIVE_RESOURCE",
                    internal_name=internal_name,
                    sha256=_sha256_file(path),
                    missing_members=missing_local,
                    errors=["One or more explicit package-local Shape/Grain/Texture references are missing"],
                    metadata=metadata,
                    resource_refs=refs,
                    **ref_state,
                    zip_members=names,
                )

            external_refs = ref_state["external_or_system_resource_refs"]
            if external_refs:
                resource_check = "EXTERNAL_OR_SYSTEM_REFS_RECORDED"
            elif ref_state["embedded_resource_refs"]:
                resource_check = "EMBEDDED_REFS_RESOLVED"
            else:
                resource_check = "NO_FILE_REFS_FOUND"

            return _result(
                "NATIVE_STRUCTURE_PASS",
                reason_code="BRUSH_STRUCTURE_VALID",
                evidence_state="VERIFIED_METADATA",
                internal_name=internal_name,
                sha256=_sha256_file(path),
                member_count=1,
                metadata=metadata,
                resource_refs=refs,
                resource_reference_check=resource_check,
                external_resource_validation="NOT_TARGET_SOFTWARE_VALIDATED" if external_refs else "NOT_REQUIRED",
                **ref_state,
                zip_members=names,
                structural_validation="PACKAGE_STRUCTURE_ONLY",
            )
    except Exception as exc:
        return _result(
            "NATIVE_OUTPUT_BLOCKED",
            reason_code="BRUSH_INSPECTION_FAILED",
            sha256=_sha256_file(path),
            errors=[str(exc)],
        )


def inspect_brushset(file: PathLike) -> Dict[str, Any]:
    path = Path(file)
    if not path.exists():
        return _result("NATIVE_OUTPUT_BLOCKED", reason_code="BRUSHSET_NOT_FOUND", errors=[str(path)])

    lfs = detect_lfs_pointer(path)
    if lfs.get("status") == "LFS_POINTER":
        return _result(
            "NATIVE_OUTPUT_BLOCKED",
            reason_code="BRUSHSET_IS_LFS_POINTER",
            evidence_state="VERIFIED_METADATA",
            sha256=_sha256_file(path),
            errors=["Git LFS pointer is not a native .brushset"],
            lfs=lfs,
        )

    if not zipfile.is_zipfile(path):
        return _result(
            "NATIVE_OUTPUT_BLOCKED",
            reason_code="INVALID_BRUSHSET_STRUCTURE",
            sha256=_sha256_file(path),
            errors=[".brushset is not a ZIP-based native package"],
        )

    try:
        with zipfile.ZipFile(path) as archive_zip:
            names = archive_zip.namelist()
            if "brushset.plist" not in names:
                return _result(
                    "NATIVE_OUTPUT_BLOCKED",
                    reason_code="INVALID_BRUSHSET_STRUCTURE",
                    sha256=_sha256_file(path),
                    missing_members=["brushset.plist"],
                    errors=["brushset.plist missing"],
                )

            plist_data = plistlib.loads(archive_zip.read("brushset.plist"))
            order = plist_data.get("brushes", []) if isinstance(plist_data, dict) else []
            set_name = plist_data.get("name") if isinstance(plist_data, dict) else None
            if not isinstance(order, list):
                return _result(
                    "NATIVE_OUTPUT_BLOCKED",
                    reason_code="INVALID_BRUSHSET_PLIST",
                    sha256=_sha256_file(path),
                    errors=["brushset.plist 'brushes' is not a list"],
                )

            archive_dirs = {
                name.split("/", 1)[0]
                for name in names
                if name.count("/") == 1 and name.endswith("/Brush.archive")
            }
            declared = [str(member) for member in order]
            declared_set = set(declared)
            missing = sorted(member for member in declared if member not in archive_dirs)
            extra = sorted(member for member in archive_dirs if member not in declared_set)

            members = []
            for member_id in declared:
                archive_path = f"{member_id}/Brush.archive"
                members.append({
                    "member_id": member_id,
                    "internal_name": _brush_name_from_archive(archive_zip.read(archive_path)) if archive_path in names else None,
                })

            if missing or extra:
                return _result(
                    "NATIVE_OUTPUT_BLOCKED",
                    reason_code="BRUSHSET_MEMBER_SET_MISMATCH",
                    internal_name=set_name,
                    sha256=_sha256_file(path),
                    member_count=len(declared),
                    missing_members=missing,
                    extra_members=extra,
                    errors=["brushset.plist member IDs and packaged Brush.archive directories differ"],
                    members=members,
                    declared_order=declared,
                )

            return _result(
                "NATIVE_STRUCTURE_PASS",
                reason_code="BRUSHSET_STRUCTURE_VALID",
                evidence_state="VERIFIED_METADATA",
                internal_name=set_name,
                sha256=_sha256_file(path),
                member_count=len(declared),
                members=members,
                declared_order=declared,
                structural_validation="PACKAGE_STRUCTURE_ONLY",
            )
    except Exception as exc:
        return _result(
            "NATIVE_OUTPUT_BLOCKED",
            reason_code="BRUSHSET_INSPECTION_FAILED",
            sha256=_sha256_file(path),
            errors=[str(exc)],
        )


def resolve_lfs_asset(source: PathLike) -> Dict[str, Any]:
    path = Path(source)
    if not path.exists():
        return _result("LFS_RESOLUTION_BLOCKED", reason_code="LFS_SOURCE_NOT_FOUND", errors=[str(path)])

    state = detect_lfs_pointer(path)
    if state.get("status") != "LFS_POINTER":
        return _result(
            "NATIVE_METADATA_PASS",
            reason_code="LFS_RESOLUTION_NOT_REQUIRED",
            evidence_state="VERIFIED_METADATA",
            sha256=_sha256_file(path),
            resolved_path=str(path),
            was_lfs_pointer=False,
        )

    try:
        root = subprocess.run(
            ["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        relative = os.path.relpath(path.resolve(), Path(root).resolve())
        subprocess.run(
            ["git", "-C", root, "lfs", "pull", "--include", relative, "--exclude", ""],
            capture_output=True,
            text=True,
            check=True,
        )
        after = detect_lfs_pointer(path)
        if after.get("status") == "LFS_POINTER":
            return _result(
                "LFS_RESOLUTION_BLOCKED",
                reason_code="LFS_OBJECT_STILL_POINTER",
                errors=["git lfs pull completed but file is still a pointer"],
                lfs=after,
            )
        return _result(
            "NATIVE_METADATA_PASS",
            reason_code="LFS_ASSET_RESOLVED",
            evidence_state="VERIFIED_METADATA",
            sha256=_sha256_file(path),
            resolved_path=str(path),
            was_lfs_pointer=True,
        )
    except Exception as exc:
        return _result(
            "LFS_RESOLUTION_BLOCKED",
            reason_code="LFS_RUNTIME_UNAVAILABLE_OR_PULL_FAILED",
            errors=[str(exc)],
            lfs=state,
        )


def _rewrite_zip_member(source: Path, output: Path, member: str, replacement: bytes) -> None:
    with zipfile.ZipFile(source, "r") as src, zipfile.ZipFile(output, "w") as dst:
        for info in src.infolist():
            data = replacement if info.filename == member else src.read(info.filename)
            new_info = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            new_info.compress_type = info.compress_type
            new_info.comment = info.comment
            new_info.extra = info.extra
            new_info.internal_attr = info.internal_attr
            new_info.external_attr = info.external_attr
            new_info.create_system = info.create_system
            dst.writestr(new_info, data)


def derive_or_build_brush(base: PathLike, spec: Dict[str, Any], output: PathLike) -> Dict[str, Any]:
    base_path = Path(base)
    output_path = Path(output)
    inspection = inspect_brush(base_path)
    if inspection.get("status") != "NATIVE_STRUCTURE_PASS":
        return _result(
            "NATIVE_BUILD_BLOCKED",
            reason_code="BASE_BRUSH_VALIDATION_FAILED",
            errors=["Base brush failed native structural inspection"] + inspection.get("errors", []),
        )

    operation = str(spec.get("operation", "KEEP")).upper()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if operation in {"KEEP", "COPY"} and not spec.get("metadata_patch") and not spec.get("internal_name"):
        shutil.copy2(base_path, output_path)
        checked = inspect_brush(output_path)
        checked["build_operation"] = operation
        return checked

    if operation not in {"ADJUST", "DERIVE", "NEW"}:
        return _result(
            "NATIVE_BUILD_BLOCKED",
            reason_code="UNSUPPORTED_BUILD_OPERATION",
            errors=[f"Unsupported operation: {operation}"],
        )

    if operation == "NEW" and not spec.get("allow_new_from_validated_base"):
        return _result(
            "NATIVE_BUILD_BLOCKED",
            reason_code="NEW_REQUIRES_VALIDATED_BASE",
            errors=["NEW requires an explicitly validated native base or external format-specific builder"],
        )

    try:
        with zipfile.ZipFile(base_path) as archive_zip:
            archive = archive_zip.read(REQUIRED_BRUSH_MEMBER)
        payload, objects, root = _decode_archive(archive)
        patch = spec.get("metadata_patch") or {}
        unknown = sorted(set(patch) - SAFE_ARCHIVE_PATCH_FIELDS)
        if unknown:
            return _result(
                "NATIVE_BUILD_BLOCKED",
                reason_code="UNSAFE_ARCHIVE_PATCH_FIELD",
                errors=[f"Unsafe/unrecognized Brush.archive patch fields: {unknown}"],
            )

        for key, value in patch.items():
            if not isinstance(value, (int, float, bool, str)):
                return _result(
                    "NATIVE_BUILD_BLOCKED",
                    reason_code="NON_SCALAR_ARCHIVE_PATCH_VALUE",
                    errors=[f"Non-scalar patch value for {key}"],
                )
            root[key] = value

        name = spec.get("internal_name")
        if name:
            name_ref = root.get("name")
            if isinstance(name_ref, plistlib.UID) and 0 <= name_ref.data < len(objects):
                objects[name_ref.data] = str(name)
            elif isinstance(name_ref, str):
                root["name"] = str(name)
            else:
                return _result(
                    "NATIVE_BUILD_BLOCKED",
                    reason_code="INTERNAL_NAME_PATCH_UNSUPPORTED",
                    errors=["Could not safely update internal brush name"],
                )

        rebuilt = plistlib.dumps(payload, fmt=plistlib.FMT_BINARY, sort_keys=False)
        _rewrite_zip_member(base_path, output_path, REQUIRED_BRUSH_MEMBER, rebuilt)
        checked = inspect_brush(output_path)
        checked["build_operation"] = operation
        checked["build_evidence_state"] = "PROPOSED"
        return checked
    except Exception as exc:
        return _result("NATIVE_BUILD_FAILED", reason_code="BRUSH_BUILD_EXCEPTION", errors=[str(exc)])


def _unique_member_id() -> str:
    return str(uuid.uuid4()).upper()


def build_brushset(
    brush_files: Sequence[PathLike],
    output: PathLike,
    set_name: str = "Brush Creator Studio",
) -> Dict[str, Any]:
    if not brush_files:
        return _result("NATIVE_BUILD_FAILED", reason_code="NO_BRUSH_FILES", errors=["No brush files supplied"])

    inspections = [inspect_brush(path) for path in brush_files]
    failed = [result for result in inspections if result.get("status") != "NATIVE_STRUCTURE_PASS"]
    if failed:
        return _result(
            "NATIVE_BUILD_BLOCKED",
            reason_code="SOURCE_BRUSH_VALIDATION_FAILED",
            errors=["At least one brush failed structural validation"],
            failed_brushes=failed,
        )

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    member_ids = [_unique_member_id() for _ in brush_files]

    try:
        with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as out_zip:
            out_zip.writestr(
                "brushset.plist",
                plistlib.dumps({"brushes": member_ids, "name": set_name}, fmt=plistlib.FMT_XML),
            )
            for brush, member_id in zip(brush_files, member_ids):
                with zipfile.ZipFile(brush) as src:
                    for info in src.infolist():
                        if info.filename.endswith("/") or info.filename.startswith("__MACOSX/"):
                            continue
                        out_zip.writestr(f"{member_id}/{info.filename}", src.read(info.filename))
        checked = inspect_brushset(output_path)
        checked["source_brush_names"] = [item.get("internal_name") for item in inspections]
        return checked
    except Exception as exc:
        return _result("NATIVE_BUILD_FAILED", reason_code="BRUSHSET_BUILD_EXCEPTION", errors=[str(exc)])


def validate_native_family(brushes: Sequence[PathLike], brushset: PathLike) -> Dict[str, Any]:
    brush_results = [inspect_brush(path) for path in brushes]
    set_result = inspect_brushset(brushset)
    errors = []

    if any(result.get("status") != "NATIVE_STRUCTURE_PASS" for result in brush_results):
        errors.append("One or more individual .brush files failed structural validation")
    if set_result.get("status") != "NATIVE_STRUCTURE_PASS":
        errors.append(".brushset failed structural validation")

    brush_names = [result.get("internal_name") for result in brush_results if result.get("internal_name")]
    set_names = [member.get("internal_name") for member in set_result.get("members", []) if member.get("internal_name")]
    brush_counter = Counter(brush_names)
    set_counter = Counter(set_names)
    missing = sorted((brush_counter - set_counter).elements())
    extra = sorted((set_counter - brush_counter).elements())

    if len(brush_results) != set_result.get("member_count"):
        errors.append("Individual brush count != brushset member count")
    if missing or extra:
        errors.append("Individual brush names != brushset member names")

    return _result(
        "NATIVE_STRUCTURE_PASS" if not errors else "FAMILY_VALIDATION_FAILED",
        reason_code="NATIVE_FAMILY_VALID" if not errors else "NATIVE_FAMILY_SET_MISMATCH",
        evidence_state="VERIFIED_METADATA" if not errors else "UNVERIFIED",
        member_count=set_result.get("member_count"),
        missing_members=missing,
        extra_members=extra,
        errors=errors,
        individual_brush_count=len(brush_results),
        brush_names=brush_names,
        brushset_names=set_names,
        count_consistent=(len(brush_results) == set_result.get("member_count")),
        name_multiset_consistent=(brush_counter == set_counter),
    )


def _validate_xlsx_container(path: Path) -> Tuple[bool, Optional[str]]:
    if not zipfile.is_zipfile(path):
        return False, "Project XLSX is not a valid OOXML ZIP container"
    try:
        with zipfile.ZipFile(path) as archive_zip:
            names = set(archive_zip.namelist())
            required = {"[Content_Types].xml", "xl/workbook.xml"}
            missing = sorted(required - names)
            if missing:
                return False, f"Project XLSX missing required OOXML members: {missing}"
    except Exception as exc:
        return False, str(exc)
    return True, None


def _normalized_name_set(values: Sequence[str], label: str) -> Tuple[Optional[Set[str]], Optional[str]]:
    if values is None:
        return None, f"{label} is unavailable"
    cleaned = [str(value).strip() for value in values if str(value).strip()]
    if not cleaned:
        return None, f"{label} is empty"
    return set(cleaned), None


def validate_delivery_zip(
    zip_path: PathLike,
    expected_native_brush_names: Sequence[str],
    xlsx_reference_names: Sequence[str],
) -> Dict[str, Any]:
    """Mandatory four-way set validation for Mode B delivery."""
    path = Path(zip_path)
    if not path.exists() or not zipfile.is_zipfile(path):
        return _result("PACKAGE_VALIDATION_FAILED", reason_code="DELIVERY_ZIP_INVALID", errors=["ZIP missing or invalid"])

    expected_set, expected_error = _normalized_name_set(expected_native_brush_names, "Expected Native Brush Set")
    if expected_error:
        return _result("PACKAGE_VALIDATION_FAILED", reason_code="EXPECTED_NATIVE_SET_UNAVAILABLE", errors=[expected_error])

    refs_set, refs_error = _normalized_name_set(xlsx_reference_names, "XLSX Referenced Brush Set")
    if refs_error:
        return _result("PACKAGE_VALIDATION_FAILED", reason_code="XLSX_REFERENCE_SET_UNAVAILABLE", errors=[refs_error])

    errors = []
    reason_code: Optional[str] = None

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        try:
            with zipfile.ZipFile(path) as delivery_zip:
                delivery_zip.extractall(temp_path)
                extracted_files = [temp_path / name for name in delivery_zip.namelist() if not name.endswith("/")]
        except Exception as exc:
            return _result("PACKAGE_VALIDATION_FAILED", reason_code="DELIVERY_ZIP_REOPEN_FAILED", errors=[str(exc)])

        brushes = [file for file in extracted_files if file.suffix == ".brush"]
        brushsets = [file for file in extracted_files if file.suffix == ".brushset"]
        xlsx_files = [file for file in extracted_files if file.suffix.lower() == ".xlsx"]

        if not brushes:
            errors.append("No .brush files in delivery ZIP")
            reason_code = reason_code or "DELIVERED_BRUSH_FILES_MISSING"
        if len(brushsets) != 1:
            errors.append("Delivery ZIP must contain exactly one .brushset")
            reason_code = reason_code or "BRUSHSET_CARDINALITY_INVALID"
        if len(xlsx_files) != 1:
            errors.append("Delivery ZIP must contain exactly one project XLSX")
            reason_code = reason_code or "XLSX_CARDINALITY_INVALID"

        if len(xlsx_files) == 1:
            xlsx_ok, xlsx_error = _validate_xlsx_container(xlsx_files[0])
            if not xlsx_ok:
                errors.append(xlsx_error or "Project XLSX structure invalid")
                reason_code = reason_code or "XLSX_STRUCTURE_INVALID"

        brush_results = [inspect_brush(brush) for brush in brushes]
        failed_brushes = [result for result in brush_results if result.get("status") != "NATIVE_STRUCTURE_PASS"]
        if failed_brushes:
            errors.append("One or more delivered .brush files failed native structural validation")
            reason_code = reason_code or "DELIVERED_BRUSH_STRUCTURE_INVALID"

        delivered_names = [
            result.get("internal_name")
            for result in brush_results
            if result.get("status") == "NATIVE_STRUCTURE_PASS" and result.get("internal_name")
        ]
        delivered_set = set(delivered_names)

        if len(delivered_names) != len(brushes):
            errors.append("One or more delivered brushes lack a validated internal name")
            reason_code = reason_code or "DELIVERED_BRUSH_NAME_UNAVAILABLE"
        if len(delivered_set) != len(delivered_names):
            errors.append("Duplicate delivered brush internal names detected")
            reason_code = reason_code or "DUPLICATE_DELIVERED_BRUSH_NAME"

        family = None
        brushset_set: Set[str] = set()
        if brushes and len(brushsets) == 1:
            family = validate_native_family(brushes, brushsets[0])
            if family.get("status") != "NATIVE_STRUCTURE_PASS":
                errors.extend(family.get("errors", []))
                reason_code = reason_code or "NATIVE_FAMILY_SET_MISMATCH"
            brushset_set = {name for name in family.get("brushset_names", []) if name}

        set_map = {
            "expected_native": sorted(expected_set),
            "delivered_brush": sorted(delivered_set),
            "brushset_members": sorted(brushset_set),
            "xlsx_references": sorted(refs_set),
        }
        set_consistent = expected_set == delivered_set == brushset_set == refs_set

        if not set_consistent:
            errors.append(
                "Expected Native Brush Set, Delivered .brush Set, Brushset Member Set, and XLSX Referenced Brush Set are not exactly equal"
            )
            reason_code = reason_code or "DELIVERY_SET_MISMATCH"

        return _result(
            "PACKAGE_PASS" if not errors else "PACKAGE_VALIDATION_FAILED",
            reason_code="FOUR_WAY_SET_CONSISTENT" if not errors else reason_code,
            evidence_state="VERIFIED_METADATA" if not errors else "UNVERIFIED",
            sha256=_sha256_file(path),
            member_count=family.get("member_count") if family else None,
            errors=errors,
            expected_native_brush_count=len(expected_set),
            delivered_brush_count=len(brushes),
            delivered_distinct_name_count=len(delivered_set),
            brushset_member_count=family.get("member_count") if family else None,
            brushset_distinct_name_count=len(brushset_set),
            xlsx_referenced_distinct_count=len(refs_set),
            set_consistent=set_consistent,
            sets=set_map,
            full_pass=False,
            target_software_validation="NATIVE_VALIDATION_NOT_RUN",
            full_pass_reason="Real Procreate import/drawing test not executed by this structural runtime.",
        )


def _load_json_list(path: PathLike, label: str) -> Sequence[str]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be a JSON array of brush-name strings")
    if not value:
        raise ValueError(f"{label} must not be empty")
    return value


def _cli() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    cmd = sub.add_parser("inspect-brush")
    cmd.add_argument("file")
    cmd = sub.add_parser("inspect-brushset")
    cmd.add_argument("file")
    cmd = sub.add_parser("detect-lfs")
    cmd.add_argument("file")
    cmd = sub.add_parser("resolve-lfs")
    cmd.add_argument("file")
    cmd = sub.add_parser("build-brushset")
    cmd.add_argument("output")
    cmd.add_argument("brushes", nargs="+")
    cmd.add_argument("--name", default="Brush Creator Studio")
    cmd = sub.add_parser("validate-family")
    cmd.add_argument("brushset")
    cmd.add_argument("brushes", nargs="+")
    cmd = sub.add_parser("validate-zip")
    cmd.add_argument("zip")
    cmd.add_argument("--expected-json", required=True)
    cmd.add_argument("--refs-json", required=True)

    args = parser.parse_args()

    if args.cmd == "inspect-brush":
        result = inspect_brush(args.file)
    elif args.cmd == "inspect-brushset":
        result = inspect_brushset(args.file)
    elif args.cmd == "detect-lfs":
        result = detect_lfs_pointer(args.file)
    elif args.cmd == "resolve-lfs":
        result = resolve_lfs_asset(args.file)
    elif args.cmd == "build-brushset":
        result = build_brushset(args.brushes, args.output, args.name)
    elif args.cmd == "validate-family":
        result = validate_native_family(args.brushes, args.brushset)
    else:
        try:
            expected = _load_json_list(args.expected_json, "expected-json")
            refs = _load_json_list(args.refs_json, "refs-json")
            result = validate_delivery_zip(args.zip, expected, refs)
        except Exception as exc:
            result = _result("PACKAGE_VALIDATION_FAILED", reason_code="VALIDATION_INPUT_INVALID", errors=[str(exc)])

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result.get("status") in PASS_STATUSES else 2


if __name__ == "__main__":
    raise SystemExit(_cli())
