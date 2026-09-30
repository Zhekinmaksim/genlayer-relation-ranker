# Portal submission - Relation Ranker

## Title

Relation Ranker

## Notes under 1000 chars

```text
A GenLayer IC that ranks two to ten items by reaching consensus on one canonical
pairwise relation, then deriving the order deterministically. Items and criterion
are normalized, bounded, stored, hashed, and checked again before judgment.
Cycles settle as UNDETERMINED instead of being hidden by a forced ordering; ties
remain visible as unseparated pairs. The LLM produces only one bounded verdict
per pair, while graph construction, cycle detection and ordering are on-chain
deterministic steps.
```

## Evidence checklist

- GitHub: https://github.com/Zhekinmaksim/genlayer-relation-ranker
- Commit: pending
- Explorer contract: pending
- Deploy transaction: pending
- Offline verification: `python3 sim/check.py`, 6/6 pass on 2026-09-27 (all six strict orders of three items covered)
- Hosted Studio checks: pending
