"""CLI: python3 -m gridforge {show,validate,run}"""
import argparse
import sys

from .episode import prompt
from .gen import generate
from .runner import build_suite, run_suite


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
    ap = argparse.ArgumentParser(prog="gridforge")
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
    a = ap.parse_args(argv)

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
