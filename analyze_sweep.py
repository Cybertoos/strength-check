#!/usr/bin/env python3
"""Every number for PLAN-sweep.md, from cases/ and results/. Writes results/numbers-sweep.md."""
import json
import math
from collections import Counter
from itertools import combinations

from analyze import HERE, MODELS, cases, decide, jl, verdicts, wilson

ARMS = ["qwen-low", "gptoss-high", "glm4", "phi4"]
FIRST = {"qwen-none": MODELS[0], "gptoss-low": MODELS[1]}


def wilson_bounds(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def newcombe(k1, n1, k2, n2):
    """95% interval for p1 - p2 from two independent groups, Newcombe's hybrid score method, in points."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson_bounds(k1, n1)
    l2, u2 = wilson_bounds(k2, n2)
    lo = p1 - p2 - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = p1 - p2 + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return 100 * lo, 100 * hi


def arm_verdicts():
    first = verdicts("results/real.jsonl") | verdicts("results/planted.jsonl")
    v = {a: {c: x for (c, m), x in first.items() if m == model} for a, model in FIRST.items()}
    raw = {}
    for a in ARMS:
        rs = jl(f"results/sweep-{a}.jsonl")
        raw[a] = rs
        v[a] = {r["id"]: (r["result"] or {}).get("verdict") for r in rs}
    return v, raw


def main():
    real, planted = cases()
    sets = {
        "real stronger": [c["id"] for c in real if c["label"] == "stronger"],
        "planted": [c["id"] for c in planted],
        "controls": [c["id"] for c in real if c["label"] == "holds"],
    }
    v, raw = arm_verdicts()
    out = []
    say = out.append

    say("## Per arm: \"claims more\" and invalid replies")
    say("\nRates over cases with a valid verdict. Separation: real stronger minus controls.")
    say("\n| Arm | Real stronger | Planted | Controls | Separation (points) | Invalid |")
    say("|---|---|---|---|---|---|")
    for a in list(FIRST) + ARMS:
        cells, kn = [], {}
        for name, ids in sets.items():
            ms = [v[a].get(i) for i in ids if v[a].get(i)]
            kn[name] = (ms.count("claims_more"), len(ms))
            cells.append(wilson(*kn[name]))
        (k1, n1), (k2, n2) = kn["real stronger"], kn["controls"]
        lo, hi = newcombe(k1, n1, k2, n2)
        sep = f"{100 * (k1 / n1 - k2 / n2):+.0f} (95% CI {lo:+.0f} to {hi:+.0f})"
        n = len(raw.get(a) or v[a])
        bad = sum(x is None for x in v[a].values())
        cells += [sep, f"{bad} of {n}"]
        say(f"| {a} | " + " | ".join(cells) + " |")

    say("\n## Invalid replies after one retry, by cause of the last attempt")
    for a in ARMS:
        bad = [r for r in raw[a] if not (r["result"] or {}).get("verdict")]
        cause = Counter("output token cap" if any(x.get("finish") == "length" for x in r["attempts"]) else "reply failed validation" for r in bad)
        say(f"- {a}: {len(bad)}: {dict(cause)}; ids {[r['id'] for r in bad]}")

    say("\n## All verdicts per arm and set")
    for a in ARMS:
        for name, ids in sets.items():
            say(f"- {a}, {name}: {dict(Counter(v[a].get(i) for i in ids))}")

    say("\n## Surprise test: at least 7 of 9 real stronger and at most 4 of 14 controls")
    for a in ARMS:
        s = sum(v[a].get(i) == "claims_more" for i in sets["real stronger"])
        c = sum(v[a].get(i) == "claims_more" for i in sets["controls"])
        miss = sum(v[a].get(i) is None for i in sets["controls"])
        say(f"- {a}: {s} of {len(sets['real stronger'])} and {c} of {len(sets['controls'])} ({miss} controls invalid): {'met' if s >= 7 and c <= 4 else 'not met'}")

    say("\n## Two-model rule for every pair (flag / ask a person / pass)")
    say("\nA case is left out of a pair when either arm has no valid verdict on it.")
    say("\n| Pair | Real stronger | Planted | Controls |")
    say("|---|---|---|---|")
    for x, y in combinations(list(FIRST) + ARMS, 2):
        if x in FIRST and y in FIRST:
            continue
        cells = []
        for ids in sets.values():
            ds = [decide(v[x][i], v[y][i]) for i in ids if v[x].get(i) and v[y].get(i)]
            caught = sum(d != "pass" for d in ds)
            cells.append(f"{ds.count('flag')} / {ds.count('person')} / {ds.count('pass')} of {len(ds)}; flag or ask {caught} of {len(ds)}")
        say(f"| {x} + {y} | " + " | ".join(cells) + " |")

    text = "\n".join(out) + "\n"
    print(text)
    (HERE / "results/numbers-sweep.md").write_text("# Numbers, sweep\n\nWritten by analyze_sweep.py. Do not edit.\n\n" + text)


if __name__ == "__main__":
    main()
