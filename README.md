# strength-check

AI tools that write literature notes usually cite real papers. The failure is quieter: a sentence says more than its source. A limit is dropped, a range becomes its upper end, "about" disappears. This repo is a first test of a checker for that: given a sentence and the passage it cites, do two local models from different families tell when the sentence claims more?

## Result

First run, no, not yet. On 9 real overstated lines and 13 lines that match their source (14 in all; one has no verdict from gpt-oss-20b), the two-model checker flagged 3 of the overstated lines and 2 of the matching ones. Counting the lines it sent to a person, it caught all 9 overstated lines, but it also sent or flagged 10 of the 13 matching ones. Qwen3.8-27B called 8 of 9 overstated lines and 10 of 14 matching lines "claims more". The two models agreed on 39% of cases.

A sweep of four more local settings on the same cases (`PLAN-sweep.md`, `sweep.py`) found a lead: phi-4 called 7 of 9 overstated lines and 3 of 14 matching lines "claims more". It is the best of six arms on cases already seen, so it needs new cases labelled by a person before it means anything. Details and intervals: `RESULTS.md`.

The labels come from one model verifier, not people. Some of the checker's false alarms name a real dropped condition; a person has to decide those.

## What was done

- **Real cases:** 29 lines from seven AI-written literature notes, each paired with a verbatim passage from the source it cites, fetched on 2026-09-30 (`cases/real.jsonl`; URLs and text hashes in `cases/SOURCES.tsv`). Labels from an earlier model verifier that read the full papers: 9 stronger, 14 holding, 3 weaker, 2 ambiguous, 1 reworded quotation.
- **Planted cases:** 23 rule-based edits meant to make a holding line stronger; some only drop a detail (`plant.py`, `cases/planted-diff.txt`).
- **Checker:** `check.py` with `prompt.md`. Qwen3.8-27B and gpt-oss-20b in LM Studio, temperature 0.
- **Decision:** flag when both models say the line claims more; ask a person when one does or either cannot tell.

Plan, fixed before the run: `PLAN.md`. Changes since, including three cases removed after the run: `DEVIATIONS.md`.

## Run it

Needs Python 3.10 or later. The analysis needs nothing else:

```
python3 analyze.py
```

To rerun the checker, load both models in LM Studio on its default port, then:

```
python3 check.py --tryout
python3 check.py cases/real.jsonl results/real.jsonl
python3 check.py cases/planted.jsonl results/planted.jsonl
```

## Licence

Code: MIT (`LICENSE`). Case labels, planted cases and results: CC BY 4.0 (`LICENSE-DATA`). The source passages are short quotations from the cited sources, under their own licences.
