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
    from .hard import generate_hard
    tasks = []
    for fam in families:
        if fam == "chain":
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
