# Portal submission - Relation Ranker

## Category

Builder > Intelligent Contracts

## Title

Relation Ranker

## Contribution date

September 30, 2026 (publication and live verification date).

## Description / Notes (903 characters)

```text
Relation Ranker is a GenLayer Intelligent Contract for ranking 2-10 textual items against a committed criterion. It performs its own non-deterministic LLM judgment with gl.nondet.exec_prompt inside gl.eq_principle.prompt_comparative. Validators independently repeat the pairwise assessment and compare the decision-bearing relation and input hash. That accepted relation determines the stored ranking; this is not an aggregation of already-settled upstream state. Deterministic checks reject malformed or intransitive relations, preserve ties, and prevent changing inputs or re-ranking settled cases. Deployed on hosted Studio with normal validator consensus. Three finalized live tests demonstrate B>A>C, an explicit A=B tie, and UNDETERMINED for a cyclic relation. All 9 local test groups pass. Exact inputs, results, transaction links, and the deployed source revision are included in the repository.
```

## Primary evidence links

GitHub repository:
https://github.com/Zhekinmaksim/genlayer-relation-ranker

Deployed contract (GenLayer hosted Studio):
https://explorer-studio.genlayer.com/address/0xbF86982b3c35AECa4e32a19bDbAead7a89BE255A

## Additional evidence

- [Exact deployed source](https://github.com/Zhekinmaksim/genlayer-relation-ranker/blob/c8e1bc848639162a53d514e6df463c9dc0ec9d15/contract.py)
- [Deployment](https://explorer-studio.genlayer.com/tx/0xff0acfa0b2bf219089aa444c4c0576f1539e6fafe70388d77499ffc640c79c39)
- [Normal order: B > A > C](https://explorer-studio.genlayer.com/tx/0x1ca47d7ec7cc7389b93c33c20eb5cd96f65fa795ad7a307ceacb6b42f6927de5)
- [Tie: A = B > C](https://explorer-studio.genlayer.com/tx/0xa199adf0b1fea281dce78c72e3a5d00a114d82edd057fcd79b4caf4f2e505246)
- [Cycle: UNDETERMINED](https://explorer-studio.genlayer.com/tx/0xc9360078ba1db97c674ac63e49b5d3db1894876e8f74da1fcca1075441eabaa0)
- [Exact live inputs and stored results](https://github.com/Zhekinmaksim/genlayer-relation-ranker/blob/main/evidence.json)

All three ranking transactions are FINALIZED with leader execution SUCCESS and
MAJORITY_AGREE, not necessarily unanimous votes. Each result was confirmed with
get_result, not inferred from transaction acceptance alone.

## Local verification

`python3 sim/check.py`: 9/9 test groups passed on 2026-09-30.
The local harness mocks the model and consensus; live evidence is separate.

## Submission status

Prepared for a new contribution at https://portal.genlayer.foundation/my-submissions.
No portal submission has been sent. Hosted Studio deployment is not mainnet
deployment, and successful tests do not guarantee portal acceptance.
