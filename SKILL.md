---
name: brush-creator-studio
description: Create, validate, optimize, and package evidence-bound Procreate/Photoshop brush systems from current artwork plus the persistent GitHub brush knowledge base, with complete production-stage coverage, material-aware roles, native delivery checks, and project workflow documentation.
---

# $brush-creator-studio V2.0.0

## 1. Purpose

`$brush-creator-studio` converts current artwork into a production-ready brush system. The optimization target is **Minimal Complete Production Set**: complete stage/material/object coverage with no unjustified duplication or over-merging.

The current artwork is always the highest-priority project evidence.

Modes:
- **A = Photoshop** — analysis is supported; native `.abr` delivery requires an explicitly available Photoshop native runtime.
- **B = Procreate** — `.brush` + `.brushset` native delivery through the repository runtime.
- **AB = Dual analysis** — shares Artist Profile + Brush DNA; Procreate native delivery is available, Photoshop native delivery follows the capability boundary below.

## 2. V2.0 Manifest-first repository resolver

Repository: `wakazhangjiahuang/brush`.

For every run:
1. Read `KB-MANIFEST.json` first.
2. Resolve the V2.0 canonical fields: `entrypoints`, `process_dna`, `source_directories`, `resolver_policy`, and `routing`.
3. The optional `extensions` object may optimize conditional loading, native runtime, LFS handling, and artifact QA, but V2.0 execution must not depend on understanding those extensions.
4. Do not scan the full repository at startup.
5. Do not ask the user to re-upload repository-resident assets unless the exact routed asset cannot be resolved.

`knowledge/RUNTIME-CONTRACT.md` is the single Acceptance/Gate Source.

## 3. Required V2.0 execution chain

`Current Artwork Audit`
→ `Artwork Complexity Profile`
→ `Style / Color / Material DNA`
→ `Full Production Stage Decomposition`
→ `Process DNA`
→ `Object / Material Map`
→ `Brush Role Inventory`
→ `Required Role Coverage Matrix`
→ `Existing Brush Matching`
→ `Native Metadata / Capability Validation`
→ `KEEP / ADJUST / DERIVE / NEW`
→ `Brush Specialization Gate`
→ `Merge Eligibility Gate`
→ `Redundancy Check`
→ `Undercoverage Review`
→ `Complexity Sanity Check`
→ `Dynamic Quantity Decision`
→ `ROLE_TO_NATIVE_MATRIX`
→ `Native Brush Build`
→ `Native Delivery Gate`
→ `Project-specific XLSX`
→ `QA`
→ `ZIP`

Do not finalize quantity before Redundancy + Undercoverage + Complexity Sanity.

## 4. Production stages, materials, and roles

Use the manifest entrypoints for:
- `PROCESS-STAGE-TAXONOMY.json`
- `MATERIAL-TAXONOMY.json`
- `COMPLEXITY-RULES.json`
- `MERGE-GATE.md`

Each applicable production stage must be classified `REQUIRED / OPTIONAL / NOT_APPLICABLE`.

Separate:
`Production Stage → Required Behavior → Brush Role → Candidate → Delivered Native Brush`.

A visible specialist behavior (fur, dry brush, wet bleed, cloth, grain, foliage, decorative smooth line, fine cleanup, etc.) must not disappear merely because a general brush can technically approximate it.

## 5. Process routing

Priority:
`CURRENT_ARTWORK > SELECTED_PROCESS_DNA > ARTIST_PROFILE`.

Use `process_dna.cartoon` or `process_dna.vintage` from the V2.0 Manifest. For mixed work, inspect only the needed branch baselines.

Use `PROCESS-REGISTRY.json` media only when:
- current artwork evidence is insufficient;
- Process DNA conflicts with the artwork;
- a specific real workflow stage must be confirmed.

Process DNA is a baseline, not a replacement for the current artwork.

## 6. Candidate retrieval and native evidence

After required Brush Roles exist:
1. Resolve `entrypoints.brush_registry`.
2. Resolve `entrypoints.brush_capability_registry`.
3. Prefer capability records whose source hashes still match.
4. Shortlist the best candidates per Role; when Manifest extensions are understood, honor the configured maximum (currently 3).
5. Prefer suitable individual `.brush` candidates before downloading large LFS `.brushset` assets.
6. Inspect only shortlisted native candidates.

Filename, folder name, `purpose_hint`, and discovery hints are not VERIFIED capability evidence.

An unvalidated relevant candidate remains `PENDING_VALIDATION`; lack of native access does not justify `NEW`.

## 7. Classification, specialization, Merge, and undercoverage

Decide `KEEP / ADJUST / DERIVE / NEW` only after relevant candidate validation.

Run **Specialization before Merge**.

Every REQUIRED Brush Role must map to:
- an independent Native Brush; or
- an explicit `MERGE_PASS` pointing to a shared Native Brush.

Always output `ROLE_TO_NATIVE_MATRIX`.

Large compression (for example 14 roles → 3 native brushes) requires explicit merge evidence for every collapsed role. Missing evidence triggers `UNDERCOVERAGE_REVIEW_REQUIRED`.

Complexity bands are QA triggers, never fixed brush-count targets.

## 8. Procreate native runtime

For Mode B, if execution is available, use `runtime/native_runtime.py` from the Manifest extension.

Required responsibilities:
- detect Git LFS pointers before native inspection;
- inspect real `.brush/.brushset`;
- validate referenced package resources where readable;
- build/copy/derive supported native brushes;
- build one complete final `.brushset`;
- validate individual family membership;
- validate final ZIP against the expected native brush set and XLSX reference set.

Git LFS pointer text is never native brushset content.

Do not fake `.brush`, `.brushset`, or `.abr` by changing extensions.

## 9. Mode B build order

1. Final/Provisional Role Set
2. `ROLE_TO_NATIVE_MATRIX`
3. Build/copy every distinct final `.brush`
4. Build one complete final `.brushset`
5. Validate native family
6. Load `entrypoints.procreate_workflow_template`
7. Generate project XLSX using actual delivered native brush names
8. Build final ZIP
9. Reopen ZIP and run four-way set validation:
   `Expected Native Brush Set = Delivered .brush Set = Brushset Member Set = XLSX Referenced Brush Set`

Do not generate the XLSX first and backfill native files later.

## 10. Mode boundaries

Mode B: Procreate analysis + native delivery are supported by this repository.

Mode A: analysis may continue, but native `.abr` delivery returns `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE` unless an explicit working external dependency is declared.

Mode AB: Procreate native delivery may proceed; full dual-native delivery returns `PHOTOSHOP_NATIVE_RUNTIME_UNAVAILABLE` while Photoshop native runtime is absent.

Never fabricate `.abr`.

## 11. Acceptance and failure behavior

Use `knowledge/RUNTIME-CONTRACT.md` for:
- evidence states;
- FINAL_COUNT gate;
- native statuses/reason codes;
- Role coverage;
- LFS gate;
- four-way set consistency;
- PACKAGE_PASS / FULL_PASS.

No prose reasoning may override a machine-readable native runtime failure.

Without a real Procreate/Photoshop import/drawing test, do not claim `FULL_PASS`.
