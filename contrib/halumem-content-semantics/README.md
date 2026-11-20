# HaluMem Content-Semantics Contribution

This directory contains public-safe material for discussing three HaluMem QA
evaluation semantics:

1. reference answers that conflict with the source evidence;
2. evidence scope for memories merged across sessions; and
3. source-supported details that are absent from the compressed key memory
   points.

The fixtures are synthetic and contain no HaluMem dialogue, question, answer,
or evidence text. They are intended to clarify behavior, not to reproduce an
official benchmark result.

## Files

- `synthetic_cases.jsonl`: six synthetic boundary cases.
- `issue-body.md`: draft text for the upstream maintainer discussion.

Each case records two views:

- `expected_official_label_under_strict_scope`: the label suggested by a strict
  interpretation of the current question/key-memory contract;
- `audit_labels`: the additional content-level diagnosis proposed for review.

The strict labels are discussion expectations, not claims about the exact
output of a stochastic judge model.

## Official contract referenced

The current evaluator sends the QA judge the question, reference answer, key
memory points, and system response. It does not send the complete source
history. See:

- <https://github.com/MemTensor/HaluMem/blob/main/eval/evaluation.py>
- <https://github.com/MemTensor/HaluMem/blob/main/eval/eval_tools.py>

The proposed audit labels must not replace the official
`Correct`/`Hallucination`/`Omission` result unless the HaluMem maintainers
explicitly approve a scoring change.
