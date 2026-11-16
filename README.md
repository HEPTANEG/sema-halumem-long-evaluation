# Sema HaluMem-Long Evaluation

This repository records a reproducible single-user HaluMem-Long long-term
memory experiment with Sema. It is a public-safe snapshot: benchmark-derived
dialogue, questions, answers, and per-question evidence are intentionally
excluded.

## Results

The secondary review is shown first because it audits whether the official
labels match the original dialogue. It is a manual, non-official estimate and
must not be confused with the benchmark score.

| Result track | Accuracy | Hallucination | Omission |
| --- | ---: | ---: | ---: |
| Favorable secondary-review estimate | 89.02% (146/164) | 4.88% (8/164) | 6.10% (10/164) |
| Official HaluMem evaluator | 63.41% (104/164) | 29.27% (48/164) | 7.32% (12/164) |

The favorable estimate reclassifies supported answers and mixed extra-detail
cases after a manual source audit. It is not an official leaderboard score.
The official evaluator result is preserved unchanged and remains the primary
reproducible benchmark output.

## Experimental Configuration

| Parameter | Recorded value |
| --- | --- |
| Benchmark | HaluMem-Long |
| Scope | One HaluMem user, 115 ordered sessions, 164 questions |
| System under test | Sema |
| Runtime profile | Developer mode |
| STM budget | 10,000 tokens |
| WM budget | 10,000 tokens |
| LTM Maintainer activation threshold | 100 pending slots |
| Permission policy | Unattended |
| Provider-reported API model | `deepseek-flash` (DeepSeek V4 Flash) |
| Configured model value in run metadata | `deepseek-chat` |
| Secondary reviewer | Codex / GPT-5.6 Luna XHigh; manual review only |
| Official evaluator revision | `718f16ff0c83413b1c86fa83fc13cc1a639871f9` |

The provider-reported model identifier is recorded separately from the
configured value in the historical run metadata. This avoids silently
rewriting the original experiment record.

The STM, WM, runtime profile, threshold, and permission settings above
describe the local Sema execution environment. They are reported for
reproducibility and are not part of the official HaluMem benchmark
specification.

Additional conditions that affect interpretation are:

- The answer phase used the supplied answer-writing guidelines, including a
  maximum of 20 English words per answer.
- Learning and examination were separated. The learning data was removed from
  the Sema workspace before examination.
- The official HaluMem evaluator used the fixed revision recorded above.
- The secondary review used the original dialogue and reference material from
  the private evidence copy; it did not change the official evaluator inputs.
- The public branch contains no raw benchmark dialogue, question/answer
  sheet, or per-question evidence.

## Public Release Boundary

This snapshot contains experiment configuration, prompts, hashes, source
references, methodology, and aggregate results. The complete evidence remains
in the local `main` branch. Reproducing the full evaluation requires obtaining
HaluMem separately under its applicable terms and supplying the external
reference data to the private evaluation scripts.

## Contents

- `learning_prompt.md`: learning-phase prompt
- `exam_prompt.md`: examination-phase file protocol
- `answering_guidelines.md`: answer-writing guidance
- `experiment_manifest.json`: experiment metadata and release boundary
- `LearningData.sha256`: hash inventory for the private learning set
- `Sema/Placeholder text for test.txt`: foreground-memory pressure placeholder
- `Evaluation/full-115-sessions-20261116T000000Z/summary.md`: aggregate run
  summary without source dialogue
- `reports/sema-halumem-long-evaluation-report.pdf`: public-safe result report
- `reports/sema-halumem-long-evaluation-report.md`: report source

The MIT license applies only to original files in this repository. It does not
grant any rights to HaluMem data or other external benchmark materials.

## HaluMem Source and Licensing

HaluMem is an external benchmark. This repository does not redistribute its
dialogue data or derived question/answer evidence. See the HaluMem repository
and its maintainer clarification for applicable data terms and attribution:

- https://github.com/MemTensor/HaluMem
- https://github.com/MemTensor/HaluMem/issues/13

## Reproduction Boundary

The experiment uses the HaluMem data ordering and evaluator revision recorded
above. The public snapshot alone is insufficient to reproduce the full run
because benchmark-derived input and detailed evidence are intentionally
excluded.
