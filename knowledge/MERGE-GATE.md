# Merge Eligibility Gate — V2.0

A role merge is allowed only if all relevant dimensions are compatible and the merge does not materially reduce quality, speed, control, or material specificity.

## Mandatory dimensions
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

## Results
- `MERGE_PASS`
- `KEEP_SEPARATE`
- `MERGE_BLOCKED_PENDING_VALIDATION`

## Automatic KEEP_SEPARATE tendencies
Keep roles separate unless strong evidence supports merging when:
- one is precision linework and the other is large-area fill;
- one is dry-brush texture and the other is wet wash;
- one is fur/hair breakup and the other is smooth ribbon/fabric line;
- a merge requires frequent Brush Studio parameter changes;
- a merge forces an impractically wide size range;
- a merge loses material-specific edge or grain behavior;
- a merge slows repeat production.

“Can technically perform both” is never sufficient justification.
