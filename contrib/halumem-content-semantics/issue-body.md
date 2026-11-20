# Clarify QA evidence scope, reference conflicts, and source-supported extra details

## Summary

We evaluated one HaluMem-Long user across 115 ordered sessions and 164
questions using the HaluMem dataset and evaluation code at commit
[`718f16ff0c83413b1c86fa83fc13cc1a639871f9`](https://github.com/MemTensor/HaluMem/commit/718f16ff0c83413b1c86fa83fc13cc1a639871f9).

HaluMem is the benchmark and evaluator under discussion; Sema was only the
system under test. We did not modify the HaluMem evaluator. The commit above
identifies the HaluMem repository version used for the run, not a Sema
repository or project commit.

The unchanged official QA result was:

| Correct | Hallucination | Omission |
| ---: | ---: | ---: |
| 104/164 (63.41%) | 48/164 (29.27%) | 12/164 (7.32%) |

We then performed a manual source audit of every non-Correct item. This audit
is not an alternative leaderboard score. It classified the items as:

- 8 confirmed errors;
- 10 confirmed omissions;
- 24 likely official over-penalties;
- 17 mixed-scope or extra-detail cases; and
- 1 reference conflict.

The purpose of this report is to clarify the intended evaluation contract, not
to request that our result replace the official score.

## Representative cases

The identifiers below use the dataset's `session_index:question_index` form.
They are provided so that maintainers can locate the cases in the official
dataset. We intentionally do not reproduce the original questions, answers,
dialogue, or evidence text.

| Case | Official label | Manual audit finding | Specific issue |
| --- | --- | --- | --- |
| `0:2` | Hallucination | `mixed_scope_or_extra` | The core negative answer is supported, but the response adds a later date that is not established by the question's session. |
| `2:1` | Hallucination | `likely_misjudgment` | The core negative answer is correct; additional employment and financial details are supported by the source but are narrower than the compressed reference answer. |
| `15:1` | Hallucination | `confirmed_error` | The response gives a definite value that exists in an earlier session, while the current session's reference is Unknown. This is a genuine session-boundary error. |
| `15:7` | Omission | `confirmed_omission` | The source records the relevant influence on a career transition, but the response says the information is unknown. |
| `18:0` | Hallucination | `confirmed_error` | The source supports one class of physical activity, while the response substitutes a different activity through unsupported inference. |
| `18:2` | Omission | `confirmed_omission` | The source explicitly records the activity, but the response says it cannot recall it. |
| `22:0` | Hallucination | `likely_misjudgment` | The response preserves the requested non-violent and cognitive-benefit direction, but adds a specific example not present in the compressed reference. |
| `114:1` | non-Correct | `reference_conflict` | The source dialogue and the released reference disagree on a date; the system response follows the source dialogue. |

These cases show that the negative labels are not all the same phenomenon:
some are genuine memory or reasoning errors, while others depend on the
evidence window or on a conflict between the source and reference.

## Current evaluator contract

The current evaluator passes the QA judge only:

```text
question
reference_answer
key_memory_points
system_response
```

The complete source history is not passed to the QA judge. This is visible in
the current evaluator implementation and prompt:

- <https://github.com/MemTensor/HaluMem/blob/main/eval/evaluation.py>
- <https://github.com/MemTensor/HaluMem/blob/main/eval/eval_tools.py>

This creates two concrete questions:

1. If a memory object merges facts from several sessions, is QA evidence
   intentionally limited to the current session, or should the judge be able
   to verify the object's complete source history?
2. If an answer's core conclusion is correct and an additional detail is
   supported by the source history, but that detail is absent from the
   reference answer and key memory points, should it be Correct, Hallucination,
   or a separate diagnostic category?

The current prompt says that irrelevant extra information should not by
itself be treated as hallucination, but also restricts judgment to the
reference answer and key memory points. We would appreciate clarification of
how these rules are intended to interact.

## Reference conflicts

For a case such as `114:1`, where the dialogue and reference disagree, which
source is authoritative?

Should a reference conflict:

- receive a separate `ReferenceConflict` diagnosis;
- be excluded from the valid score; or
- be corrected in the released reference data?

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
score or leaderboard comparability. The public synthetic fixtures are here:

<https://github.com/HEPTANEG/sema-halumem-long-evaluation/tree/codex/halumem-content-semantics/contrib/halumem-content-semantics>

We can provide additional source identifiers and private verification details
to the maintainers if needed. We do not redistribute HaluMem-derived dialogue
or evidence. This is consistent with the licensing clarification in Issue
`#13`.

After the intended semantics are confirmed, we would be happy to prepare a
small PR with synthetic regression fixtures and an optional audit mode. The
official mode would remain unchanged.

Thank you for clarifying the expected evaluation contract.
