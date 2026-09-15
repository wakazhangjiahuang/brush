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
6. Use KEEP / ADJUST / DERIVE / NEW gap-analysis states before proposing new brushes.
7. Never infer native brush parameters from filenames. Filename-based fields are routing hints only.
8. Recognize Git LFS pointer files for `.brushset`; do not classify a small pointer blob as a damaged brushset.
9. Existing repository data must not be requested from the user again unless GitHub access or the exact indexed asset is unavailable.
10. If the repository cannot be read, set `KB_UNAVAILABLE`; identify the missing path and fall back only to explicit local inputs.

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
- A resolver PASS is not a software import PASS.

## Default user interaction after patch

Normal run: upload current artwork + invoke `$brush-creator-studio` + optionally specify A/B/AB.

The repository URL and persistent artist/brush data are part of the Skill contract and should not need to be re-entered each time.
