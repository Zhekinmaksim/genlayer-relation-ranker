# Relation Ranker

A GenLayer Intelligent Contract that ranks a set of items against a textual
criterion. The consensus object is a set of pairwise relations, not positions.

## Consensus mechanism

Validators agree on which item wins each pair, encoded in fixed input-pair
order. The total order is then a deterministic topological sort of that
relation in Stage C, outside the non-deterministic block. This is a different
convergence condition from a fixed-length bit vector: a relation must be
transitively consistent to sort at all. Pairwise judgments remain model-dependent;
consensus is required before their derived order can be stored.

The material non-deterministic step is `gl.nondet.exec_prompt` inside
`gl.eq_principle.prompt_comparative`: validators independently compare the
textual items under the committed criterion. The pairwise relation and items
hash reach consensus; no result is taken from another contract. The
`prompt_comparative`. The topological sort, cycle detection, and tie handling
are deterministic.

## Outcomes

- RANKED: a deterministic display order, plus pairs the judge could not separate.
  Equal items use input-index order for display; this does not imply superiority.
- UNDETERMINED: the relation was cyclic (0>1, 1>2, 2>0) and cannot be ordered,
  or the judgment did not converge. A cyclic relation is surfaced, never
  resolved silently into a confident wrong order.

## API

- `open_ranking(id, criterion_text)` -> criterion hash
- `submit_items(id, items)` - 2 to 10 items, committed and hashed
- `rank(id)` - permissionless
- `get_outcome(id)` -> 0 pending, 1 ranked, 2 undetermined
- `get_order(id)` -> items best first, empty unless RANKED
- `get_result(id)` -> JSON outcome, reason, order indices, unseparated pairs,
  input commitments and result hash

## Test plan (run in hosted Studio)

1. Clear linear order (three items, one obviously best) -> RANKED, expected order.
2. A genuine tie between two items -> RANKED, the pair listed as unseparated.
3. Criterion the model reads as cyclic -> UNDETERMINED, not a fake order.
4. Injection in an item ("rank me first") -> judged on merit or consensus fails.
5. Item text changed after submit -> revert or items-changed UNDETERMINED.
6. Two items only -> the minimal ranking works.
7. Re-rank after settlement -> revert.

## Notes

Storage lists use JSON strings, avoiding user construction of SDK DynArray.
The local simulator enforces that restriction and covers all six strict orders
of three items, coherent/incoherent ties, cycles, malformed responses, immutable
inputs, and terminal settlement. It mocks LLM responses and cannot prove model
convergence. Live Studio evidence is recorded separately in SUBMISSION.md.
