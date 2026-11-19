"""Small (6-10 square) puzzles for the daily game.

    python3 scripts/export_daily.py [N]     # writes web/daily.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from stickler.gen import generate  # noqa: E402
from stickler.hard import generate_hard  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")


def g(grid):
    return ["".join(str(c) for c in row) for row in grid]


def pack(t, kind):
    return {"id": t.id, "kind": kind, "rule": t.rule(), "train": [[g(a), g(b)] for a, b in t.train],
            "test": g(t.test_in), "answer": g(t.test_out)}


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    # weekly rhythm: easy early in the week, harder later
    plan = ["chain1", "chain2", "sizecolor", "chain2", "count", "chain2", "life"]
    out, seed = [], 5000
    while len(out) < n:
        kind = plan[len(out) % len(plan)]
        seed += 1
        try:
            t = generate(seed, depth=int(kind[-1]), size="s") if kind.startswith("chain") \
                else generate_hard(seed, kind, size="s")
        except Exception:
            continue
        if t is None or t.test_in == t.test_out:
            continue
        out.append(pack(t, kind))
        print(len(out), kind, t.id, flush=True)
    json.dump(out, open(os.path.join(ROOT, "web", "daily.json"), "w"), separators=(",", ":"))
    print("wrote web/daily.json", len(out))


if __name__ == "__main__":
    main()
