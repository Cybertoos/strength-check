#!/usr/bin/env python3
"""Every number in the write-up, from cases/ and results/. Writes results/numbers.md.

Usage: analyze.py            # print and write results/numbers.md
       analyze.py --pick     # the 20 case ids for the run-to-run check, drawn from the 55 cases run
"""
import json, math, random, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
MODELS = ["qwen/qwen3.8-27b", "openai/gpt-oss-20b"]


def jl(p):
    p = HERE / p
    return [json.loads(l) for l in p.open() if l.strip()] if p.exists() else []


def wilson(k, n, z=1.96):
    if n == 0:
        return "n/a"
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return f"{k} of {n} ({100 * p:.0f}%, 95% CI {100 * (c - h):.0f} to {100 * (c + h):.0f}%)"


def cases():
    real = [c for c in jl("cases/real.jsonl") if c.get("passage")]
    planted = jl("cases/planted.jsonl")
    return real, planted


def verdicts(path):
    v = {}
    for r in jl(path):
        v[(r["id"], r["model"])] = (r["result"] or {}).get("verdict")
    return v


def decide(a, b):
    if a == b == "claims_more":
        return "flag"
    if (a == "claims_more") != (b == "claims_more") or "cannot_tell" in (a, b):
        return "person"
    return "pass"


def main():
    real, planted = cases()
    if "--pick" in sys.argv:
        ids = [f"r{i:02d}" for i in range(1, 33)] + [f"p{i:02d}" for i in range(1, 24)]
        print(",".join(sorted(random.Random(5).sample(sorted(ids), 20))))
        return

    v = verdicts("results/real.jsonl") | verdicts("results/planted.jsonl")
    out = []
    say = out.append

    failed = [k for k, x in v.items() if x is None]
    say(f"Replies: {len(v)} records, {len(failed)} with no valid verdict after one retry: {sorted(failed)}")

    def dec(c):
        a, b = (v.get((c["id"], m)) for m in MODELS)
        return None if a is None or b is None else decide(a, b)

    sets = {
        "real stronger": [c for c in real if c["label"] == "stronger"],
        "planted": planted,
        "controls (real holds)": [c for c in real if c["label"] == "holds"],
    }
    for name, cs in sets.items():
        ds = [dec(c) for c in cs if dec(c)]
        caught = sum(d in ("flag", "person") for d in ds)
        say(f"\n## {name}: {len(cs)} cases, {len(ds)} with both verdicts")
        say(f"- flag: {wilson(ds.count('flag'), len(ds))}")
        say(f"- ask a person: {wilson(ds.count('person'), len(ds))}")
        say(f"- flag or ask a person: {wilson(caught, len(ds))}")
        for m in MODELS:
            ms = [v.get((c["id"], m)) for c in cs if v.get((c["id"], m))]
            say(f"- {m}: claims_more {wilson(ms.count('claims_more'), len(ms))}; all verdicts {dict(Counter(ms))}")

    say("\n## planted, per operator (flag or ask a person)")
    by = defaultdict(list)
    for c in planted:
        if dec(c):
            by[c["operator"]].append(dec(c) in ("flag", "person"))
    for op, xs in sorted(by.items()):
        say(f"- {op}: {wilson(sum(xs), len(xs))}")

    say("\n## weaker lines (not in the headline)")
    for m in MODELS:
        ms = [v.get((c["id"], m)) for c in real if c["label"] == "weaker" and v.get((c["id"], m))]
        say(f"- {m}: claims_less {wilson(ms.count('claims_less'), len(ms))}; all {dict(Counter(ms))}")

    say("\n## ambiguous and reworded lines (not counted)")
    for c in real:
        if c["label"] in ("ambiguous", "reworded"):
            say(f"- {c['id']} {c['label']}: " + ", ".join(f"{m.split('/')[1]} {v.get((c['id'], m))}" for m in MODELS))

    both = [c for c in real + planted if all(v.get((c["id"], m)) for m in MODELS)]
    agree = sum(v[(c["id"], MODELS[0])] == v[(c["id"], MODELS[1])] for c in both)
    agree_more = sum((v[(c["id"], MODELS[0])] == "claims_more") == (v[(c["id"], MODELS[1])] == "claims_more") for c in both)
    say("\n## agreement between the two models, all cases")
    say(f"- same verdict: {wilson(agree, len(both))}")
    say(f"- same on claims_more or not: {wilson(agree_more, len(both))}")

    say("\n## reasons given for claims_more on controls, verbatim")
    reasons = {(r["id"], r["model"]): (r["result"] or {}).get("reason") for r in jl("results/real.jsonl")}
    for c in real:
        if c["label"] != "holds":
            continue
        for m in MODELS:
            if v.get((c["id"], m)) == "claims_more":
                say(f"- {c['id']} {m.split('/')[1]}: {reasons[(c['id'], m)]}")

    rr = jl("results/rerun.jsonl")
    if rr:
        pairs = [(r["model"], (r["result"] or {}).get("verdict"), v.get((r["id"], r["model"]))) for r in rr]
        valid = [(m, a == b) for m, a, b in pairs if a and b]
        say(f"\n## run-to-run, {len({r['id'] for r in rr})} cases rerun once per model")
        say(f"- pairs with a valid verdict both times: {len(valid)} of {len(pairs)}")
        say(f"- same verdict: {wilson(sum(x for _, x in valid), len(valid))}")
        for m in MODELS:
            s = [x for mm, x in valid if mm == m]
            say(f"- {m}: {wilson(sum(s), len(s))}")

    text = "\n".join(out) + "\n"
    print(text)
    (HERE / "results/numbers.md").write_text("# Numbers\n\nWritten by analyze.py. Do not edit.\n\n" + text)


if __name__ == "__main__":
    main()
