# Clarify QA evidence scope, reference conflicts, and source-supported extra details

## Context

We evaluated one HaluMem-Long user across 115 ordered sessions and 164
questions using the official-compatible evaluator revision
`718f16ff0c83413b1c86fa83fc13cc1a639871f9`.

The official three-way QA result remains unchanged. We are not proposing to
replace the official leaderboard score. We performed a separate manual source
audit to understand non-Correct cases. The audit classified the cases as:

- 8 confirmed errors;
- 10 confirmed omissions;
- 24 likely official over-penalties;
- 17 mixed-scope or extra-detail cases; and
- 1 reference conflict.

These counts are diagnostic observations from one private run, not a new
official score. We do not include HaluMem dialogue, questions, answers, or
derived evidence in this issue. We can provide source identifiers and private
verification details to the maintainers if useful.

The current evaluator passes the QA judge the question, reference answer, key
memory points, and system response. The complete source history is not passed
to the QA judge. See the current evaluator implementation and prompt:

- <https://github.com/MemTensor/HaluMem/blob/main/eval/evaluation.py>
- <https://github.com/MemTensor/HaluMem/blob/main/eval/eval_tools.py>

We prepared public synthetic cases in
`contrib/halumem-content-semantics/synthetic_cases.jsonl` to isolate the
semantic boundaries without redistributing benchmark-derived content.

## Questions for maintainers

### 1. Reference conflict

If the original dialogue and key memory points support fact A, but the
reference answer states fact B, which source is authoritative?

Should such a case:

- receive a separate `ReferenceConflict` diagnosis;
- be excluded from the valid score; or
- be corrected in the released reference data?

### 2. Evidence scope for cross-session memories

If a memory object merges facts from multiple sessions, should QA evaluation
remain limited to the current session's key memory points, or may the judge
use the complete source history for that memory object?

More specifically:

- Is QA intended to be session-local or user-history based?
- How should a merged memory expose source evidence from earlier sessions?
- If a fact is supported by the user's history but absent from the current key
  memory points, is it valid evidence for the answer?

### 3. Source-supported extra detail

If the core answer is correct and an additional detail is supported by the
source history, but the detail is absent from the reference answer and key
memory points, should the result be `Correct`, `Hallucination`, or a separate
diagnostic category such as `SupportedExtra`?

The current prompt says that irrelevant extra information should not by itself
be treated as hallucination, but it also restricts the evaluation to the
reference answer and key memory points. We would appreciate clarification of
how these rules are intended to interact.

## Proposed backwards-compatible direction

We suggest preserving the official
`Correct`/`Hallucination`/`Omission` score and, if useful, adding an optional
audit output with labels such as:

- `SupportedExtra`;
- `UnsupportedExtra`;
- `ReferenceConflict`;
- `EvidenceScopeMismatch`; and
- `PartialAnswer`.

The audit output would explain a negative label without changing the official
score or leaderboard comparability. We would be happy to prepare a small PR
with synthetic regression fixtures after the intended semantics are
confirmed.

Thank you for clarifying the expected evaluation contract.
