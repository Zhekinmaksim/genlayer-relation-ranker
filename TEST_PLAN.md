# Test plan - Relation Ranker

## Offline checks

1. Three acyclic pair verdicts produce a complete deterministic order.
2. A cyclic relation settles as `R_UNDETERMINED`, never as a fabricated order.
3. A tie remains visible in `unseparated` while index order is used only as the
   deterministic presentation tie-break.
4. Two to ten items are accepted; smaller and larger fields revert.
5. Empty, duplicate, and overlong items revert before an LLM call.
6. Recomputed stored-item hash must equal the commitment before ranking.
7. A second `rank` call after settlement reverts.
8. All six strict orders of three items, including B > A > C, must rank
   successfully. Pair-result order must not depend on winner indices.

The simulator prohibits constructing DynArray, including in finalization and
view methods. Stored lists are JSON strings decoded into ordinary local lists.

## Hosted Studio checks

Deploy the exact GitHub revision, run one clear three-item ranking and one
ambiguous field, confirm the source compiles with the pinned runtime, and record
the deploy and smoke transaction hashes. LLM convergence is not simulated by
the offline checks.
