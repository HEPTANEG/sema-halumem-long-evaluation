# Sema HaluMem-Long Evaluation Report

## Executive Summary

This report documents a single-user HaluMem-Long experiment with Sema across
115 ordered sessions and 164 questions. It presents the manual secondary audit
before the unchanged official evaluator result, as requested. The two tracks
answer different questions and must not be merged into one leaderboard score.

## 1. Secondary Review

The favorable secondary-review estimate is:

| Accuracy | Hallucination | Omission | Correct |
| ---: | ---: | ---: | ---: |
| 89.02% | 4.88% | 6.10% | 146/164 |

This is a manual source-level audit. It reclassifies answers whose core claim
is supported by the original dialogue, including mixed extra-detail cases. It
is not an official HaluMem metric or leaderboard result.

## 2. Official Evaluator Result

The original official-compatible evaluator output remains unchanged:

| Accuracy | Hallucination | Omission | Correct |
| ---: | ---: | ---: | ---: |
| 63.41% | 29.27% | 7.32% | 104/164 |

The evaluator revision was fixed at commit
`718f16ff0c83413b1c86fa83fc13cc1a639871f9`. The official score is the
reproducible benchmark result; the secondary audit is interpretive context.

## 3. Experiment Configuration

| Parameter | Value |
| --- | --- |
| Benchmark scope | HaluMem-Long, one user, 115 sessions, 164 questions |
| System | Sema |
| Runtime profile | Developer mode |
| STM / WM budget | 10,000 / 10,000 tokens |
| LTM Maintainer activation threshold | 100 pending slots |
| Permission policy | Unattended |
| Answer model reported by provider | `deepseek-flash` (DeepSeek V4 Flash) |
| Configured model value in metadata | `deepseek-chat` |
| Secondary reviewer | Codex / GPT-5.6 Luna XHigh |
| Answer length limit | 20 English words |

The threshold, context budgets, runtime profile, permission policy, and answer
length limit are local experimental conditions. They are not part of the
official HaluMem benchmark specification.

Learning data was removed from the Sema workspace before the examination.
The public release does not include raw dialogue, the answer sheet, or
per-question evidence.

## 4. Interpretation and Limitations

The official evaluator is intentionally preserved as the primary result. The
secondary estimate should be read as an audit of label strictness and source
support, not as a replacement score. It cannot establish official leaderboard
eligibility.

The public snapshot contains hashes, configuration, prompts, methodology, and
aggregate results. Full reproduction requires obtaining HaluMem separately
under its applicable terms and supplying the excluded reference data.

## Sources

- HaluMem repository: https://github.com/MemTensor/HaluMem
- HaluMem maintainer clarification: https://github.com/MemTensor/HaluMem/issues/13
- Official evaluator revision: `718f16ff0c83413b1c86fa83fc13cc1a639871f9`
