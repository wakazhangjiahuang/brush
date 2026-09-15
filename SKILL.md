---
name: brush-creator-studio
description: Create, validate, optimize, and package production-ready Procreate or Photoshop brush systems from current artwork plus the persistent GitHub brush knowledge base, with complete production-stage coverage, material-aware brush roles, anti-undercoverage gates, native brush delivery, and project-specific workflow documentation.
---

# $brush-creator-studio V2.0.0

## 1. Purpose

`$brush-creator-studio` turns a current illustration source into a complete, evidence-bound brush production system. It does **not** optimize for the fewest brushes. It optimizes for the **Minimal Complete Production Set**: the smallest set that fully covers the real drawing process, materials, object-specific needs, quality, and production efficiency without redundant brushes.

Supported modes:
- **A = Photoshop** → `.abr`
- **B = Procreate** → `.brush` + `.brushset`
- **AB = Dual mode** → one shared Artist Profile + Brush DNA, then software-specific native branches

The current artwork is always the highest-priority project evidence.

## 2. Persistent GitHub knowledge resolver

Repository: `https://github.com/wakazhangjiahuang/brush`

Before asking the user to re-upload reusable data, read the repository in this order:
1. `KB-MANIFEST.json`
2. `knowledge/ARTIST-PROFILE.json`
3. `knowledge/PROCESS-REGISTRY.json`
4. `knowledge/BRUSH-REGISTRY.json`
5. `knowledge/BRUSH-CAPABILITY-REGISTRY.json`
6. `knowledge/PROCESS-STAGE-TAXONOMY.json`
7. `knowledge/MATERIAL-TAXONOMY.json`
8. `knowledge/COMPLEXITY-RULES.json`
9. `knowledge/MERGE-GATE.md`
10. `knowledge/RUNTIME-CONTRACT.md`
11. manifest-registered Process DNA and delivery template for the selected mode/branch

Do not ask the user to re-upload repository-resident brush libraries, process recordings, profiles, or templates unless the exact required remote asset is unavailable.

## 3. Required execution chain

For every new brush creation run, use this exact chain:

`Current Artwork Audit`
→ `Repository Resolver`
→ `Artwork Complexity Profile`
→ `Style / Color / Material DNA`
→ `Full Production Stage Decomposition`
→ `Process DNA`
→ `Object / Material Map`
→ `Brush Role Inventory`
→ `Required Role Coverage Matrix`
→ `Existing Brush Candidate Retrieval`
→ `Native Metadata / Capability Validation`
→ `KEEP / ADJUST / DERIVE / NEW`
→ `Brush Specialization Gate`
→ `Merge Eligibility Gate`
→ `Redundancy Check`
→ `Undercoverage Review`
→ `Complexity Sanity Check`
→ `Dynamic Quantity Decision`
→ `Native Brush Build`
→ `Native Delivery Gate`
→ `Project Workflow XLSX`
→ `QA`
→ `ZIP`

No quantity decision may be finalized before the two anti-error gates have run:
- **Redundancy Check** prevents unnecessary duplicates.
- **Undercoverage Review** prevents over-merging and missing brush roles.

## 4. Full Production Stage Decomposition

Before brush matching, inspect all applicable production stages from `PROCESS-STAGE-TAXONOMY.json`.

Every stage must be explicitly classified:
- `REQUIRED`
- `OPTIONAL`
- `NOT_APPLICABLE`

At minimum audit these categories when relevant:
- sketch / construction
- primary lineart
- secondary/detail line
- base fill
- transparent wash
- local color
- wet-edge / bleed
- blend / smudge
- paper / pigment / grain texture
- shadow / value
- dry brush
- fur / hair
- fabric / clothing
- decorative patterns / accessories
- environment / foliage / architecture
- fine detail
- highlight
- glaze / color refinement
- final cleanup

Do not collapse these into three generic buckets such as “line / color / blend” without first proving that all stage-specific behaviors remain covered.

## 5. Artwork Complexity Profile

Assess at least:
- number of main subjects
- number of secondary subjects
- number of object classes
- number of distinct material classes
- fur/hair types
- clothing/accessory complexity
- texture density
- background/scene complexity
- lighting/value complexity
- refinement depth
- repeated decorative systems

Complexity determines the strictness of the undercoverage review. It does **not** directly set a fixed brush count.

## 6. Object / Material Map

Build a map of actual project materials and behaviors. Examples include:
- short fur
- long fur
- curly/fluffy fur
- rough terrier fur
- dense dark fur
- skin
- fabric
- ribbon
- paper
- wood
- foliage
- metal
- glass
- watercolor wash
- dry pigment
- rough pencil
- smooth decorative line

A visible material-specific behavior may not be deleted merely because a general-purpose brush can produce a rough approximation.

## 7. Brush Role Inventory

Separate **Production Stage**, **Required Brush Behavior**, **Brush Role**, **Candidate Brush**, and **Delivered Native Brush**.

A Brush Role is a production function, not a filename. Examples:
- construction sketch
- loose watercolor line
- precise detail line
- flat/base fill
- transparent wash
- wet-edge glaze
- dry pigment texture
- fur breaker
- cloth/fabric texture
- ribbon/decorative smooth line
- foliage scatter
- shadow wash
- highlight / cleanup

One brush may cover multiple roles only after the Merge Eligibility Gate passes.

## 8. Existing brush matching and evidence states

Use repository inventory and capability data as candidates.

Evidence labels:
- `VERIFIED` — tested/extracted in target software or equivalent validated native workflow
- `VERIFIED_METADATA` — native metadata extracted, but not necessarily hand-tested in target software
- `INFERRED` — supported by artwork/process evidence, not native-tested
- `PROPOSED` — recommended new setting or behavior
- `UNVERIFIED` — insufficient evidence

Candidate discovery states:
- `MATCH_FOUND`
- `PENDING_VALIDATION`

Final classifications:
- `KEEP`
- `ADJUST`
- `DERIVE`
- `NEW`

Rules:
- filename/purpose hints are discovery only, never proof of behavior;
- an unresolved candidate remains `PENDING_VALIDATION` and may not be converted to `NEW` only because inspection is unavailable;
- `NEW` is allowed only after relevant existing candidates are sufficiently checked and cannot cover the role without unacceptable compromise.

## 9. Brush Specialization Gate

Distinguish general-purpose from specialized roles.

Specialized visible behaviors such as fur, dry brush, fabric, stipple, grain, wet bleed, foliage, smooth decorative ribbon lines, or high-detail cleanup must not be removed simply because a general brush can “technically” perform them.

Keep a dedicated role when specialization materially improves any of:
- visual fidelity
- repeatability
- speed
- pressure/opacity control
- edge behavior
- texture behavior
- size-range usability
- reduced parameter switching

## 10. Merge Eligibility Gate

Never merge roles solely because one brush can perform both.

A merge may pass only when all relevant dimensions are compatible:
1. Shape behavior
2. Grain behavior
3. Edge behavior
4. Opacity response
5. Pressure response
6. Wet/dry behavior
7. Required size range
8. Stroke rhythm
9. Parameter-switch burden
10. Workflow speed
11. Output quality
12. Material-specific behavior

Possible results:
- `MERGE_PASS`
- `KEEP_SEPARATE`
- `MERGE_BLOCKED_PENDING_VALIDATION`

If merging causes frequent size/opacity/wetness switching, loss of material fidelity, slower work, or weaker control, keep roles separate.

## 11. Dynamic quantity and undercoverage rules

Never preset a final brush count, minimum target, or fixed family size.

However, V2 introduces complexity sanity bands as QA diagnostics, not quantity targets:
- minimal icon / simple spot art: typically 2–5 roles
- simple single-character illustration: typically 5–8 roles
- complete single-character illustration: typically 7–12 roles
- multi-character / multi-material illustration: typically 8–16 roles
- multi-character + fur + clothing + texture: typically 10–18 roles
- complete scene illustration: typically 12–24+ roles

For a normal complete illustration, **fewer than 8 final brush roles automatically triggers `UNDERCOVERAGE_REVIEW_REQUIRED` unless the artwork is explicitly simple/minimal and the system can demonstrate full coverage.** This is a review trigger, not a forced minimum count.

Also trigger undercoverage review if any of these occur:
- a required production stage has no mapped role;
- a visible material has no role;
- a single brush is asked to cover more than four materially different production roles;
- one brush spans both large-area base fill and precision linework without evidence that workflow cost is acceptable;
- one brush spans wet-media and dry-media behavior without a proven equivalent workflow;
- fur/hair and smooth fabric/decorative line are merged without a specialization justification;
- complex multi-subject or scene work returns an unusually small set.

Quantity states:
- `PROVISIONAL_COUNT`
- `FINAL_COUNT`
- `QUANTITY_DECISION_BLOCKED`

`FINAL_COUNT` is allowed only after Stage Coverage, Material Coverage, Candidate Validation, Specialization, Merge, Redundancy, Undercoverage, and Complexity Sanity all pass.

## 12. Native build strategy

Prefer in this order:
1. `KEEP` an existing validated native brush unchanged when it fully covers the role.
2. `ADJUST` an existing native brush only when parameter changes are justified and technically writable.
3. `DERIVE` from a validated native base when a related specialized variant is justified.
4. `NEW` only when no suitable base exists and the runtime can produce a structurally valid native brush.

Do not fake native files by renaming extensions or packaging arbitrary data.

## 13. Mode B — Procreate hard delivery contract

A Procreate task is **not complete** unless the final ZIP contains all of the following:
1. **Every final delivered native `.brush` file** — one file per delivered brush role where individual brushes are part of the output.
2. **One native `.brushset`** containing the full final delivered brush family.
3. **One project-specific XLSX** named `[项目名]｜Procreate 新笔刷绘画操作流程.xlsx`.

The XLSX must be based on the manifest-registered V2 template and must map every `REQUIRED` production stage to a real delivered brush name.

Forbidden completion states:
- ZIP contains XLSX but no `.brush`;
- ZIP contains individual `.brush` but no `.brushset`;
- ZIP references brush names that were not actually delivered;
- `.brushset` exists but does not contain the final brush family;
- placeholder brush names;
- renamed fake native files.

If native output cannot be generated or structurally validated, set:
- `NATIVE_OUTPUT_BLOCKED`
- `NATIVE_BUILD_FAILED`
- `NATIVE_VALIDATION_NOT_RUN`

Do **not** report `PACKAGE PASS` in those states.

## 14. Native Delivery Gate

Before packaging Mode B, check:
- all final brush names exist as native `.brush` outputs when required;
- `.brushset` exists;
- `.brushset` contains all final delivered brushes;
- XLSX exists;
- XLSX references only delivered brush names;
- file extensions correspond to real native structures;
- no required role is missing.

`PACKAGE PASS` requires all items above.

`FULL PASS` additionally requires real Procreate import/drawing validation or an equivalent validated native workflow. Do not claim import success if it was not actually run.

## 15. Mode A / AB

Mode A uses the same V2 coverage logic and replaces the native delivery branch with Photoshop `.abr` validation.

Mode AB shares:
- Artist Profile
- Style / Color / Material DNA
- Production Stage Decomposition
- Object / Material Map
- Brush Role Inventory

Then it splits into Procreate and Photoshop native mappings. Do not independently redefine the artistic process for each software.

## 16. XLSX requirements

The workbook must include, at minimum:
- project production steps;
- stage status (`REQUIRED / OPTIONAL / NOT_APPLICABLE`);
- object/material;
- Brush Role;
- real delivered brush name;
- operation instructions;
- completion standard;
- coverage/candidate/evidence sheet;
- quantity/native QA sheet.

All untested settings must be labeled `PROPOSED`.

## 17. Fail-safe behavior

If GitHub knowledge cannot be read:
- mark `KB_UNAVAILABLE`, `KB_INCOMPLETE`, or `KB_READ_FAILED`;
- identify the exact missing path;
- do not invent missing repository facts.

If a relevant native candidate is unavailable and could change the set:
- mark it `PENDING_VALIDATION`;
- use `PROVISIONAL_COUNT` or `QUANTITY_DECISION_BLOCKED`.

If the V2 XLSX template is unavailable:
- mark `DELIVERY_TEMPLATE_MISSING`;
- do not claim a complete Mode B package.

## 18. Completion gates

A V2 run reaches `FINAL_COUNT` only when:
- G1 Process Stage Coverage = PASS
- G2 Material Coverage = PASS
- G3 Object-specific Coverage = PASS
- G4 Candidate Validation = PASS
- G5 Specialization Review = PASS
- G6 Merge Eligibility = PASS
- G7 Redundancy Check = PASS
- G8 Undercoverage Review = PASS
- G9 Complexity Sanity = PASS

Mode B `PACKAGE PASS` additionally requires:
- G10 Native Delivery Gate = PASS
- actual `.brush` files present
- actual `.brushset` present
- project XLSX present

The correct optimization target is **Minimal Complete Production Set**, not “minimum number of brushes”.
