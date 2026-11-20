"""Tables level: the same "find the hidden rule, then apply it exactly" test, on tables of numbers.

A table is a tuple of rows of ints; columns are named a, b, c, ... in order. A hidden rule of 1-2
steps (add a computed column, keep a value only past a threshold, running total, change from the
row above, sort, filter rows) turns each example input into its output.

Fair, like the grids: every rule of the same length from the library below that fits all examples
must give the same test answer. Thresholds are checked over every whole number, not just round ones
(only the gaps between values seen matter, so the check is exact).
"""
from __future__ import annotations

import json
import os
import random
import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

Table = Tuple[Tuple[int, ...], ...]
NAMES = "abcdefgh"
SIZES = {"m": dict(rows=(8, 12), lo=0, hi=99, train=4), "l": dict(rows=(24, 32), lo=10, hi=999, train=3),
         "xl": dict(rows=(40, 50), lo=100, hi=9999, train=3)}
CATS = 5  # column a holds a category 1-5 (so "group" rules have groups); other columns are numbers
FUNCS = {"+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y,
         "max": max, "min": min}


class Invalid(Exception):
    pass


# ---- operations -----------------------------------------------------------------
@dataclass(frozen=True)
class Op:
    kind: str
    p: tuple

    def apply(self, t: Table) -> Table:
        k, p = self.kind, self.p
        if not t:
            raise Invalid("empty")
        w = len(t[0])
        if any(i >= w for i in self.cols()):
            raise Invalid("no such column")
        if k == "fn":
            f, i, j = p
            return tuple(r + (FUNCS[f](r[i], r[j]),) for r in t)
        if k == "keep":       # new column = column j where column i >= n, else 0
            i, n, j = p
            return tuple(r + ((r[j] if r[i] >= n else 0),) for r in t)
        if k == "cum":
            out, s = [], 0
            for r in t:
                s += r[p[0]]
                out.append(r + (s,))
            return tuple(out)
        if k == "diff":
            i = p[0]
            return tuple(r + ((r[i] - t[n - 1][i]) if n else 0,) for n, r in enumerate(t))
        if k == "rank":       # 1 = largest value of column i
            i = p[0]
            col = [r[i] for r in t]
            if len(set(col)) != len(col):
                raise Invalid("ties")
            order = sorted(col, reverse=True)
            return tuple(r + (order.index(r[i]) + 1,) for r in t)
        if k == "above":      # how many rows above this one have a bigger value in column i
            i = p[0]
            return tuple(r + (sum(q[i] > r[i] for q in t[:n]),) for n, r in enumerate(t))
        if k == "win3":       # this row plus the two rows above, column i
            i = p[0]
            return tuple(r + (sum(q[i] for q in t[max(0, n - 2):n + 1]),) for n, r in enumerate(t))
        if k == "group":      # total of column i over every row with the same value in column j
            i, j = p
            tot = {}
            for r in t:
                tot[r[j]] = tot.get(r[j], 0) + r[i]
            if len(tot) == len(t):
                raise Invalid("no groups")
            return tuple(r + (tot[r[j]],) for r in t)
        if k == "sort":
            i, desc = p
            col = [r[i] for r in t]
            if len(set(col)) != len(col):
                raise Invalid("ties")  # tie order would be a guess, so never used
            return tuple(sorted(t, key=lambda r: r[i], reverse=desc))
        if k == "filter":
            i, n, ge = p
            out = tuple(r for r in t if (r[i] >= n) == ge)
            if not out:
                raise Invalid("empty")
            return out
        raise ValueError(k)

    def cols(self):
        k, p = self.kind, self.p
        if k == "fn":
            return p[1:]
        if k == "keep":
            return (p[0], p[2])
        if k == "group":
            return p
        return p[:1]

    def describe(self, w: int) -> str:
        k, p, nm, new = self.kind, self.p, NAMES, NAMES[w] if w < len(NAMES) else "?"
        if k == "fn":
            f, i, j = p
            e = f"{nm[i]} {f} {nm[j]}" if f in "+-*" else f"{f}({nm[i]}, {nm[j]})"
            return f"new column {new} = {e}"
        if k == "keep":
            return f"new column {new} = {nm[p[2]]} if {nm[p[0]]} >= {p[1]}, else 0"
        if k == "cum":
            return f"new column {new} = running total of {nm[p[0]]}"
        if k == "diff":
            return f"new column {new} = {nm[p[0]]} minus {nm[p[0]]} in the row above (0 on the first row)"
        if k == "rank":
            return f"new column {new} = rank of {nm[p[0]]} (1 = largest)"
        if k == "above":
            return f"new column {new} = how many rows above have a bigger {nm[p[0]]}"
        if k == "win3":
            return f"new column {new} = {nm[p[0]]} of this row plus the two rows above"
        if k == "group":
            return f"new column {new} = total of {nm[p[0]]} over all rows with the same {nm[p[1]]}"
        if k == "sort":
            return f"sort rows by {nm[p[0]]}, {'largest' if p[1] else 'smallest'} first"
        return f"keep only rows where {nm[p[0]]} {'>=' if p[2] else '<'} {p[1]}"

    def adds_col(self):
        return self.kind in ("fn", "keep", "cum", "diff", "rank", "above", "win3", "group")


def run(chain, t):
    for op in chain:
        t = op.apply(t)
    return t


def _thresholds(tables, i):
    """Every threshold that behaves differently on these tables (exact over all integers)."""
    vals = sorted({r[i] for t in tables for r in t if i < len(r)})
    return vals + [vals[-1] + 1] if vals else []


def library(tables, w):
    """All one-step rules on tables of width w. Thresholds come from the values in `tables`."""
    ops = []
    for f in FUNCS:
        for i in range(w):
            for j in range(w):
                if i == j or (f != "-" and j < i):  # + * max min are symmetric
                    continue
                ops.append(Op("fn", (f, i, j)))
    for i in range(w):
        ops += [Op("cum", (i,)), Op("diff", (i,)), Op("sort", (i, True)), Op("sort", (i, False)),
                Op("rank", (i,)), Op("above", (i,)), Op("win3", (i,))]
        ops += [Op("group", (i, j)) for j in range(w) if j != i]
        for n in _thresholds(tables, i):
            ops += [Op("filter", (i, n, True)), Op("filter", (i, n, False))]
            ops += [Op("keep", (i, n, j)) for j in range(w)]
    return ops


def _fits(chain, train):
    try:
        return all(run(chain, x) == y for x, y in train)
    except Invalid:
        return False


def fair(train, test_in, test_out):
    """(ok, n_rules_fit). ok = every library rule of length <= 2 that fits gives test_out."""
    w = len(train[0][0])
    every = [x for x, _ in train] + [test_in]
    n = 0
    for op1 in library(every, w):
        try:
            mids = [op1.apply(x) for x, _ in train]
            mid_test = op1.apply(test_in)
        except Invalid:
            continue
        if all(m == y for m, (_, y) in zip(mids, train)):
            n += 1
            if mid_test != test_out:
                return False, n
        # a second step must turn every mid into its output; check the cheap shape test first
        if not all(len(m[0]) + 1 >= len(y[0]) >= len(m[0]) and len(y) <= len(m) for m, (_, y) in zip(mids, train)):
            continue
        w2 = len(mids[0][0])
        for op2 in library(mids + [mid_test], w2):
            try:
                if op2.apply(mids[0]) != train[0][1]:
                    continue
                if not all(op2.apply(m) == y for m, (_, y) in zip(mids[1:], train[1:])):
                    continue
                got = op2.apply(mid_test)
            except Invalid:
                continue
            n += 1
            if got != test_out:
                return False, n
    return True, n


# ---- generator --------------------------------------------------------------------
@dataclass
class TableTask:
    id: str
    seed: int
    depth: int
    size: str
    chain: List[Op]
    train: List[Tuple[Table, Table]]
    test_in: Table
    test_out: Table
    n_consistent: int = 0
    kind: str = "table"
    steps: int = 1
    given: Optional[Table] = None
    given_wrong: int = 0

    def rule(self) -> str:
        w, out = len(self.test_in[0]), []
        for op in self.chain:
            out.append(op.describe(w))
            w += op.adds_col()
        return " -> ".join(out)

    def solve(self, t):
        return run(self.chain, t)


def _table(rng, cfg, w=4, cats=False):
    rows = rng.randint(*cfg["rows"])
    return tuple(((rng.randint(1, CATS),) if cats else (rng.randint(cfg["lo"], cfg["hi"]),)) +
                 tuple(rng.randint(cfg["lo"], cfg["hi"]) for _ in range(w - 1)) for _ in range(rows))


HARD = ["rank", "above", "win3", "group"]


def _random_op(rng, sample, w, hard=False):
    kind = rng.choice(HARD) if hard else rng.choice(["fn", "fn", "keep", "cum", "diff", "sort", "filter"])
    if kind == "group":
        return Op("group", (rng.randrange(1, w), 0))
    if kind in ("rank", "above", "win3"):
        return Op(kind, (rng.randrange(1, w),))
    i = rng.randrange(w)
    col = sorted(r[i] for r in sample)
    if kind == "fn":
        j = rng.choice([x for x in range(w) if x != i])
        return Op("fn", (rng.choice(list(FUNCS)), i, j))
    if kind in ("keep", "filter"):
        n = col[len(col) // 2]
        n = max(1, round(n, -1) if n >= 20 else n)  # a round-ish cut near the middle
        if kind == "keep":
            return Op("keep", (i, n, rng.choice([x for x in range(w) if x != i])))
        return Op("filter", (i, n, rng.random() < 0.5))
    if kind == "sort":
        return Op("sort", (i, rng.random() < 0.5))
    return Op(kind, (i,))


def _does_work(op, before, after):
    """Each step must visibly matter: filters drop some rows but keep half; keep has both branches."""
    if op.kind == "filter":
        return len(before) // 2 <= len(after) < len(before)
    if op.kind == "sort":
        return before != after
    if op.kind == "keep":
        col = [r[-1] for r in after]
        return 2 <= sum(v == 0 for v in col) <= len(col) - 2
    return True


def generate_table(seed: int, size: str = "m", depth: int = 1, tries: int = 400, hard: bool = False) -> Optional[TableTask]:
    """hard=True: column a is a category and the first step is a whole-column rule
    (rank, rows-above count, 3-row window, group total), so every answer depends on many rows."""
    cfg = SIZES[size]
    for a in range(tries):
        rng = random.Random(seed * 7919 + a)
        tables = [_table(rng, cfg, cats=hard) for _ in range(cfg["train"] + 1)]
        chain, ok, w = [], True, 4
        cur = tables
        for step in range(depth):
            op = _random_op(rng, cur[0], w, hard=hard and step == 0)
            try:
                nxt = [op.apply(t) for t in cur]
            except Invalid:
                ok = False
                break
            if not all(_does_work(op, b, c) for b, c in zip(cur, nxt)):
                ok = False
                break
            chain.append(op)
            cur, w = nxt, w + op.adds_col()
        if not ok or len({o.kind for o in chain}) < len(chain):
            continue
        train = list(zip(tables[:-1], cur[:-1]))
        test_in, test_out = tables[-1], cur[-1]
        good, n = fair(train, test_in, test_out)
        if good:
            return TableTask(f"table{'h' if hard else ''}{depth}-{size}/{seed}", seed, depth, size, chain, train, test_in, test_out, n)
    return None


# ---- prompt, parsing, grading -------------------------------------------------------
INSTRUCTIONS = """You are solving a table puzzle. Each table has a header row of column names, then rows
of whole numbers. Every example input table is turned into its output table by the same hidden rule.
The rule may add new columns, sort the rows, or keep only some rows. Work out the rule, then apply it to
the test input.

You cannot run code. Reason it out.

End your reply with the output table in a fenced block labelled `table`: the header row first, then
one row per line, values separated by spaces, for example:

```table
a b c
3 4 7
1 5 6
```"""


def to_text(t: Table) -> str:
    w = len(t[0]) if t else 0
    cells = [list(NAMES[:w])] + [[str(v) for v in r] for r in t]
    width = [max(len(row[c]) for row in cells) for c in range(w)]
    return "\n".join(" ".join(v.rjust(width[c]) for c, v in enumerate(row)) for row in cells)


def prompt(task: TableTask) -> str:
    parts = [INSTRUCTIONS, ""]
    for i, (x, y) in enumerate(task.train, 1):
        parts += [f"## Example {i}", f"Input ({len(x)} rows):", "```", to_text(x), "```",
                  f"Output ({len(y)} rows):", "```", to_text(y), "```", ""]
    parts += ["## Test", f"Input ({len(task.test_in)} rows):", "```", to_text(task.test_in), "```", "",
              "What is the output table?"]
    return "\n".join(parts)


def parse_answer(reply: str):
    blocks = re.findall(r"```table\s*\n(.*?)```", reply, re.S) or re.findall(r"```[a-z]*\s*\n(.*?)```", reply, re.S)
    if not blocks:
        return None, "no table block found"
    rows = []
    for line in blocks[-1].strip().splitlines():
        cells = line.replace(",", " ").replace("|", " ").split()
        if not cells:
            continue
        if all(re.fullmatch(r"-?\d+", c) for c in cells):
            rows.append(tuple(int(c) for c in cells))
        elif rows:
            return None, f"not a table row: {line.strip()!r}"
    if not rows or any(len(r) != len(rows[0]) for r in rows):
        return None, "rows have different lengths"
    return tuple(rows), None


def grade(task: TableTask, reply: str) -> dict:
    t, err = parse_answer(reply)
    if t is None:
        return {"solved": False, "cell_acc": 0.0, "error": err, "pred": None}
    gold = task.test_out
    same_shape = len(t) == len(gold) and len(t[0]) == len(gold[0])
    acc = sum(a == b for r, g in zip(t, gold) for a, b in zip(r, g)) / (len(gold) * len(gold[0])) if same_shape else 0.0
    return {"solved": t == gold, "cell_acc": round(acc, 4), "pred": t,
            "error": None if same_shape else f"wrong size {len(t)}x{len(t[0])} vs {len(gold)}x{len(gold[0])}"}


def _to_json(t: TableTask):
    return {"id": t.id, "seed": t.seed, "depth": t.depth, "size": t.size, "n": t.n_consistent,
            "chain": [[o.kind, list(o.p)] for o in t.chain], "train": t.train, "test_in": t.test_in}


def _from_json(d):
    tt = lambda t: tuple(tuple(r) for r in t)
    chain = [Op(k, tuple(p)) for k, p in d["chain"]]
    test_in = tt(d["test_in"])
    return TableTask(d["id"], d["seed"], d["depth"], d["size"], chain,
                     [(tt(x), tt(y)) for x, y in d["train"]], test_in, run(chain, test_in), d["n"])


CACHE = os.path.join(os.path.dirname(__file__), "..", "data", "tables-24.json")


SPECS = ([(s, "m", 1 + s % 2, False) for s in range(0, 8)] + [(s, "l", 1 + s % 2, False) for s in range(100, 108)]
         + [(s, "xl", 1 + s % 2, True) for s in range(300, 308)])


def _gen(spec):
    s, size, depth, hard = spec
    return generate_table(s, size, depth, hard=hard)


def tables_suite():
    """The fixed Tables set (24): 8 medium, 8 large, 8 extra-large with whole-column rules
    (rank, rows-above count, 3-row window, group total). Half one-step, half two-step rules.
    Built once in parallel (the fairness check is slow on big tables), then read from data/tables-24.json."""
    if os.path.exists(CACHE):
        return [_from_json(d) for d in json.load(open(CACHE))]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor() as ex:
        out = [t for t in ex.map(_gen, SPECS) if t]
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump([_to_json(t) for t in out], open(CACHE, "w"), separators=(",", ":"))
    return out
