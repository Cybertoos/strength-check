# Strength check, sweep: plan, fixed before results (2026-09-30)

## Question

The first run (PLAN.md) used Qwen3.8-27B with no reasoning and gpt-oss-20b at low effort. Neither separated lines that overstate their source from lines that match it. Does a different setting or model family do better on the same cases and the same prompt?

## Setup

- Cases: the public `cases/real.jsonl` (29) then `cases/planted.jsonl` (23), in file order, 52 in all. Unchanged from the first run.
- Prompt: `prompt.md`, unchanged. Parsing and validation: `check.parse`, unchanged.
- `sweep.py`: one request per case, temperature 0, at most 8,000 output tokens, one retry on an invalid reply. Models run one at a time in LM Studio on one Mac, one request at a time.
- Arms, in run order:

| Arm | Model | Reasoning effort |
|---|---|---|
| qwen-low | qwen/qwen3.8-27b | low |
| gptoss-high | openai/gpt-oss-20b | high |
| glm4 | glm-4-32b-0414 | field omitted |
| phi4 | phi-4 | field omitted |

## Metrics

For each arm, with counts and 95% Wilson intervals:

1. "claims more" on real stronger lines (9), on planted lines (23), and on controls (14).
2. Separation: "claims more" on real stronger lines minus on controls, in points.
3. Invalid replies after one retry.

For each pair of arms, and with each first-run model, the two-model rule of PLAN.md: flag, ask a person, pass, on the same three sets.

## What would surprise us

- Expected: no arm separates by more than 30 points; reasoning helps Qwen a little.
- Surprising: an arm with "claims more" on at least 7 of 9 real stronger lines and at most 4 of 14 controls.

## Stop rules

- An arm with more than 10% invalid replies is reported as such; its verdicts are still analysed.
- The night runner stops an arm after a run fails twice; what ran is reported, what did not is listed.
- No change to cases, prompt or arms after the first sweep run, except as a dated entry in DEVIATIONS.md.

## What this cannot show

The same as PLAN.md: labels from one model verifier, few cases, one topic, no retrieval.
