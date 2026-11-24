"""Scores for the extra levels (many steps, trap, fix the slip, tables) for the website.

    python3 scripts/export_layers.py      # writes web/layers.json
"""
import json
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
MODELS = [("gpt-astra", "GPT-6.2-Astra"), ("fable", "Fable 5.2"), ("claude", "Opus 5.5"), ("gpt-sol", "GPT-6.2-Sol"),
          ("sonnet", "Sonnet 5.5"), ("haiku", "Haiku 5.5")]
LAYERS = [("hardboard", "Hard board", "Life-like rules where the neighbours are hidden: only the 4 sides, only the diagonals, knight moves, or 2 squares along a row. Work out which squares count, then apply it to big grids."),
          ("steps", "Many steps", "Apply the rule 3 times in a row. One early slip spreads."),
          ("trap", "Trap", "The rule is one number off the famous Game of Life. The examples show the difference. Most fails used the famous rule anyway."),
          ("fix", "Fix the slip", "Given a near-miss answer and told exactly how many squares are wrong, fix it."),
          ("tables", "Tables (control)", "The same test on tables of numbers, up to 48 rows. Everyone does well, so the grid failures are about 2D, not maths.")]


def g(grid):
    return None if grid is None else ["".join(str(c) for c in row) for row in grid]


def main():
    out = {"layers": []}
    for key, title, what in LAYERS:
        layer = {"key": key, "title": title, "what": what, "models": {}, "n": 0}
        for tag, name in MODELS:
            f = os.path.join(ROOT, "results", f"{tag}-{key}", "results.jsonl")
            if not os.path.exists(f):
                continue
            recs = [json.loads(line) for line in open(f)]
            layer["n"] = max(layer["n"], len(recs))
            layer["models"][name] = {"solved": sum(r["solved"] for r in recs), "n": len(recs),
                                     "items": {r["id"]: {"solved": r["solved"], "acc": r["cell_acc"], "pred": g(r.get("pred"))}
                                               for r in recs}}
        out["layers"].append(layer)
    json.dump(out, open(os.path.join(ROOT, "web", "layers.json"), "w"), separators=(",", ":"))
    for l in out["layers"]:
        print(l["title"], {m: f'{v["solved"]}/{v["n"]}' for m, v in l["models"].items()})


if __name__ == "__main__":
    main()
