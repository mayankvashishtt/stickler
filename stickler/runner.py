"""Run agents over generated tasks; write results.jsonl and report.md."""
from __future__ import annotations

import json
import os
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from .agents import make_agent
from .episode import GridEnv
from .gen import generate


def build_suite(seeds, depths, sizes, n_train=4, families=("chain",)):
    from .families import FAMILIES, generate_family
    from .hard import generate_hard
    tasks = []
    for fam in families:
        if fam in FAMILIES:
            tasks += [generate_family(s, fam, z) for z in sizes for s in seeds]
        elif fam == "chain":
            tasks += [generate(s, d, z, n_train=n_train) for d in depths for z in sizes for s in seeds]
        else:
            tasks += [generate_hard(s, fam, z, n_train=n_train) for z in sizes for s in seeds]
    return tasks


# The fixed 74-puzzle set every model on the leaderboard was run on.
BENCH = [  # (seeds, depths, sizes, families)
    (range(10, 18), (2, 3), ("m", "l"), ("chain",)),
    (range(0, 4), (2,), ("m", "l"), ("life", "count", "sizecolor")),
    (range(4, 14), (2,), ("l", "xl"), ("life",)),
]
# Found ambiguous on review (another simple rule also fits the examples): dropped for every model.
EXCLUDE = {"d2l/17", "d2m/13"}


def bench_suite():
    tasks = []
    for seeds, depths, sizes, fams in BENCH:
        tasks += build_suite(list(seeds), list(depths), list(sizes), 4, fams)
    return [t for t in tasks if t.id not in EXCLUDE]


def steps_suite(k=3):
    """Layer 1, many steps: 8 medium + 4 large Life puzzles, rule applied k times."""
    from .hard import generate_steps
    return [generate_steps(s, z, k) for z, seeds in (("m", range(0, 8)), ("l", range(8, 12))) for s in seeds]


def task_by_id(pid):
    from .hard import generate_hard
    head, seed = pid.split("/")
    fam, size = head.rsplit("-", 1) if "-" in head else ("chain", head[2:])
    if fam == "chain":
        return generate(int(seed), int(head[1]), size)
    from .families import FAMILIES, generate_family
    if fam in FAMILIES:
        return generate_family(int(seed), fam, size)
    return generate_hard(int(seed), fam, size)


# Layer 2, fix the slip: real leaderboard answers with 1-6 wrong squares (one per puzzle).
FIX = [("life-m/2", "Opus 5.5"), ("d2m/10", "Sonnet 5.5"), ("count-m/2", "Sonnet 5.5"),
       ("d3m/17", "Fable 5.2"), ("count-m/1", "Haiku 5.5"), ("life-l/13", "Opus 5.5"),
       ("life-l/2", "Haiku 5.5"), ("life-l/3", "Opus 5.5"), ("life-xl/4", "Sonnet 5.5"),
       ("d3m/15", "Fable 5.2"), ("life-l/0", "Opus 5.5"), ("life-l/12", "Sonnet 5.5"),
       ("life-l/4", "Fable 5.2"), ("life-xl/13", "Haiku 5.5"), ("count-l/1", "Haiku 5.5"),
       ("life-l/9", "Opus 5.5"), ("life-m/1", "Opus 5.5"), ("count-m/3", "Sonnet 5.5"),
       ("d3m/10", "Haiku 5.5"), ("sizecolor-m/2", "Fable 5.2"), ("d3l/11", "Sonnet 5.5"),
       ("life-xl/8", "Fable 5.2")]
FIX_RUNS = {"Fable 5.2": "fable", "Opus 5.5": "claude", "Sonnet 5.5": "sonnet", "Haiku 5.5": "haiku"}


def fix_suite():
    """Each task: the original puzzle plus a real near-miss answer and how many squares are wrong."""
    import glob
    here = os.path.join(os.path.dirname(__file__), "..", "results")
    preds = {}
    for name, tag in FIX_RUNS.items():
        for f in glob.glob(os.path.join(here, f"{tag}-*", "results.jsonl")):
            if f.split(os.sep)[-2].endswith("pilot"):
                continue
            for line in open(f):
                r = json.loads(line)
                preds[(r["id"], name)] = r.get("pred")
    tasks = []
    for pid, who in FIX:
        t, g = task_by_id(pid), preds[(pid, who)]
        t.given = [list(r) for r in g]
        t.given_wrong = sum(a != b for ra, rb in zip(g, t.test_out) for a, b in zip(ra, rb))
        assert 1 <= t.given_wrong <= 6, (pid, t.given_wrong)
        t.id = f"fix-{pid}"
        tasks.append(t)
    return tasks


def marathon_suite(k=6, size="l"):
    """Layer 3, marathon: 10 large (18-26 square) Life grids, rule applied k times.

    Every step must keep at least 25% of squares lit and change at least 15%, so the
    work never thins out into an empty grid. (8 steps on 30x30 grids was tried first:
    answers ran past API limits, so most runs ended with no answer at all.)
    """
    from .hard import generate_steps
    return [generate_steps(s, size, k, busy=0.25) for s in range(40, 50)]


def trap_suite(n=12):
    """Layer 4, trap: medium Life puzzles whose rule is one number off Conway's famous one."""
    from .hard import generate_trap
    return [generate_trap(s, "m") for s in range(n)]


def tables_suite():
    """Tables level: the same test on tables of numbers (see stickler/tables.py)."""
    from .tables import tables_suite as build
    return build()


def hardboard_suite():
    """Hard board: Life-like rules on a hidden neighbourhood (4 sides, diagonals, knight moves,
    or 2 squares along a row or column). The model must work out WHICH squares count, then
    apply it exactly. 12 large (18-26) + 12 extra-large (26-30) grids."""
    from .hard import generate_hard
    return [generate_hard(s, "hood", z) for z in ("l", "xl") for s in range(12)]


def breadth_suite():
    """Pilot of the new families (gravity, mirror, rays, tiling, border): 4 medium + 4 large each."""
    from .families import FAMILIES, generate_family
    return [generate_family(s, f, z) for f in FAMILIES for z in ("m", "l") for s in range(4)]


SUITES = {"breadth": breadth_suite, "hardboard": hardboard_suite, "steps": steps_suite, "fix": fix_suite, "marathon": marathon_suite, "trap": trap_suite,
          "tables": tables_suite}


def run_one(agent_name, model, task, turns):
    agent = make_agent(agent_name, model)
    agent.reset(task)
    env = GridEnv(task, max_turns=turns)
    obs = env.reset()
    prompts, replies, rewards, t0 = [obs], [], [], time.time()
    done = False
    while not done:
        reply = agent.act(obs)
        replies.append(reply)
        obs, r, done, info = env.step(reply)
        rewards.append(r)
        if not done:
            prompts.append(obs)
    last = env.history[-1]
    return {"id": task.id, "agent": agent.name, "seed": task.seed, "depth": task.depth,
            "size": task.size, "rule": task.rule(), "chain": [str(p) for p in task.chain],
            "solved": last["solved"], "pass_at_1": env.history[0]["solved"],
            "cell_acc": last["cell_acc"], "error": last["error"], "rewards": rewards,
            "turns": len(rewards), "seconds": round(time.time() - t0, 1),
            "test_in": task.test_in, "expected": task.test_out, "pred": last["pred"],
            "train": task.train, "prompts": prompts, "replies": replies,
            "usage": getattr(agent, "usage", None) or None}


def run_suite(agent_name, tasks, turns=1, model=None, workers=1, out_dir=None):
    recs = []
    f = None
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        f = open(os.path.join(out_dir, "results.jsonl"), "w")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(run_one, agent_name, model, t, turns): t for t in tasks}
        for n, fut in enumerate(as_completed(futs), 1):
            t = futs[fut]
            try:
                rec = fut.result()
            except Exception as e:
                rec = {"id": t.id, "agent": agent_name, "seed": t.seed, "depth": t.depth,
                       "size": t.size, "rule": t.rule(), "solved": False, "pass_at_1": False,
                       "cell_acc": 0.0, "crash": repr(e)[:300]}
            recs.append(rec)
            if f:
                f.write(json.dumps(rec) + "\n")
                f.flush()
            mark = "OK " if rec["solved"] else ("ERR" if "crash" in rec else "x  ")
            print(f"[{n}/{len(tasks)}] {mark} {rec['id']:<12} acc={rec['cell_acc']:.2f}  {rec['rule']}",
                  flush=True)
    if out_dir:
        with open(os.path.join(out_dir, "report.md"), "w") as r:
            r.write(report(recs))
    return recs


def report(recs):
    def table(key, title):
        groups = defaultdict(list)
        for r in recs:
            groups[r[key]].append(r)
        lines = [f"### By {title}", "", f"| {title} | n | solved | pass@1 | mean cell acc |",
                 "| --- | --- | --- | --- | --- |"]
        for k in sorted(groups, key=str):
            g = groups[k]
            lines.append(f"| {k} | {len(g)} | {sum(x['solved'] for x in g) / len(g):.0%} | "
                         f"{sum(x['pass_at_1'] for x in g) / len(g):.0%} | "
                         f"{sum(x['cell_acc'] for x in g) / len(g):.2f} |")
        return "\n".join(lines) + "\n"

    agent = recs[0]["agent"] if recs else "?"
    solved = sum(r["solved"] for r in recs)
    out = [f"# Stickler report: {agent}", "",
           f"Solved {solved}/{len(recs)} ({solved / max(1, len(recs)):.0%}).", "",
           table("depth", "depth"), table("size", "size"), "### Every task", "",
           "| id | solved | cell acc | rule |", "| --- | --- | --- | --- |"]
    for r in sorted(recs, key=lambda r: r["id"]):
        out.append(f"| {r['id']} | {'yes' if r['solved'] else 'no'} | {r['cell_acc']:.2f} | {r['rule']} |")
    crashes = [r for r in recs if "crash" in r]
    if crashes:
        out += ["", "### Crashes", ""] + [f"- {r['id']}: {r['crash']}" for r in crashes]
    return "\n".join(out) + "\n"
