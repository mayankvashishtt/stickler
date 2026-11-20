"""CLI: python3 -m stickler {show,validate,run,bench,export,score}"""
import argparse
import sys

from .episode import prompt
from .gen import generate
from .runner import SUITES, bench_suite, build_suite, run_suite


def ints(s):
    out = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += range(int(a), int(b) + 1)
        else:
            out.append(int(part))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog="stickler")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("show", help="print the prompt for one task")
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--depth", type=int, default=2)
    s.add_argument("--size", default="m")
    s.add_argument("--rule", action="store_true", help="also print the hidden rule")
    for name in ("validate", "run"):
        p = sub.add_parser(name)
        p.add_argument("--seeds", default="0-9")
        p.add_argument("--depths", default="1,2,3")
        p.add_argument("--sizes", default="s,m,l")
        p.add_argument("--train", type=int, default=4, help="number of example pairs")
        p.add_argument("--workers", type=int, default=4)
        p.add_argument("--out")
        p.add_argument("--families", default="chain", help="chain,life,count,sizecolor")
        if name == "run":
            p.add_argument("--agent", default="claude")
            p.add_argument("--model")
            p.add_argument("--turns", type=int, default=1)
    b = sub.add_parser("bench", help="run a model on the fixed 74-puzzle leaderboard set")
    b.add_argument("--agent", default="openai", help="openai (any OpenAI-compatible API), claude or codex")
    b.add_argument("--model", required=True)
    b.add_argument("--workers", type=int, default=4)
    b.add_argument("--out", help="default results/<model>")
    b.add_argument("--suite", default="main", help="main (the 74), steps (rule applied 3 times), fix (correct a near miss), marathon (large busy grids, rule applied 6 times), trap, tables (same test on tables of numbers)")
    e = sub.add_parser("export", help="write the 74 puzzles as JSONL (prompt + answer) for any harness")
    e.add_argument("--out", default="data/stickler-74.jsonl")
    sc = sub.add_parser("score", help="score a predictions JSONL ({id, reply} or {id, grid}) against the 74")
    sc.add_argument("predictions")
    a = ap.parse_args(argv)

    if a.cmd == "bench":
        suffix = "" if a.suite == "main" else "-" + a.suite
        out = a.out or "results/" + a.model.replace("/", "_").replace(":", "_") + suffix
        tasks = bench_suite() if a.suite == "main" else SUITES[a.suite]()
        recs = run_suite(a.agent, tasks, 1, a.model, a.workers, out)
        print(f"\n{a.model}: solved {sum(r['solved'] for r in recs)}/{len(recs)}  -> {out}/results.jsonl")
        return
    if a.cmd == "export":
        import json
        import os
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        with open(a.out, "w") as f:
            for t in bench_suite():
                f.write(json.dumps({"id": t.id, "prompt": prompt(t), "train": t.train, "test_input": t.test_in,
                                    "answer": t.test_out}) + "\n")
        print(f"wrote {a.out}")
        return
    if a.cmd == "score":
        import json
        from .episode import parse_answer
        gold = {t.id: t.test_out for t in bench_suite()}
        got = {}
        for line in open(a.predictions):
            r = json.loads(line)
            got[r["id"]] = r["grid"] if "grid" in r else parse_answer(r.get("reply") or "")[0]
        solved = sum(1 for k, v in gold.items() if got.get(k) == v)
        missing = sum(1 for k in gold if k not in got)
        print(f"solved {solved}/{len(gold)}" + (f"  ({missing} puzzles had no prediction)" if missing else ""))
        return

    if a.cmd == "show":
        t = generate(a.seed, a.depth, a.size)
        print(prompt(t))
        if a.rule:
            print("\n# hidden rule:", t.rule(), f"(fits: {t.n_consistent} short rules, all agree)")
        return
    tasks = build_suite(ints(a.seeds), ints(a.depths), a.sizes.split(","), a.train, a.families.split(","))
    if a.cmd == "validate":
        oracle = run_suite("oracle", tasks, workers=a.workers)
        copy = run_suite("copy", tasks, workers=a.workers)
        print(f"\noracle solved {sum(r['solved'] for r in oracle)}/{len(oracle)}")
        print(f"copy baseline solved {sum(r['solved'] for r in copy)}/{len(copy)}")
        sys.exit(0 if all(r["solved"] for r in oracle) else 1)
    recs = run_suite(a.agent, tasks, a.turns, a.model, a.workers, a.out)
    print(f"\nsolved {sum(r['solved'] for r in recs)}/{len(recs)}")


if __name__ == "__main__":
    main()
