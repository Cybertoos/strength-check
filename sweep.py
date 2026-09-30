#!/usr/bin/env python3
"""Sweep run: one model setting over the public cases, one case per call (PLAN-sweep.md).

Usage: sweep.py --model M --effort none|low|medium|high|omit --start K --tasks K+1 --out results/sweep-X.jsonl
Cases are cases/real.jsonl then cases/planted.jsonl, in file order. Appends one record per case.
"""
import argparse, datetime, hashlib, json, time, urllib.request
from pathlib import Path

import check

HERE = Path(__file__).parent


def cases():
    rows = []
    for f in ("cases/real.jsonl", "cases/planted.jsonl"):
        rows += [json.loads(l) for l in open(HERE / f) if l.strip()]
    return rows


def ask(model, effort, max_tokens, system, user):
    body = {"model": model, "temperature": 0, "max_tokens": max_tokens,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    if effort != "omit":
        body["reasoning_effort"] = effort
    req = urllib.request.Request(check.BASE, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--effort", required=True)
    ap.add_argument("--max-tokens", type=int, default=8000)
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--tasks", type=int, required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    system, user_t = check.load_prompt()
    prompt_sha = hashlib.sha256((system + user_t).encode()).hexdigest()[:12]
    out = HERE / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    for c in cases()[a.start:a.tasks]:
        user = user_t.replace("{passage}", c["passage"]).replace("{claim}", c["claim"])
        rec = {"id": c["id"], "model": a.model, "effort": a.effort, "prompt_sha": prompt_sha,
               "date": datetime.date.today().isoformat(), "result": None, "attempts": []}
        for _ in range(2):
            t0 = time.time()
            try:
                resp = ask(a.model, a.effort, a.max_tokens, system, user)
                msg = resp["choices"][0]["message"]
                raw = msg.get("content") or ""
                rec["attempts"].append({"raw": raw, "finish": resp["choices"][0].get("finish_reason"),
                                        "seconds": round(time.time() - t0, 1), "usage": resp.get("usage")})
                rec["result"] = check.parse(raw)
                break
            except Exception as e:
                rec["attempts"].append({"error": f"{type(e).__name__}: {e}", "seconds": round(time.time() - t0, 1)})
        with out.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print(c["id"], (rec["result"] or {}).get("verdict", "FAILED"), rec["attempts"][-1].get("seconds"))


if __name__ == "__main__":
    main()
