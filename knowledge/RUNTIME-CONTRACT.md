# Runtime Contract — $brush-creator-studio V2.0.0

Repository: `wakazhangjiahuang/brush`  
Canonical skill: repository `SKILL.md` and installed `SKILL.md` must express the same V2 rules.

## Mandatory runtime order
1. Current Artwork Audit
2. KB-MANIFEST resolver
3. Artwork Complexity Profile
4. Style / Color / Material DNA
5. Full Production Stage Decomposition
6. Process DNA
7. Object / Material Map
8. Brush Role Inventory
9. Required Role Coverage Matrix
10. Existing Brush Matching
11. Native Metadata / Capability Validation
12. KEEP / ADJUST / DERIVE / NEW
13. Brush Specialization Gate
14. Merge Eligibility Gate
15. Redundancy Check
16. Undercoverage Review
17. Complexity Sanity Check
18. Dynamic Quantity Decision
19. Native Brush Build
20. Native Delivery Gate
21. Project Workflow XLSX
22. QA
23. ZIP

## V2 anti-undercoverage rule
The runtime must not equate “can technically paint” with “should share one brush”. A role can merge only when the multi-dimensional Merge Gate passes without meaningful quality, material, or workflow compromise.

A normal complete illustration returning fewer than 8 roles must trigger `UNDERCOVERAGE_REVIEW_REQUIRED`, unless the project is demonstrably minimal and every required stage/material remains covered. Complex multi-character or scene projects should receive stricter review.

## Quantity hard gate
`FINAL_COUNT` requires PASS on:
- Process Stage Coverage
- Material Coverage
- Object-specific Coverage
- Candidate Validation
- Specialization Review
- Merge Eligibility
- Redundancy Check
- Undercoverage Review
- Complexity Sanity

## Mode B native delivery hard gate
A Mode B package is not complete unless it contains:
- actual final `.brush` files;
- an actual `.brushset` containing the full final family;
- a project XLSX generated from `assets/Procreate新笔刷绘画操作流程_V2.xlsx` or the remote manifest-registered equivalent.

If any of these are missing, return `NATIVE_OUTPUT_BLOCKED`, `NATIVE_BUILD_FAILED`, or `DELIVERY_TEMPLATE_MISSING`. Never substitute parameter notes for required native files.

## Existing candidate policy
- Filename hints are discovery only.
- `PENDING_VALIDATION` must remain distinct from `NEW`.
- Git LFS pointer text is not native `.brushset` inspection.
- Do not invent import tests, hand feel, pressure habits, tilt behavior, or native parameters.

## Merge policy
Use `references/MERGE-GATE.md`. A merge requires compatibility across shape, grain, edge, opacity, pressure, wet/dry behavior, size range, stroke rhythm, parameter-switch burden, workflow speed, quality, and material-specific behavior.

## Full PASS
`FULL PASS` is allowed only after actual Procreate/Photoshop import or equivalent validated native testing. Structural checks alone are `PACKAGE PASS`, not `FULL PASS`.
