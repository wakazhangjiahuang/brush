# $brush-creator-studio V1.0.0 → V1.1 Remote Resolver Patch

This is an additive patch. Preserve all existing V1.0.0 Mode A / Mode B / Mode AB logic, output contracts, schemas, validation rules, and the shared Artist Profile + Brush DNA single-source contract.

## Add to SKILL.md — Remote Knowledge Resolver

Before asking the user for existing brush libraries, illustrator workflow recordings, or persistent artist workflow information, use the connected GitHub capability to resolve the repository `wakazhangjiahuang/brush`.

Runtime order:

1. Read repository root `KB-MANIFEST.json` on the default branch.
2. Follow the manifest entrypoints exactly:
   - `knowledge/ARTIST-PROFILE.json`
   - `knowledge/PROCESS-REGISTRY.json`
   - `knowledge/BRUSH-REGISTRY.json`
   - `knowledge/RUNTIME-CONTRACT.md`
3. Treat the current user-uploaded artwork as the primary project evidence.
4. Select `cartoon` or `vintage` branch from artwork/process evidence; explicit user selection wins.
5. Load only relevant process media and candidate brushes, not the complete binary library.
6. Complete `Process DNA → Brush Function Clustering → Required Function Coverage Matrix` before deciding quantity.
7. Match relevant repository candidates, then validate candidate coverage as far as the available native evidence permits.
8. Use KEEP / ADJUST / DERIVE / NEW only after coverage analysis. If a relevant candidate exists but its behavior is not sufficiently validated, mark it `PENDING_VALIDATION`; lack of validation alone must never trigger `NEW`.
9. Run Merge / Redundancy Check before the Dynamic Quantity Decision.
10. Never infer native brush parameters from filenames. Filename-based fields are routing hints only.
11. Recognize Git LFS pointer files for `.brushset`; do not classify a small pointer blob as a damaged brushset.
12. If an unresolved `.brush` / `.brushset` candidate could materially change coverage or total quantity, use `PROVISIONAL_COUNT` or `QUANTITY_DECISION_BLOCKED`; do not claim `FINAL_COUNT`.
13. Existing repository data must not be requested from the user again unless GitHub access or the exact indexed asset is unavailable.
14. If the repository cannot be read, set `KB_UNAVAILABLE`; identify the missing path and fall back only to explicit local inputs.

## Quantity Decision Hard Gate

Brush quantity is an output of evidence and coverage analysis, never a preset target or preferred range.

Required sequence:

`Process DNA → Brush Function Clustering → Required Function Coverage Matrix → Existing Brush Matching → Existing Brush Validation → KEEP / ADJUST / DERIVE / NEW → Merge / Redundancy Check → Dynamic Quantity Decision`

Before `FINAL_COUNT` is allowed:

- every required brush-function slot must be documented;
- relevant existing candidates must be mapped to those slots;
- any unresolved candidate must be marked `PENDING_VALIDATION`;
- `NEW` must be justified by demonstrated lack of adequate existing coverage, not by inability to inspect a candidate;
- equivalent/redundant slots must be merged where one brush can cover them without material compromise;
- no unresolved repository asset may remain if it could materially change the classification or count.

Quantity states:

- `PROVISIONAL_COUNT` — working count before all quantity gates close;
- `FINAL_COUNT` — final dynamic count after the hard gate closes;
- `QUANTITY_DECISION_BLOCKED` — a required native asset cannot be resolved well enough to make a defensible final decision.

A provisional quantity must never be reported as the final dynamically determined quantity.

## Evidence labels

Every parameter/behavior claim must use one of:

- `VERIFIED` — extracted or validated in real target software/workflow;
- `INFERRED` — supported by artwork/process evidence but not software-tested;
- `PROPOSED` — new design recommendation;
- `UNVERIFIED` — insufficient evidence.

Do not present `INFERRED`, `PROPOSED`, or `UNVERIFIED` values as native Procreate/Photoshop facts.

## Native binary access boundary

- Individual `.brush` files stored directly in Git can be retrieved as binary/base64 by an appropriate GitHub file action.
- `.brushset` files in this repository are stored with Git LFS. Standard contents/blob reads may return the LFS pointer instead of the actual binary. Use registry metadata for routing and obtain/validate the native binary only through an LFS-capable path when required.
- If a relevant LFS-managed `.brushset` cannot be inspected and its internal brushes could change KEEP / ADJUST / DERIVE / NEW decisions, mark it `PENDING_VALIDATION` and do not claim `FINAL_COUNT`.
- A resolver PASS is not a software import PASS.

## Default user interaction after patch

Normal run: upload current artwork + invoke `$brush-creator-studio` + optionally specify A/B/AB.

The repository URL and persistent artist/brush data are part of the Skill contract and should not need to be re-entered each time.
