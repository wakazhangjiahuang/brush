# $brush-creator-studio Remote Runtime Contract

Version: 1.3 remote-resolver + delivery-template + quantity-decision-gate contract  
Repository: `wakazhangjiahuang/brush`  
Default branch: `main`

## Purpose

This repository is the persistent source of reusable brush assets, illustrator workflow evidence, machine-readable indexes, and delivery/acceptance templates for `$brush-creator-studio`. The user should not need to re-upload repository-resident brush libraries, illustrator workflow media, technical profiles, or registered delivery templates on every run.

## Required runtime sequence

1. Audit the current task input. A current target/source artwork is required for a new brush-analysis run. A local brush or brushset is optional.
2. Resolve GitHub knowledge before asking for reusable data already stored remotely:
   - read `KB-MANIFEST.json`;
   - read `knowledge/ARTIST-PROFILE.json`;
   - read `knowledge/PROCESS-REGISTRY.json`;
   - read `knowledge/BRUSH-REGISTRY.json`;
   - read the registered delivery template when the selected mode requires it.
3. Route the current artwork to the most relevant workflow branch (`cartoon` or `vintage`) using visual/process evidence. Explicit user routing overrides automatic routing.
4. Inspect only the relevant process media and candidate brush assets needed for the task. Do not load every binary by default.
5. Build or update a shared `Artist Profile + Brush DNA` for the task. This remains the single source of truth for Mode A / Mode B / Mode AB.
6. Perform `Process DNA → Brush Function Clustering → Required Function Coverage Matrix` before deciding brush quantity.
7. Perform Existing Brush Matching against the relevant repository candidates. A filename/purpose hint is discovery evidence only; it is not proof of native behavior.
8. Validate candidate coverage as far as the available native evidence permits, then classify each resolved functional slot as:
   - KEEP: existing brush is sufficient;
   - ADJUST: existing brush is a plausible base but requires parameter tuning;
   - DERIVE: create a related brush variant from a verified/usable base;
   - NEW: no suitable existing candidate can cover the functional slot after relevant candidates have been checked.
   A candidate whose behavior is not yet validated must be marked `PENDING_VALIDATION`; it must not be converted directly to `NEW` merely because verification is unavailable.
9. Run Merge / Redundancy Check. If two functional slots can be covered by one brush without materially compromising the required workflow, merge them.
10. Pass the Quantity Decision Hard Gate, then determine the final brush quantity.
11. Generate the requested native brush output and the required operation-workflow workbook.
12. Run QA and clearly distinguish verified software results from design/mapping recommendations.

## Mode contract

- Mode A = Photoshop / `.abr`
- Mode B = Procreate / `.brush` and `.brushset`
- Mode AB = shared Artist Profile + Brush DNA, then software-specific mapping and validation branches

## Mode B mandatory delivery contract

A Mode B ZIP is not considered complete unless it contains:

1. One or more actual Procreate native `.brush` files when individual brushes are part of the delivery.
2. A `.brushset` containing the delivered brush family when a grouped set is requested or appropriate.
3. A project-specific `Procreate 新笔刷绘画操作流程.xlsx` workbook generated from the registered acceptance template:
   `templates/Procreate/柔彩小熊原稿｜Procreate 新笔刷绘画操作流程.xlsx`.

The XLSX must preserve the template's structural logic and visual hierarchy while replacing project-specific content. Its core columns are:

`序号` / `步骤次序` / `具体步骤` / `操作说明` / `技巧` / `使用笔刷` / `设置与控制` / `完成标准`

The workbook must map the final delivered brush names to actual painting stages. It must not reference placeholder brush IDs that were not delivered.

## Dynamic brush quantity rule

Do not preset the number of brushes, a minimum target, a preferred range, or a fixed family size.

Required sequence:

`Process DNA → Brush Function Clustering → Required Function Coverage Matrix → Existing Brush Matching → Existing Brush Validation → KEEP / ADJUST / DERIVE / NEW → Merge / Redundancy Check → Dynamic Quantity Decision`

For every final brush, record:
- functional slot;
- painting task(s);
- why the brush is necessary;
- relevant existing candidate(s);
- whether existing candidates cover the requirement;
- whether it can be merged with another brush;
- KEEP / ADJUST / DERIVE / NEW classification;
- evidence state.

If necessity cannot be demonstrated, do not include the brush in the final set.

The final count may be zero or any positive number. The count must be the consequence of the coverage analysis, not a design target.

## Quantity Decision Hard Gate

This gate is mandatory and cannot be skipped.

Before labeling any brush quantity as final, all of the following must be true:

1. `Process DNA` is complete enough to identify the actual painting stages required by the current artwork.
2. `Brush Function Clustering` is complete and each distinct functional slot is documented.
3. A `Required Function Coverage Matrix` maps every functional slot to relevant repository candidates or explicitly records that no candidate exists.
4. Relevant Existing Brush candidates have been inspected/validated to the extent technically available.
5. A candidate that exists but is not behavior-validated is marked `PENDING_VALIDATION`, not automatically `NEW`.
6. `NEW` is allowed only after the relevant existing candidates have been checked and none can reasonably cover the slot without unacceptable compromise.
7. Merge / Redundancy Check has been completed so one brush is not duplicated across equivalent functional slots.
8. No unresolved repository asset remains that could materially change KEEP / ADJUST / DERIVE / NEW classification or the total count.

Quantity state rules:

- `PROVISIONAL_COUNT` — a working count produced before the hard gate closes.
- `FINAL_COUNT` — allowed only after every hard-gate condition above is satisfied.
- `QUANTITY_DECISION_BLOCKED` — use when a missing/unreadable native asset prevents a reliable final count.

If a key `.brush` / `.brushset` candidate is unavailable, inaccessible through the current binary path, or only represented by an LFS pointer while its internal brush behavior could materially change the decision, do not claim `FINAL_COUNT`. Use `PROVISIONAL_COUNT` or `QUANTITY_DECISION_BLOCKED` and identify the unresolved asset.

A provisional quantity must never be described to the user as the final dynamically determined quantity.

## Existing Brush state rule

The discovery and classification states are separate:

- `MATCH_FOUND` — a relevant existing candidate was found.
- `PENDING_VALIDATION` — the candidate exists, but its native behavior/parameters are not sufficiently validated.
- `KEEP / ADJUST / DERIVE / NEW` — final decision states after sufficient coverage analysis.

`UNVERIFIED` or `PENDING_VALIDATION` is not evidence that a brush must be recreated. Lack of validation alone must never trigger `NEW`.

## Evidence hierarchy

1. Current user-provided target/source artwork
2. Verified repository process media for the matched branch
3. Verified repository brush asset inventory
4. Extracted brush metadata or settings when technically available
5. Filename-derived routing hints

Filename-derived hints are not equivalent to validated brush behavior.

## Git LFS rule

Repository `.brushset` files are managed by Git LFS. A normal Git blob fetch may return a small LFS pointer containing an object id and size rather than the actual `.brushset` bytes. Do not mistake the pointer for a corrupt brushset. The runtime should use the repository/LFS-aware file path when the binary itself is required.

If an LFS-managed `.brushset` is a relevant candidate for the current Function Coverage Matrix but its actual native contents cannot be inspected, mark the candidate `PENDING_VALIDATION`. If that unresolved set could materially change the final quantity, the quantity state must remain `PROVISIONAL_COUNT` or `QUANTITY_DECISION_BLOCKED`.

## Non-fabrication rule

Never invent Procreate or Photoshop parameters, dynamics, pressure curves, grain values, blend modes, drawing habits, or import-test results. A parameter can be labeled `VERIFIED` only when supported by actual extraction or real software validation. Otherwise use `PROPOSED`, `INFERRED`, or `UNVERIFIED`.

## Native-output rule

Do not create fake `.brush`, `.brushset`, or `.abr` files by renaming extensions.

If native output cannot be generated, mark the corresponding state clearly:
- `NATIVE_OUTPUT_MISSING`
- `NATIVE_BUILD_FAILED`
- `NATIVE_VALIDATION_NOT_RUN`

Parameter mappings may be included as supplemental material, but they never substitute for required native output.

## User convenience contract

For a normal repeat run, the intended user interaction is:

`上传当前插画原稿 + 调用 $brush-creator-studio + 指定模式（若未指定则由任务判断）`

The runtime must not ask the user to upload the existing repository brush library, illustrator workflow recordings, technical profile, or registered operation-workflow template again unless a required remote asset is actually unavailable.

## Fail-safe behavior

If GitHub access fails, the manifest is missing, a registry path is invalid, or the registered delivery template cannot be read:

- set state to `KB_UNAVAILABLE`, `KB_INCOMPLETE`, or `KB_READ_FAILED`;
- identify the exact missing path;
- do not silently invent replacement repository facts;
- continue only from explicit local inputs when that is sufficient.

If a relevant native candidate cannot be resolved and this prevents the Quantity Decision Hard Gate from closing:
- mark the unresolved candidate `PENDING_VALIDATION`;
- use `PROVISIONAL_COUNT` or `QUANTITY_DECISION_BLOCKED`;
- do not mislabel a provisional package as a final optimized brush set.

If the operation-workflow template is unavailable, the ZIP may still contain native brush files, but the delivery must be marked `DELIVERY_TEMPLATE_MISSING` and cannot be reported as a complete Mode B acceptance package.

## Completion gates

A repository-resolver run is `PASS` only when:

- `KB-MANIFEST.json` is readable;
- all required manifest entrypoints are readable;
- selected registry paths resolve to existing repository assets;
- the Mode B delivery template resolves when Mode B is selected;
- LFS pointers are recognized correctly;
- no brush parameter or software test is presented as verified without evidence.

A Quantity Decision is `FINAL_COUNT` only when:
- the Required Function Coverage Matrix is complete;
- relevant existing candidates are resolved enough for a defensible coverage decision;
- no material `PENDING_VALIDATION` candidate remains;
- KEEP / ADJUST / DERIVE / NEW classification is complete;
- Merge / Redundancy Check is complete.

A Mode B delivery package is `PACKAGE PASS` only when:
- the Quantity Decision Hard Gate has closed with `FINAL_COUNT`;
- native `.brush/.brushset` outputs required by the task are present;
- the project-specific Procreate drawing-operation XLSX is present;
- the XLSX references only delivered brush names and stages;
- native-format structure checks have passed where technically possible.

A final native-brush generation run is `FULL PASS` only after the relevant `.brush/.brushset/.abr` has also been imported/tested in the target software or an equivalent validated native workflow has been executed.
