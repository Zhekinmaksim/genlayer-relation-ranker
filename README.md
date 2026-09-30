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
hash reach consensus. The topological sort, cycle detection, and tie handling
are deterministic.

This is a material decision flow: changing an accepted pair verdict changes the
stored order or makes the relation UNDETERMINED. No upstream contract supplies
an already-settled answer. The comparative wrapper repeats the judgment on
validators and uses an LLM comparison of decision fields; it is not a
byte-for-byte cryptographic equality check. See the official
[non-determinism documentation](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism).

## Outcomes

- RANKED: a deterministic display order, plus pairs the judge could not separate.
  Equal items use input-index order for display; this does not imply superiority.
- UNDETERMINED: the accepted relation is cyclic or otherwise intransitive,
  malformed, or a catchable judgment failure occurred. A cyclic relation is
  surfaced, never resolved silently into a confident wrong order. Network-level
  failure to reach consensus can instead leave the transaction unaccepted;
  it does not guarantee a stored UNDETERMINED result.

## Published deployment

- Network: GenLayer hosted Studio (not mainnet).
- [Contract](https://explorer-studio.genlayer.com/address/0xbF86982b3c35AECa4e32a19bDbAead7a89BE255A)
- [Deployment transaction](https://explorer-studio.genlayer.com/tx/0xff0acfa0b2bf219089aa444c4c0576f1539e6fafe70388d77499ffc640c79c39)
- [Deployed source revision](https://github.com/Zhekinmaksim/genlayer-relation-ranker/blob/c8e1bc848639162a53d514e6df463c9dc0ec9d15/contract.py)
- [Submission fields](SUBMISSION.md) and [reproducible live evidence](evidence.json).

## API

- `open_ranking(id, criterion_text)` -> criterion hash
- `submit_items(id, items)` - 2 to 10 items, committed and hashed
- `rank(id)` - permissionless
- `get_outcome(id)` -> 0 pending, 1 ranked, 2 undetermined
- `get_order(id)` -> items best first, empty unless RANKED
- `get_result(id)` -> JSON outcome, reason, order indices, unseparated pairs,
  input commitments and result hash

## Additional test scenarios

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
convergence. Its hash stub uses SHA3-256 only to exercise commitment checks;
the deployed contract uses the SDK's Keccak256. Live evidence is recorded
separately in SUBMISSION.md and evidence.json.

Model agreement is not a guarantee of factual correctness. Items are delimited
as data, but adversarial text and ambiguous criteria remain model-level risks.
This prototype has not received an independent security audit and should not
control funds or high-stakes decisions without further review.
