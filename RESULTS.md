# Results

Run on 2026-09-30 on one Mac, both models in LM Studio, one request at a time. Every number here is printed by `analyze.py` into `results/numbers.md`, or for the sweep by `analyze_sweep.py` into `results/numbers-sweep.md`. The plan, fixed before the run: `PLAN.md`. Changes since: `DEVIATIONS.md`.

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
- 29 real lines from seven notes written in one session on one topic, several citing the same paper. The intervals are wide.
- Three real cases were removed after the run (DEVIATIONS item 1), two of them overstated lines, so the real overstated set went from 11 to 9.
- The 23 planted edits come from 11 holding lines, up to four from one line, so they are not independent. Their intervals are too narrow.
- Planted edits are rule-based; some drop a detail without widening the claim (listed in `cases/planted-diff.txt`). The 83% planted catch comes mostly from lines sent to a person (12 of 19).
- Two small local models, one prompt, one setting each. It says nothing about larger models.
- Retrieval was not tested.

## Sweep: other settings and models

Run on the night of 2026-09-30 to 2026-10-01, same 52 cases, same prompt, plan fixed before the run: `PLAN-sweep.md`. Numbers from `analyze_sweep.py` into `results/numbers-sweep.md`. Nothing was changed after the sweep started.

| Arm | "Claims more" on real overstated lines | On controls | Separation, points (95% CI) | Invalid replies |
|---|---|---|---|---|
| Qwen3.8-27B, no reasoning (first run) | 8 of 9 | 10 of 14 | +17 (-19 to +45) | 0 of 52 |
| gpt-oss-20b, low (first run) | 3 of 9 | 3 of 13 | +10 (-24 to +45) | 1 of 52 |
| Qwen3.8-27B, low | 9 of 9 | 9 of 14 | +36 (0 to +61) | 0 of 52 |
| gpt-oss-20b, high | 4 of 5 | 3 of 13 | +57 (+7 to +79) | 13 of 52 |
| GLM-4-32B | 8 of 9 | 6 of 14 | +46 (+5 to +69) | 0 of 52 |
| phi-4 | 7 of 8 | 3 of 12 | +62 (+18 to +82) | 3 of 52 |

Rates count only cases with a valid verdict, so the denominators differ between arms. Separation is the rate on real overstated lines minus the rate on controls; its interval is Newcombe's hybrid score method.

- **The plan's expectation failed.** It expected no arm to separate by more than 30 points. Four did: Qwen at low effort, gpt-oss-20b at high effort, GLM-4-32B and phi-4. All four intervals are wide; Qwen's starts at 0, and gpt-oss-20b's rests on 5 overstated lines (below).
- **Reasoning helped Qwen on overstated lines, not on controls.** At low effort it says "claims more" on 9 of 9 real overstated lines (from 8, the ceiling) and 19 of 23 planted lines (from 15), and on 9 of 14 controls (from 10). One run each, so whether this is a change in judgement or chance is not tested.
- **gpt-oss-20b at high effort is not usable at this budget.** 13 of 52 replies hit the 8,000-token cap twice with no answer, 4 of them real overstated lines. Its +57 rests on the 5 real overstated lines it finished. Whether those are easier or harder than the rest is unknown, so its numbers cannot be compared with the others.
- **phi-4 met the plan's surprise bar, narrowly, and that is not yet a finding.** The plan's bar counts all 9 overstated lines and all 14 controls, with an invalid reply counted as not "claims more": phi-4 had 7 of 9 and 3 of 14 (bar: at least 7 and at most 4). Over valid replies only, as in the table, that is 7 of 8 and 3 of 12. Three replies failed validation (wrong field values, not the token cap): one real overstated line and two controls. Had both controls been "claims more", it would miss the bar. It said "claims more" on only 11 of 23 planted lines.
- **GLM-4-32B** flags 6 of 14 controls and only 9 of 23 planted lines.
- **Two-model rule, by controls sent on.** Picked after the run: among pairs of different models whose arms both have at most 10% invalid replies, the fewest controls go to a flag or a person with GLM-4-32B and phi-4 (5 of 12) and with gpt-oss-20b at low effort and phi-4 (also 5 of 12), against 10 of 13 in the first run. gpt-oss-20b at high effort with phi-4 sends 4 of 12, but that arm has 13 of 52 invalid replies and only 5 valid overstated lines. GLM-4-32B with phi-4 still sends 8 of 8 real overstated lines on (7 flagged, 1 to a person). It passes 10 of 23 planted lines. A case drops out of a pair when either model has no valid verdict, hence 8 and 12.

### What changes

The first run's answer was that the checker moves reading to a person instead of saving it. On the sweep, three usable arms separate real overstated lines from controls by more than the first run did. phi-4, alone or paired with GLM-4-32B, separates most. That is one result picked from six arms and fourteen pairs, on the same 9 overstated lines and 14 controls the first run was judged on, with no held-out cases, so the best of them is favoured by chance. It is a lead to test on new cases labelled by a person, not a result. The weak planted catch (under half for GLM-4-32B and phi-4) suggests the gain does not come from reading the qualifiers that `plant.py` removes; this is not tested.

### What the sweep cannot show

Everything under "What this cannot show" above still holds, including that the 23 planted lines come from 11 holding lines and are not independent. Also: gpt-oss-20b at high effort ran out of tokens on a quarter of the cases, in unknown direction; GLM-4-32B and phi-4 ran with no reasoning setting; all arms ran on the same cases, so the arms are not independent samples.
