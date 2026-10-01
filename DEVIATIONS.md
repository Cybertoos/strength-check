# Deviations from the plan

Items 1 to 4 dated 2026-09-30, after the first run; items 5 to 8 dated 2026-10-01, after the sweep.

1. **Three real cases removed.** r04 (weaker), r08 (stronger) and r15 (stronger) are lines whose text names private projects of the author. They were run like every other case; their records are removed from `cases/real.jsonl`, `results/real.jsonl` and `results/rerun.jsonl`. No other verdict changes. With them, the real stronger set was 11 cases: flag 3 of 11, flag or ask a person 11 of 11; Qwen3.8-27B said "claims more" on 8 of 11 and gpt-oss-20b on 4 of 11. Without them: 3 of 9, 9 of 9, 8 of 9 and 3 of 9. Agreement between the models was 22 of 54 with them and 20 of 51 without.
2. **Full source texts not published.** The plan names `cases/sources/`, the saved text of each source. Most sources do not allow redistribution, so the repo ships only the passages in `cases/real.jsonl` and, in `cases/SOURCES.tsv`, each source's URL, fetch date and the SHA-256 of the text extracted from it.
3. **Labeller notes replaced.** The labeller's working notes are not published. Three cases carry a short plain note instead: r03 (a line whose direction is mixed) and r13 and r32 (labels the case builder disputed; the labels are kept as the labeller made them).
4. **Run-to-run count.** The plan draws 20 cases with seed 5 from the 55 cases run; `analyze.py --pick` reproduces the draw. r08 is one of them and is removed (item 1), so 19 cases are reported. One pair, r26 on gpt-oss-20b, had no valid verdict in either run and is left out of the repeat count.
5. **One planting rule never applied.** PLAN.md lists widening a quantifier ("some" or "several" to "all", "one study" to "studies"). No holding line had a match, so it produced no planted case. This was visible in `cases/planted-diff.txt` on 2026-09-30 but recorded only on 2026-10-01, after a review caught it. The planted set has four operators: scope phrase 9, hedge 6, range upper end 5, sample size 3.

## Sweep, 2026-10-01, after the sweep ran

6. **No change to cases, prompt or arms.** The sweep ran as `PLAN-sweep.md` fixed it.
7. **Separation interval added.** `PLAN-sweep.md` asks for Wilson intervals on each count. The separation (real overstated minus controls) is also given a 95% interval by Newcombe's hybrid score method, chosen after the run. It treats the two sets as independent, though they share some sources and one model reads both.
8. **Invalid replies left out of rates.** The plan does not say how to count them. Rates use valid replies only; the plan's surprise bar is checked over all cases with an invalid reply counted as not "claims more" (RESULTS.md says both).
