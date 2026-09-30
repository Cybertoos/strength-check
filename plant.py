#!/usr/bin/env python3
"""Make each holding line stronger with one rule-based edit per planted case.

Usage: plant.py cases/real.jsonl > cases/planted.jsonl
Each operator applies at its first match only. A line where an operator
does not match gets no case for that operator.
"""
import json, re, sys

HEDGES = r"\b(?:(?:about|approximately|roughly|nearly|around|at most|up to)\s+(?=\d|half\b|two\b|five\b)|(?:may|might|likely|suggests? that)\s+)|~(?=\d)"
NUM = r"\d[\d.,]*%?"


def hedge(s):
    return re.sub(HEDGES, "", s, count=1, flags=re.I)


def range_upper(s):
    # "26-73%" -> "73%"; "7 to 19 points" -> "19 points". Not "from X to Y", which is a change, not a range.
    for m in re.finditer(rf"(?<![\w.-])({NUM})\s*(?:to|-|–)\s*(?:about\s+)?({NUM})(?![\w.-]*[A-Za-z])", s):
        if re.search(r"\bfrom\b", s[max(0, m.start() - 40):m.start()]):
            continue
        return s[:m.start()] + m.group(2) + s[m.end():]
    return s


def quantifier(s):
    for a, b in [(r"\bsome\b", "all"), (r"\bseveral\b", "all"), (r"\bone study\b", "studies"),
                 (r"(?<!at )\bmost\b(?! common)", "all")]:
        t = re.sub(a, b, s, count=1)
        if t != s:
            return t
    return s


def scope(s):
    # a parenthetical, else a short trailing phrase naming where or for whom the result holds
    t = re.sub(r"\s*\([^()%]{2,60}\)", "", s, count=1)
    if t != s:
        return t
    return re.sub(r",?\s+(?:for|in|on|among|at|depending on|with)\s+[^,;:.\"()]{3,40}(?=[;.\"]?$|[;.\"])", "", s, count=1)


def sample(s):
    return re.sub(r"\b\d[\d,.]*(?: million)? (?:labels|summaries|tasks|models|LLMs|completions|studies|hypotheses|annotations)\b[^,;:\"]*[,;:]\s*",
                  "", s, count=1)


OPS = {"hedge": hedge, "range_upper": range_upper, "quantifier": quantifier, "scope": scope, "sample": sample}


def main():
    n = 0
    for line in open(sys.argv[1]):
        c = json.loads(line)
        if c["label"] != "holds" or not c.get("passage"):
            continue
        for name, op in OPS.items():
            new = op(c["claim"]).strip()
            if new == c["claim"].strip():
                continue
            n += 1
            print(json.dumps({"id": f"p{n:02d}", "from": c["id"], "operator": name, "claim": new,
                              "passage": c["passage"], "source": c["source"], "label": "stronger"}))


if __name__ == "__main__":
    main()
