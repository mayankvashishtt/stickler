"""How sure are the rankings? Bootstrap 95% ranges and paired model-vs-model comparisons.

    python3 scripts/stats.py        # writes results/STATS.md

Resamples the 74 puzzles 10,000 times. A score range is the middle 95% of resampled scores. For two
models, the same resampled puzzles are used for both (paired), so the question is "on puzzles like
these, how often is A ahead of B?".
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from compare_report import MODELS, ROOT, load  # noqa: E402

N = 10000


def main():
    D = {}
    for tag, name in MODELS:
        recs = load(tag)
        if recs:
            D[name] = {k: int(v["solved"] in (True, "True")) for k, v in recs.items()}
    names = sorted(D, key=lambda n: -sum(D[n].values()))
    ids = sorted(set.intersection(*(set(D[n]) for n in names)))
    rng = random.Random(0)
    samples = [[rng.choice(ids) for _ in ids] for _ in range(N)]
    md = ["# Stickler: how sure are the rankings?", "",
          f"{len(ids)} puzzles, one attempt each, {N:,} bootstrap resamples. Range = middle 95%.", "",
          "| Model | Solved | 95% range |", "| --- | --- | --- |"]
    for n in names:
        s = sorted(sum(D[n][i] for i in smp) for smp in samples)
        md.append(f"| {n} | {sum(D[n][i] for i in ids)} | {s[int(N * .025)]} to {s[int(N * .975)]} |")
    md += ["", "Neighbours on the table, paired:", "", "| A vs B | A minus B | 95% range | A ahead in |",
           "| --- | --- | --- | --- |"]
    for a, b in zip(names, names[1:]):
        d = sorted(sum(D[a][i] - D[b][i] for i in smp) for smp in samples)
        ahead = sum(x > 0 for x in d) / N
        md.append(f"| {a} vs {b} | {sum(D[a][i] - D[b][i] for i in ids):+d} | {d[int(N * .025)]:+d} to "
                  f"{d[int(N * .975)]:+d} | {ahead:.0%} of resamples |")
    md += ["", "A gap is clear when its range does not include 0. One attempt per puzzle; runs repeated 3 times",
           "would also capture a model's own run-to-run luck."]
    open(os.path.join(ROOT, "results", "STATS.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
