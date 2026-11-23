"""Export the 74 compared puzzles + every model's answer for the web game.

    python3 scripts/export_web.py      # writes web/puzzles.json
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from compare_report import CATS, MODELS, load  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")


def g(grid):
    return None if grid is None else ["".join(str(c) for c in row) for row in grid]


def rule_line(reply):
    if not reply:
        return None
    m = re.search(r"\*\*Rule:?\*\*:?\s*(.+)", reply)
    line = (m.group(1) if m else reply.strip().splitlines()[0]).strip()
    return line[:260]


def main():
    by_model = {name: load(tag) for tag, name in MODELS}
    ref = by_model[MODELS[0][1]]
    out = []
    for pid in sorted(ref):
        r = ref[pid]
        cat = next((c for c in CATS if pid.split("/")[0] in c[2]), None)
        if cat is None:
            continue
        p = {"id": pid, "cat": cat[0], "hint": cat[1], "rule": r["rule"],
             "train": [[g(a), g(b)] for a, b in r["train"]], "test": g(r["test_in"]), "answer": g(r["expected"]),
             "models": {}}
        for _, name in MODELS:
            m = by_model[name].get(pid)
            if m:
                p["models"][name] = {"solved": m["solved"], "acc": m["cell_acc"], "secs": m.get("seconds"),
                                     "pred": g(m.get("pred")), "said": rule_line((m.get("replies") or [None])[-1])}
        out.append(p)
    json.dump(out, open(os.path.join(ROOT, "web", "puzzles.json"), "w"), separators=(",", ":"))
    print(len(out), "puzzles", os.path.getsize(os.path.join(ROOT, "web", "puzzles.json")) // 1024, "KB")


if __name__ == "__main__":
    main()
