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
9. Malformed model output (including a string instead of the verdict array)
   produces UNDETERMINED.
10. Finalized RANKED and UNDETERMINED cases reject another rank call.
11. Unauthorized item submission and replacing committed inputs are rejected.
12. Public get_result exposes tie pairs and the final reason.

The simulator prohibits constructing DynArray, including in finalization and
view methods. Stored lists are JSON strings decoded into ordinary local lists.

## Hosted Studio checks

Deployed contract.py from revision c8e1bc848639162a53d514e6df463c9dc0ec9d15
with the pinned runtime on 2026-09-30. Live cases use normal consensus, not
leader-only mode. Exact inputs, transaction hashes, and get_result responses
are in evidence.json. Inspect both the receipt's execution result and the
stored result; ACCEPTED alone can also describe a transaction that reverted.

The local harness has nine test groups. The boundary scenarios above are a
test plan, not a claim that every case was run live. LLM convergence and
network-level consensus are not simulated by the offline checks.
