# Runtime Contract — $brush-creator-studio V2.0.0

This file is the **single Acceptance / Gate Source** for the repository runtime.

- `SKILL.md` defines the V2.0 execution chain and failure behavior.
- `KB-MANIFEST.json` defines V2.0 canonical routes plus optional extensions.
- Other documentation must not redefine acceptance gates.

## 1. Evidence states

- `VERIFIED` — real target-software import/drawing validation or an equivalent validated target-software workflow.
- `VERIFIED_METADATA` — native package/metadata structurally parsed and tied to a source hash; not hand-tested.
- `INFERRED` — supported by artwork/process evidence, not native-tested.
- `PROPOSED` — recommended role/setting/build change.
- `UNVERIFIED` — insufficient evidence.

Discovery state:
- `PENDING_VALIDATION`

## 2. Canonical runtime statuses

Knowledge / routing:
- `KB_UNAVAILABLE`
- `KB_INCOMPLETE`
- `KB_READ_FAILED`
- `MODE_UNSUPPORTED`
- `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`

Candidate / quantity:
- `PENDING_VALIDATION`
- `PROVISIONAL_COUNT`
- `FINAL_COUNT`
- `QUANTITY_DECISION_BLOCKED`
- `UNDERCOVERAGE_REVIEW_REQUIRED`

Native / package:
- `NATIVE_METADATA_PASS`
- `NATIVE_STRUCTURE_PASS`
- `LFS_POINTER`
- `LFS_RESOLUTION_BLOCKED`
- `NATIVE_OUTPUT_BLOCKED`
- `NATIVE_BUILD_BLOCKED`
- `NATIVE_BUILD_FAILED`
- `NATIVE_VALIDATION_NOT_RUN`
- `FAMILY_VALIDATION_FAILED`
- `DELIVERY_TEMPLATE_MISSING`
- `PACKAGE_VALIDATION_FAILED`
- `PACKAGE_PASS`
- `FULL_PASS`

Technical implementation details must use `reason_code` and `errors`; do not create ad-hoc top-level statuses for every parser/transport error.

Examples:
- `status = NATIVE_OUTPUT_BLOCKED`, `reason_code = BINARY_MATERIALIZATION_UNAVAILABLE`
- `status = NATIVE_OUTPUT_BLOCKED`, `reason_code = INVALID_BRUSH_STRUCTURE`
- `status = PACKAGE_VALIDATION_FAILED`, `reason_code = XLSX_REFERENCE_SET_UNAVAILABLE`

## 3. FINAL_COUNT hard gate

`FINAL_COUNT` is allowed only after all pass:
1. Process Stage Coverage
2. Material Coverage
3. Object-specific Coverage
4. Required Brush Role Coverage
5. Candidate Validation
6. Specialization Review
7. Merge Eligibility
8. Redundancy Check
9. Undercoverage Review
10. Complexity Sanity

Complexity bands are QA triggers, not minimum brush quotas.

## 4. Required Role rule

Each `REQUIRED` Brush Role must have exactly one defensible route:
- **Independent Native Brush**, or
- **Explicit `MERGE_PASS` → Shared Native Brush**.

Every run must output `ROLE_TO_NATIVE_MATRIX` containing at least:
`role_id / stage / object_material / native_brush_name / classification / merge_state / merge_target / evidence_state`.

`Role Count >= Distinct Native Brush Count`.

If compression is large, every collapsed Role must carry its own `MERGE_PASS` evidence. Missing merge evidence returns `UNDERCOVERAGE_REVIEW_REQUIRED`.

## 5. Candidate validation gate

- Filename / folder / `purpose_hint` never establishes native behavior.
- `PENDING_VALIDATION` must not become `NEW` solely because native inspection is unavailable.
- Prefer `BRUSH-CAPABILITY-REGISTRY.json` entries whose source hashes still match.
- A changed source hash invalidates prior capability evidence until revalidated.
- Validate shortlisted candidates instead of scanning full libraries.

Candidate validation is not complete until the candidate has a real local binary path or an already-valid hash-bound capability record whose binary is not required for the current output operation.

## 6. Binary Materialization Gate — Mode B

Before native inspection, derivation, build, or template use, all decision-critical binary assets must exist as real local files:
- shortlisted `.brush` candidates that may become KEEP / ADJUST / DERIVE bases;
- routed `.brushset` assets when shortlisted members are needed;
- the canonical Procreate V2 XLSX template.

Connector text, metadata, a base64 preview, a repository path string, or a Git LFS pointer does **not** satisfy this gate.

Materialization order:
1. an already-real local file path;
2. the GitHub Actions artifact bridge declared by `KB-MANIFEST.json > extensions.binary_materialization_bridge`;
3. local Git LFS resolution inside a real checkout, only for the required routed asset.

The bridge artifact should provide branch-scoped binary bundles and a SHA256 manifest. For preferred brushsets it should also pre-extract declared members into standalone `.brush` files so hash-bound Capability Registry entries can become usable build bases without requiring the calling environment to re-fetch member bytes.

For `mixed`, both branch artifacts may be required.

Only after all declared materialization routes fail may the run return:
- `status = NATIVE_OUTPUT_BLOCKED`
- `reason_code = BINARY_MATERIALIZATION_UNAVAILABLE`

If an artifact is downloaded but its expected binary file is missing, corrupt, still a Git LFS pointer, or SHA-mismatched:
- `status = NATIVE_OUTPUT_BLOCKED`
- `reason_code = BINARY_MATERIALIZATION_INTEGRITY_FAILED`

`BINARY_MATERIALIZATION_UNAVAILABLE` is therefore a terminal fallback, not the first response to connector binary limitations.

## 7. Git LFS gate

A Git LFS pointer is not a native `.brushset`.

Detect pointer text before native inspection. Resolve LFS only when the shortlisted candidate can materially affect Role coverage/quantity, unless the branch artifact bridge has already supplied the real binary.

If local LFS resolution is attempted and unavailable:
- `status = LFS_RESOLUTION_BLOCKED`
- keep the candidate `PENDING_VALIDATION` when relevant;
- if the GitHub Actions bridge is declared and has not yet been attempted, attempt it before converting the run to terminal binary-materialization failure.

## 8. Individual `.brush` structure gate

A `.brush` may reach `NATIVE_STRUCTURE_PASS` only when:
- the file is a ZIP-based native package;
- `Brush.archive` exists and is parseable;
- internal brush name can be read when present;
- any **explicit package-local** Shape / Grain / Texture path reference resolves to an actual package member.

Procreate archives may also contain **bare resource identifiers** such as `Brush-Preset-*`, `Brush-Artery-*`, `Brush-Pocket-*`, `Gouache-Wash.jpg`, `Acrylic-Square.jpg`, or similar names that can refer to Procreate/system/library assets rather than files embedded in the `.brush` ZIP. A bare filename that is not present in the package must therefore be recorded as `external_or_system_resource_refs`; its absence alone is **not** package-corruption evidence and must not fail structural validation.

Hard failure applies only when a reference is demonstrably package-local (for example a path-qualified relative reference) and that referenced member is missing:
- `status = NATIVE_OUTPUT_BLOCKED`
- `reason_code = MISSING_PACKAGE_LOCAL_NATIVE_RESOURCE`

For external/system refs, structural validation may still pass as `VERIFIED_METADATA`, but the result must record:
- `external_or_system_resource_refs`
- `external_resource_validation = NOT_TARGET_SOFTWARE_VALIDATED`

This distinction prevents false negatives while preserving the boundary that only a real Procreate import/drawing test can establish `VERIFIED` / `FULL_PASS`.

## 9. `.brushset` structure gate

A `.brushset` may reach `NATIVE_STRUCTURE_PASS` only when:
- `brushset.plist` exists and parses;
- declared member IDs have `Brush.archive` packages;
- `missing_members` is empty;
- `extra_members` is empty.

Any missing **or extra** member fails validation:
- `status = NATIVE_OUTPUT_BLOCKED`
- `reason_code = BRUSHSET_MEMBER_SET_MISMATCH`

If a brushset member is selected for KEEP / ADJUST / DERIVE, it must be materialized as a standalone `.brush` before `derive_or_build_brush()` is called. The repository helper for this is `runtime/binary_materialization.py`.

## 10. Native Build gate — Mode B

Required order:
1. Final/Provisional Role Set
2. `ROLE_TO_NATIVE_MATRIX`
3. Binary Materialization Gate
4. Native candidate inspection / classification
5. Build/copy every distinct final `.brush`
6. Build one complete `.brushset`
7. Validate native family
8. Load canonical V2 XLSX template from a real local binary path
9. Generate project XLSX using actual delivered brush names
10. Build final ZIP
11. Reopen ZIP and validate again

Do not create XLSX first and fill native files later.

`runtime/native_runtime.py` is the canonical Procreate native structure/build/package validator.
`runtime/binary_materialization.py` is the transport/extraction helper.

Machine-readable failure cannot be overridden by prose.

## 11. Four-way delivery set consistency

`validate_delivery_zip()` must receive both:
- **Expected Native Brush Set** — derived from `ROLE_TO_NATIVE_MATRIX`;
- **XLSX Referenced Brush Set** — extracted/validated from the project workbook.

Before `PACKAGE_PASS`, exact set equality is required:

`Expected Native Brush Set`
=
`Delivered .brush Set`
=
`Brushset Member Set`
=
`XLSX Referenced Brush Set`

Count equality alone is insufficient.

XLSX reference validation is mandatory. If the reference set cannot be extracted or validated:
- `status = PACKAGE_VALIDATION_FAILED`
- `reason_code = XLSX_REFERENCE_SET_UNAVAILABLE`

Any set mismatch:
- `status = PACKAGE_VALIDATION_FAILED`
- `reason_code = DELIVERY_SET_MISMATCH`

## 12. Mode B artifact contract

Final ZIP must contain:
- every expected final native `.brush`;
- exactly one complete final `.brushset`;
- exactly one project workflow XLSX derived from `templates/Procreate/Procreate新笔刷绘画操作流程_V2.xlsx`.

Forbidden states:
- XLSX without `.brush`;
- `.brush` without `.brushset`;
- `.brushset` missing or adding unexpected native brushes;
- XLSX referencing a non-expected/non-delivered brush;
- placeholder brush names;
- renamed fake native files;
- a Git LFS pointer substituted for an actual `.brushset`;
- a bridge artifact declared ready while required branch binaries are absent.

## 13. PACKAGE_PASS vs FULL_PASS

`PACKAGE_PASS` means:
- required source/template binaries were successfully materialized;
- individual native package structures pass;
- native family member names and sets pass;
- expected/delivered/brushset/XLSX sets are exactly equal;
- final ZIP reopens and passes validation.

`PACKAGE_PASS` does **not** prove Procreate import success or drawing feel.

`FULL_PASS` additionally requires a real target-software import/drawing test. If not run, report `NATIVE_VALIDATION_NOT_RUN` in the validation details and never claim `FULL_PASS`.

## 14. Mode A / AB boundary

This repository does not currently contain an equivalent Photoshop `.abr` native builder, delivery template, native asset branch, or binary bridge.

Unless the Manifest explicitly declares a working external Photoshop native runtime:
- Mode A native delivery → `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`
- Mode AB full dual-native delivery → `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`

Analysis may continue. `.abr` must not be fabricated.

## 15. Acceptance invariant

No prose claim overrides machine-readable runtime output.

When narrative reasoning and runtime validation disagree, runtime validation controls package acceptance.
