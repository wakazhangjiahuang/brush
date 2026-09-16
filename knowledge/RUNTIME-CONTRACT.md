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

Technical implementation details must use `reason_code` and `errors`; do not create ad-hoc top-level statuses for every parser error.

Examples:
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

## 6. Git LFS gate

A Git LFS pointer is not a native `.brushset`.

Detect pointer text before native inspection. Resolve LFS only when the shortlisted candidate can materially affect Role coverage/quantity.

If resolution is unavailable:
- `status = LFS_RESOLUTION_BLOCKED`
- keep the candidate `PENDING_VALIDATION` when relevant.

## 7. Individual `.brush` structure gate

A `.brush` may reach `NATIVE_STRUCTURE_PASS` only when:
- the file is a ZIP-based native package;
- `Brush.archive` exists and is parseable;
- internal brush name can be read when present;
- explicit Shape / Grain / Texture file references found in the archive resolve to actual package members.

If an explicit required native resource reference is missing:
- `status = NATIVE_OUTPUT_BLOCKED`
- `reason_code = MISSING_REFERENCED_NATIVE_RESOURCE`

Absence of an explicit file reference does **not** prove drawing behavior; it only means no missing referenced resource was detected.

## 8. `.brushset` structure gate

A `.brushset` may reach `NATIVE_STRUCTURE_PASS` only when:
- `brushset.plist` exists and parses;
- declared member IDs have `Brush.archive` packages;
- `missing_members` is empty;
- `extra_members` is empty.

Any missing **or extra** member fails validation:
- `status = NATIVE_OUTPUT_BLOCKED`
- `reason_code = BRUSHSET_MEMBER_SET_MISMATCH`

## 9. Native Build gate — Mode B

Required order:
1. Final/Provisional Role Set
2. `ROLE_TO_NATIVE_MATRIX`
3. Build/copy every distinct final `.brush`
4. Build one complete `.brushset`
5. Validate native family
6. Load canonical V2 XLSX template
7. Generate project XLSX using actual delivered brush names
8. Build final ZIP
9. Reopen ZIP and validate again

Do not create XLSX first and fill native files later.

`runtime/native_runtime.py` is the canonical Procreate native structure runtime. Machine-readable failure cannot be overridden by prose.

## 10. Four-way delivery set consistency

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

## 11. Mode B artifact contract

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
- renamed fake native files.

## 12. PACKAGE_PASS vs FULL_PASS

`PACKAGE_PASS` means:
- individual native package structures pass;
- native family member names and sets pass;
- expected/delivered/brushset/XLSX sets are exactly equal;
- final ZIP reopens and passes validation.

`PACKAGE_PASS` does **not** prove Procreate import success or drawing feel.

`FULL_PASS` additionally requires a real target-software import/drawing test. If not run, report `NATIVE_VALIDATION_NOT_RUN` in the validation details and never claim `FULL_PASS`.

## 13. Mode A / AB boundary

This repository does not currently contain an equivalent Photoshop `.abr` native builder, delivery template, or native asset branch.

Unless the Manifest explicitly declares a working external Photoshop native runtime:
- Mode A native delivery → `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`
- Mode AB full dual-native delivery → `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`

Analysis may continue. `.abr` must not be fabricated.

## 14. Acceptance invariant

No prose claim overrides machine-readable runtime output.

When narrative reasoning and runtime validation disagree, runtime validation controls package acceptance.
