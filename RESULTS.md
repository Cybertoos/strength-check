# Results

Run on 2026-09-30 on one Mac, both models in LM Studio, one request at a time. Every number here is printed by `analyze.py` into `results/numbers.md`. The plan, fixed before the run: `PLAN.md`. Changes since: `DEVIATIONS.md`.

## Headline

The checker did not separate lines that overstate their source from lines that match it. It caught every real overstated line only because it sent most lines of every kind to a person.

| Set | Flag (both models) | Ask a person | Flag or ask |
|---|---|---|---|
| Real overstated lines | 3 of 9 (33%, CI 12 to 65%) | 6 of 9 | 9 of 9 (100%, CI 70 to 100%) |
| Planted overstatements | 7 of 23 (30%, CI 16 to 51%) | 12 of 23 | 19 of 23 (83%, CI 63 to 93%) |
| Controls (lines that match) | 2 of 13 (15%, CI 4 to 42%) | 8 of 13 | 10 of 13 (77%, CI 50 to 92%) |

CI is the 95% Wilson interval. One control has no verdict from gpt-oss-20b (two invalid replies), so the controls count 13 of 14.

## Per model

- **Qwen3.8-27B** said "claims more" on 8 of 9 real overstated lines (89%) and on 10 of 14 controls (71%). It flagged most lines of both kinds.
- **gpt-oss-20b** said "claims more" on 3 of 9 real overstated lines (33%) and on 3 of 13 controls (23%). Fewer false alarms, but it missed most overstatements.
- On planted lines: Qwen 15 of 23 (65%), gpt-oss 11 of 23 (48%).
- Per edit type, flag or ask a person: hedge removed 5 of 6, range cut to its upper end 4 of 5, sample size removed 3 of 3, scope phrase removed 7 of 9.
- The two models gave the same verdict on 20 of 51 cases (39%, CI 27 to 53%).
- Rerun of 19 cases: 36 of 37 valid verdict pairs repeated. The disagreement between the models is not run-to-run noise.
- Weaker lines (3): each model called 1 of 3 "claims less". Qwen called one "claims more".

## Why the controls were flagged

The models' reasons for the 13 "claims more" verdicts on controls are listed verbatim in `results/numbers.md`. They fall into two groups:

- **The line holds details the passage does not.** Each case carries 1 to 4 sentences of the source. These lines probably merge facts from more than one place in a paper, so a model that sees one passage reads the rest as added. No analysis here tests that explanation.
- **The line drops a condition the passage states** ("with the augmented suites", "22 models", "all six model-task combinations"). The labeller marked these lines as holding. Some may be real losses the labeller accepted. Without a person's label this cannot be decided.

## Against the plan's expectations

| Plan | Expected or surprising | Observed | Met |
|---|---|---|---|
| Catch on real overstated lines (flag or ask) | expected 50 to 80%; surprising under 30% | 100% | above the expected range; not the surprise |
| Catch on planted lines | expected 60 to 90% | 83% | yes |
| Controls flagged (both models) | expected 10 to 40%; surprising over half | 15% | yes; not the surprise |
| Agreement between models | surprising under 60% | 39% | the surprise happened |

The plan set no expectation for controls sent to a person. At 8 of 13 it is the largest cost of the rule.

## What this means for the tool

- A two-model rule sends most lines to a person. On these cases it saves little reading.
- The next version should see the whole paper, or several passages, per line, and test whether "detail not in this passage" then stops counting as overstatement.
- It needs human labels. The labels here come from one model verifier, and some of the checker's false alarms may be the labeller's misses.
- A stronger checker model, or a model tuned on labelled pairs, should be tried against the same cases.

## What this cannot show

- The labels come from one model verifier, not people. The case builder disputed two of them (notes on r13 and r32).
- 29 real lines from one set of notes on one topic. The intervals are wide.
- The 23 planted edits come from 11 holding lines, up to four from one line, so they are not independent. Their intervals are too narrow.
- Planted edits are rule-based; some drop a detail without widening the claim (listed in `cases/planted-diff.txt`). The 83% planted catch comes mostly from lines sent to a person (12 of 19).
- Two small local models, one prompt, one setting each. It says nothing about larger models.
- Retrieval was not tested.
