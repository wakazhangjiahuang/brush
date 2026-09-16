---
name: brush-creator-studio
description: Build and validate evidence-bound Procreate brush systems from current artwork using a Manifest-driven remote knowledge base, conditional candidate retrieval, native structure validation, and package count-consistency checks.
---

# $brush-creator-studio — Repository Runtime Contract Adapter

## 1. Purpose
This repository-side `SKILL.md` defines only execution order, decision boundaries, and failure behavior.  
Concrete paths and load policy come from `KB-MANIFEST.json`. Acceptance criteria and status codes come only from `knowledge/RUNTIME-CONTRACT.md`.

Optimization target: **Minimal Complete Production Set** — complete production coverage without redundant brushes. Never optimize for “the fewest possible brushes”.

## 2. Manifest-first boot
For every run:
1. Read only `KB-MANIFEST.json`.
2. Verify requested mode against `mode_capability`.
3. Follow `runtime_load_policy`; do not scan the full repository.
4. Current artwork is the highest-priority project evidence.
5. Do not request repository-resident assets from the user again unless the routed asset is unavailable.

`README.md`, `START-PROMPT.md`, `templates/README.md`, Git history, migration notes, and static reports are not runtime knowledge sources.

## 3. Conditional execution chain
`BOOT / Manifest`
→ `Current Artwork Audit`
→ `Artwork Complexity + Branch Routing`
→ `Core Rule Load`
→ `Stage Decomposition`
→ `Object / Material Map`
→ `Brush Role Inventory`
→ `Selected Process DNA`
→ `Candidate Registry Match`
→ `Shortlist Native Validation`
→ `KEEP / ADJUST / DERIVE / NEW`
→ `Specialization`
→ `Merge`
→ `Redundancy / Undercoverage`
→ `Dynamic Quantity Decision`
→ `ROLE_TO_NATIVE_MATRIX`
→ `Native Build`
→ `XLSX`
→ `Delivery QA`
→ `ZIP`

Do not load brush binaries, process videos, or the XLSX template during BOOT.

## 4. Artwork and process routing
Priority:
`CURRENT_ARTWORK > SELECTED_PROCESS_DNA > ARTIST_PROFILE`.

Choose `cartoon`, `vintage`, `mixed`, or `unknown` from current artwork evidence. Load only the selected Process DNA.  
Use `PROCESS-REGISTRY.json` process media only when artwork evidence is insufficient, conflicts with Process DNA, or a specific real workflow step must be confirmed.

## 5. Brush candidate retrieval
After required Brush Roles exist:
1. Read `BRUSH-REGISTRY.json` for discovery.
2. Read `BRUSH-CAPABILITY-REGISTRY.json` for reusable native evidence.
3. Shortlist at most the Manifest-defined candidate limit per Role.
4. Prefer verified capability records and individual `.brush` files before large LFS `.brushset` assets.
5. Resolve/inspect only shortlisted native files.

Filename, `purpose_hint`, folder name, or declared set count are discovery hints only.

## 6. Native evidence and classification
Use evidence states from the Runtime Contract.  
A candidate that has not been sufficiently inspected remains `PENDING_VALIDATION`; lack of access is not evidence for `NEW`.

Decide `KEEP / ADJUST / DERIVE / NEW` only after shortlist validation.

## 7. Specialization, Merge, and undercoverage
Run specialization before Merge.  
Apply `knowledge/MERGE-GATE.md`; technical ability to paint two tasks is not sufficient merge evidence.

Every REQUIRED Brush Role must map to:
- an independent Native Brush; or
- an explicit `MERGE_PASS` pointing to a shared Native Brush.

Always produce `ROLE_TO_NATIVE_MATRIX`. A large Role-to-brush compression requires explicit merge evidence for every collapsed Role. Missing merge evidence triggers `UNDERCOVERAGE_REVIEW_REQUIRED`.

Complexity bands are QA triggers, never fixed quantity targets.

## 8. Native runtime
For Mode B use only `runtime/native_runtime.py` for Procreate structural inspection/build/package validation when execution is available.

Git LFS pointer text is not native brush data. Resolve LFS only for shortlisted candidates that materially affect the decision.

Do not fake `.brush`, `.brushset`, or `.abr` by renaming arbitrary files.

## 9. Build order
Do not build the XLSX before native Brush Roles are resolved.

Required order:
1. Final/Provisional Role Set
2. Native `.brush` outputs
3. Complete `.brushset`
4. Load canonical XLSX template
5. Generate project XLSX using actual delivered native brush names
6. Reopen native family + ZIP and run delivery QA

## 10. Mode boundaries
Mode B: repository contains Procreate assets, V2 template, and native runtime.

Mode A / AB: this repository currently does not contain an equivalent Photoshop `.abr` native runtime/template/asset branch.  
If a native Photoshop delivery is requested and no external runtime dependency has been explicitly supplied by the Manifest, return `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE`. Never fabricate `.abr` delivery.

## 11. Acceptance
Do not duplicate acceptance rules here. Use `knowledge/RUNTIME-CONTRACT.md` as the single Acceptance/Gate Source.

If a routed file or capability is unavailable, return the exact Contract status instead of natural-language PASS guessing.
