# Strength check: plan, fixed before results (2026-09-30)

## Question

Given a sentence and the source passage it cites, can two local models from different families tell when the sentence claims more than the source? How often do they raise a false alarm on sentences that match their source?

This is a first test of the compare and cross-check steps of a larger tool. Finding and retrieving the source passage is not tested: every case comes with its passage.

## Cases

- **Real.** Lines from seven AI-written literature notes made on 2026-09-30, each paired with the passage of the paper it cites. An earlier verifier (a Claude agent that read the full papers) marked each line as holding, stronger than the source, weaker, ambiguous or a reworded quotation. Its labels are used as they are. No person labelled them. The passages were copied verbatim from the papers, fetched again on 2026-09-30, and each is checked against the saved text. `cases/real.jsonl`, `cases/sources/`.
- **Planted.** Each real line labelled as holding is made stronger by rule-based edits, one edit per planted case (`plant.py`, no model). Operators: remove a hedge word ("about", "roughly", "up to", "may", "suggests" and similar); replace a range "X to Y" by its upper end; widen a quantifier ("some" or "several" to "all", "one study" to "studies"); delete a scope phrase that names where the result was measured ("in one ...", "on ...", "among ..."); delete a stated interval or sample size. An edit that does not apply to a line is skipped. Some scope and sample edits drop a detail without widening the claim; they are kept and counted as planted, and results are shown per operator so a reader can set them aside. `cases/planted.jsonl`, with each edit listed in `cases/planted-diff.txt`.
- **Controls.** The holding lines, unchanged.

## Checker

`check.py` sends each case to each model once, one request at a time, temperature 0, at most 4,000 output tokens, reasoning effort `none` for Qwen and `low` for gpt-oss, with the prompt in `prompt.md`. The model returns JSON: a verdict for each of six qualifiers (population, conditions, effect size, uncertainty, hedging, date), each kept, weakened, strengthened, missing or not applicable, and an overall verdict: `claims_more`, `matches`, `claims_less` or `cannot_tell`, with the source words it relied on.

Models, both run locally in LM Studio on one Mac: `qwen/qwen3.8-27b` and `openai/gpt-oss-20b`. Neither is from the family of the verifier that made the labels.

Tool decision per case:

- **flag:** both models say `claims_more`.
- **ask a person:** exactly one says `claims_more`, or either says `cannot_tell`.
- **pass:** otherwise.

## Metrics

1. Catch rate on real stronger lines: flag or ask a person, over real stronger lines. Also flag alone.
2. Catch rate on planted lines, overall and per operator.
3. False alarm on controls: flag, over controls. Also the share sent to a person, which is the reviewing work the tool creates.
4. Per model: `claims_more` rate on each set, and agreement between the two models.
5. Weaker lines: share each model marks `claims_less`. Reported, not used for the headline.
6. Run-to-run: 20 cases, drawn with seed 5, rerun once per model. Share with the same verdict.

Each rate is printed with its count and a 95% Wilson interval by `analyze.py`. Ambiguous and reworded lines are reported but not counted in any rate.

## What would surprise us

- Expected: catch 50 to 80% of real stronger lines and 60 to 90% of planted ones; flag 10 to 40% of controls, because the notes compress their sources and a strict checker reads compression as a claim.
- Surprising: catch under 30% of real stronger lines; flag more than half of the controls; the two models agree on under 60% of cases.

## Stop rules

- The prompt may be tried only on three examples written for the purpose (in `prompt.md`), never on the cases, before the run.
- A reply that is not valid JSON is retried once; if more than 10% of replies still fail for a model, the run stops, the failure is reported, and any prompt change is a dated entry in DEVIATIONS.md.
- No change to cases, operators, prompt or decision rule after the first real run starts, except as a dated deviation.

## What this cannot show

- The labels are from one model verifier, not people. A disagreement between the checker and a label may be the label's error.
- The cases come from one session of notes on one topic (evaluation research). They are few, so the intervals are wide.
- Planted edits are rule-based. Real strengthening is often subtler, so the planted catch rate is an upper bound for real use.
- Retrieval is not tested.

## Timebox

One evening to build, one run on one Mac. $0: no paid model is called.

## Licence

Code MIT. Case data CC BY 4.0, except the source passages, which are short quotations from the cited papers under their own licences.
