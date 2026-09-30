#!/usr/bin/env python3
"""Ask each model whether each case's claim says more than its passage.

Usage: check.py CASES.jsonl OUT.jsonl [--models m1,m2] [--ids r01,p03] [--tryout]
Appends one record per (case, model); a rerun skips pairs already in OUT.
"""
import argparse, datetime, hashlib, json, re, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).parent
BASE = "http://localhost:1234/v1/chat/completions"
MODELS = ["qwen/qwen3.8-27b", "openai/gpt-oss-20b"]
QUALS = ["population", "conditions", "effect_size", "uncertainty", "hedging", "date"]
QVALS = ["kept", "weakened", "strengthened", "missing", "n/a"]
VERDICTS = ["claims_more", "matches", "claims_less", "cannot_tell"]

SCHEMA = {
    "type": "object",
    "properties": {
        "qualifiers": {
            "type": "object",
            "properties": {q: {"type": "string", "enum": QVALS} for q in QUALS},
            "required": QUALS,
        },
        "verdict": {"type": "string", "enum": VERDICTS},
        "evidence": {"type": "string"},
        "reason": {"type": "string"},
    },
    "required": ["qualifiers", "verdict", "evidence", "reason"],
}


def load_prompt():
    text = (HERE / "prompt.md").read_text()
    blocks = re.findall(r"^## (System|User)\n\n```\n(.*?)\n```", text, re.S | re.M)
    parts = dict(blocks)
    return parts["System"], parts["User"]


def ask(model, system, user):
    body = {
        "model": model,
        "temperature": 0,
        "reasoning_effort": "low" if "gpt-oss" in model else "none",
        "max_tokens": 4000,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }
    req = urllib.request.Request(BASE, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.load(r)


def parse(content):
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.S).strip()
    m = re.search(r"\{.*\}", content, re.S)
    out = json.loads(m.group(0))
    assert out["verdict"] in VERDICTS
    assert all(out["qualifiers"].get(q) in QVALS for q in QUALS)
    return out


def tryout_cases():
    text = (HERE / "prompt.md").read_text()
    rows = re.findall(r'^\d\. Passage: "(.*?)" Sentence: "(.*?)" Expected: (\w+)', text, re.M)
    return [{"id": f"t{i+1}", "passage": p, "claim": c, "expected": e} for i, (p, c, e) in enumerate(rows)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cases", nargs="?")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--models", default=",".join(MODELS))
    ap.add_argument("--ids")
    ap.add_argument("--tryout", action="store_true")
    a = ap.parse_args()

    system, user_t = load_prompt()
    prompt_sha = hashlib.sha256((system + user_t).encode()).hexdigest()[:12]
    if a.tryout:
        cases, out = tryout_cases(), None
    else:
        cases = [json.loads(l) for l in open(a.cases) if l.strip()]
        out = Path(a.out)
    cases = [c for c in cases if c.get("passage")]
    if a.ids:
        keep = set(a.ids.split(","))
        cases = [c for c in cases if c["id"] in keep]

    done = set()
    if out and out.exists():
        done = {(r["id"], r["model"]) for r in map(json.loads, out.open()) if r.get("result")}

    for model in a.models.split(","):
        for c in cases:
            if (c["id"], model) in done:
                continue
            user = user_t.replace("{passage}", c["passage"]).replace("{claim}", c["claim"])
            rec = {"id": c["id"], "model": model, "prompt_sha": prompt_sha,
                   "date": datetime.date.today().isoformat(), "result": None, "attempts": []}
            for attempt in range(2):
                t0 = time.time()
                try:
                    resp = ask(model, system, user)
                    msg = resp["choices"][0]["message"]
                    raw = msg.get("content") or ""
                    rec["attempts"].append({"raw": raw, "seconds": round(time.time() - t0, 1),
                                            "usage": resp.get("usage")})
                    rec["result"] = parse(raw)
                    break
                except Exception as e:
                    rec["attempts"].append({"error": f"{type(e).__name__}: {e}", "seconds": round(time.time() - t0, 1)})
            if a.tryout:
                r = rec["result"] or {}
                print(model, c["id"], "expected", c["expected"], "got", r.get("verdict"), r.get("qualifiers"))
            else:
                with out.open("a") as f:
                    f.write(json.dumps(rec) + "\n")
                print(model, c["id"], (rec["result"] or {}).get("verdict", "FAILED"),
                      rec["attempts"][-1].get("seconds"), file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
