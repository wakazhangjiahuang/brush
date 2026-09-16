# Runtime Contract — $brush-creator-studio Repository V2.1

This file is the **single Acceptance / Gate Source** for the GitHub runtime.  
`SKILL.md` defines execution order; `KB-MANIFEST.json` defines routing and paths. Other files must not redefine these gates.

## 1. Evidence states
- `VERIFIED` — real Procreate/Photoshop import/drawing validation or equivalent validated target-software workflow.
- `VERIFIED_METADATA` — native package/metadata structurally parsed and tied to a source hash; not hand-tested.
- `INFERRED` — supported by artwork/process evidence, not native-tested.
- `PROPOSED` — recommended setting/role/build change.
- `UNVERIFIED` — insufficient evidence.

Discovery-only state:
- `PENDING_VALIDATION`

## 2. Runtime status codes
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

Native:
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

## 3. Quantity hard gate
`FINAL_COUNT` is allowed only after all of the following pass:
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
- **A. Independent Native Brush**, or
- **B. Explicit `MERGE_PASS` → Shared Native Brush**.

The run must output a `ROLE_TO_NATIVE_MATRIX` containing at least:
`role_id / stage / object_material / native_brush_name / classification / merge_state / merge_target / evidence_state`.

`Role Count >= Distinct Native Brush Count`.

If compression is large (for example 14 Roles → 3 Brushes), every collapsed Role must carry its own `MERGE_PASS` evidence. Any missing merge evidence returns `UNDERCOVERAGE_REVIEW_REQUIRED`.

## 5. Candidate validation gate
- Filename / `purpose_hint` never establishes native behavior.
- `PENDING_VALIDATION` must not be converted to `NEW` solely because native inspection is unavailable.
- Prefer `BRUSH-CAPABILITY-REGISTRY.json` records whose source hash still matches.
- If a candidate source hash changed, its prior capability record is stale until revalidated.
- Shortlist native validation is preferred over full-library scanning.

## 6. Git LFS gate
A Git LFS pointer is not a native `.brushset`.

Before inspection, detect pointer text.  
Resolve LFS only when the shortlisted candidate can materially affect Role coverage/quantity.  
If resolution is unavailable, return `LFS_RESOLUTION_BLOCKED` and keep the candidate `PENDING_VALIDATION` when relevant.

## 7. Native Build gate — Mode B
Mode B build order:
1. Final/Provisional Role Set
2. Build/copy every distinct final `.brush`
3. Build one complete `.brushset`
4. Validate native family
5. Load canonical V2 XLSX template
6. Generate project XLSX using actual delivered brush names
7. Build final ZIP
8. Reopen ZIP and validate again

Do not create XLSX first and “fill in” brushes later.

`runtime/native_runtime.py` is the canonical Procreate native structure runtime. If its structural checks fail, natural-language reasoning cannot override the failure.

## 8. Native family count consistency
Before `PACKAGE_PASS`, all of these counts must agree:

`Delivered Individual Brush Count`
=
`Brushset Member Count`
=
`XLSX Referenced Distinct Brush Count`
=
`Final Distinct Native Brush Count`

The brush names must also match; count equality alone is insufficient.

Any mismatch returns `PACKAGE_VALIDATION_FAILED`.

## 9. Mode B artifact contract
Final ZIP must contain:
- every final native `.brush`;
- exactly one complete final `.brushset`;
- exactly one project workflow XLSX derived from `templates/Procreate/Procreate新笔刷绘画操作流程_V2.xlsx`.

Forbidden package states include:
- XLSX without `.brush`;
- `.brush` without `.brushset`;
- `.brushset` missing any final brush;
- XLSX referencing a non-delivered brush;
- placeholder brush names;
- renamed fake native files.

## 10. PACKAGE PASS vs FULL PASS
`PACKAGE_PASS` means:
- native ZIP/package structures parsed successfully;
- native family membership/count/name checks pass;
- project XLSX exists and references only delivered brush names;
- final ZIP reopens and passes structure/count validation.

`PACKAGE_PASS` does **not** prove Procreate drawing feel or import success.

`FULL_PASS` additionally requires a real target-software import/drawing test. If not run, report `NATIVE_VALIDATION_NOT_RUN` alongside structural results and do not claim FULL PASS.

## 11. Mode A / AB boundary
The current repository does not contain an equivalent Photoshop `.abr` builder, Photoshop delivery template, or Photoshop native asset branch.

Unless `KB-MANIFEST.json` explicitly declares a working external Photoshop native runtime dependency:
- Mode A native delivery → `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`
- Mode AB full dual-native delivery → `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`

Analysis may continue, but `.abr` must not be fabricated.

## 12. Acceptance invariant
No prose claim can override machine-readable native runtime output.  
When machine validation and narrative reasoning disagree, the machine validation status controls package acceptance.
