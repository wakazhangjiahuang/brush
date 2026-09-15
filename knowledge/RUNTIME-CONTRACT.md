# $brush-creator-studio Remote Runtime Contract

Version: 1.1 remote-resolver contract  
Repository: `wakazhangjiahuang/brush`  
Default branch: `main`

## Purpose

This repository is the persistent source of reusable brush assets, illustrator workflow evidence, and machine-readable indexes for `$brush-creator-studio`. The user should not need to re-upload repository-resident brush libraries or illustrator workflow media on every run.

## Required runtime sequence

1. Audit the current task input. A current target/source artwork is required for a new brush-analysis run. A local brush or brushset is optional.
2. Resolve GitHub knowledge before asking for reusable data already stored remotely:
   - read `KB-MANIFEST.json`;
   - read `knowledge/ARTIST-PROFILE.json`;
   - read `knowledge/PROCESS-REGISTRY.json`;
   - read `knowledge/BRUSH-REGISTRY.json`.
3. Route the current artwork to the most relevant workflow branch (`cartoon` or `vintage`) using visual/process evidence. Explicit user routing overrides automatic routing.
4. Inspect only the relevant process media and candidate brush assets needed for the task. Do not load every binary by default.
5. Build or update a shared `Artist Profile + Brush DNA` for the task. This remains the single source of truth for Mode A / Mode B / Mode AB.
6. Perform gap analysis against existing repository brushes:
   - KEEP: existing brush is sufficient;
   - ADJUST: existing brush is a plausible base but requires parameter tuning;
   - DERIVE: create a related brush variant from a verified base;
   - NEW: no suitable base exists, design a new brush specification.
7. Generate the requested output package and clearly distinguish verified software results from design/mapping recommendations.

## Mode contract

- Mode A = Photoshop / `.abr`
- Mode B = Procreate / `.brush` and `.brushset`
- Mode AB = shared Artist Profile + Brush DNA, then software-specific mapping and validation branches

## Evidence hierarchy

1. Current user-provided target/source artwork
2. Verified repository process media for the matched branch
3. Verified repository brush asset inventory
4. Extracted brush metadata or settings when technically available
5. Filename-derived routing hints

Filename-derived hints are not equivalent to validated brush behavior.

## Git LFS rule

Repository `.brushset` files are managed by Git LFS. A normal Git blob fetch may return a small LFS pointer containing an object id and size rather than the actual `.brushset` bytes. Do not mistake the pointer for a corrupt brushset. The runtime should use the repository/LFS-aware file path when the binary itself is required.

## Non-fabrication rule

Never invent Procreate or Photoshop parameters, dynamics, pressure curves, grain values, blend modes, or import-test results. A parameter can be labeled `VERIFIED` only when supported by actual extraction or real software validation. Otherwise use `PROPOSED`, `INFERRED`, or `UNVERIFIED`.

## User convenience contract

For a normal repeat run, the intended user interaction is:

`上传当前插画原稿 + 调用 $brush-creator-studio + 指定模式（若未指定则由任务判断）`

The runtime must not ask the user to upload the existing repository brush library, illustrator workflow recordings, or technical profile again unless a required remote asset is actually unavailable.

## Fail-safe behavior

If GitHub access fails, the manifest is missing, or a registry path is invalid:

- set state to `KB_UNAVAILABLE` or `KB_INCOMPLETE`;
- identify the exact missing path;
- do not silently invent replacement repository facts;
- continue only from explicit local inputs when that is sufficient.

## Completion gates

A repository-resolver run is `PASS` only when:

- `KB-MANIFEST.json` is readable;
- all manifest entrypoints are readable;
- selected registry paths resolve to existing repository assets;
- LFS pointers are recognized correctly;
- no brush parameter or software test is presented as verified without evidence.

A final native-brush generation run is `FULL PASS` only after the relevant `.brush/.brushset/.abr` has also been imported/tested in the target software or an equivalent validated native workflow has been executed.
