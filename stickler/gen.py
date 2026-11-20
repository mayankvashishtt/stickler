"""Seeded task generator.

A task = hidden rule (a chain of primitives) + train pairs + one test pair.
Every task passes two checks before it is kept:

1. Non-trivial: each step of the chain changes the grid in the test and in
   at least two train examples.
2. Unambiguous: every rule up to the task's length (at least 2) from the primitive library that
   fits all train pairs must give the same test output as the hidden rule.
   So a solver who finds *any* simple rule matching the examples is graded right.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from .grid import Grid, Invalid, blank, colors, make
from .prims import FINAL_ONLY, FUNCS, GROWS, SCENE, Prim, all_prims, run_chain

SIZES = {"s": (6, 10), "m": (11, 16), "l": (18, 26), "xl": (26, 30)}


@dataclass
class Task:
    id: str
    seed: int
    depth: int
    size: str
    chain: List[Prim]
    train: List[Tuple[Grid, Grid]]
    test_in: Grid
    test_out: Grid
    effective_depth: int = 0       # shortest library rule that explains the train pairs
    n_consistent: int = 0          # how many short rules fit the train pairs (all agree on test)
    steps: int = 1                 # "many steps" layer: apply the rule this many times to the test
    given: Optional[Grid] = None   # "fix the slip" layer: a near-miss answer to correct
    given_wrong: int = 0           # how many squares of `given` are wrong (told to the model)

    def rule(self) -> str:
        r = " -> ".join(p.describe() for p in self.chain)
        return f"{r} (applied {self.steps} times)" if self.steps > 1 else r


# ---- scenes -------------------------------------------------------------------
def _free(g, cells, margin):
    h, w = len(g), len(g[0])
    for y, x in cells:
        if not (0 <= y < h and 0 <= x < w):
            return False
        for dy in range(-margin, margin + 1):
            for dx in range(-margin, margin + 1):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and g[ny][nx]:
                    return False
    return True


def _place(rng, g, shape, color, margin=1, tries=60):
    h, w = len(g), len(g[0])
    sh = max(y for y, _ in shape) + 1
    sw = max(x for _, x in shape) + 1
    if sh > h or sw > w:
        return False
    for _ in range(tries):
        oy, ox = rng.randrange(h - sh + 1), rng.randrange(w - sw + 1)
        cells = [(oy + y, ox + x) for y, x in shape]
        if _free(g, cells, margin):
            for y, x in cells:
                g[y][x] = color
            return True
    return False


def _rect(h, w):
    return [(y, x) for y in range(h) for x in range(w)]


def _hollow(h, w):
    return [(y, x) for y in range(h) for x in range(w) if y in (0, h - 1) or x in (0, w - 1)]


def _blob(rng, n):
    cells = {(0, 0)}
    while len(cells) < n:
        y, x = rng.choice(sorted(cells))
        dy, dx = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        cells.add((y + dy, x + dx))
    my = min(y for y, _ in cells)
    mx = min(x for _, x in cells)
    return sorted((y - my, x - mx) for y, x in cells)


def _shape(rng, lo=2, hi=9):
    kind = rng.random()
    if kind < 0.4:
        return _blob(rng, rng.randint(lo, hi))
    return _rect(rng.randint(1, 3), rng.randint(2, 4)) if kind < 0.75 else _rect(rng.randint(2, 4), rng.randint(1, 3))


def scene(rng, kind: str, h: int, w: int, palette) -> Grid:
    g = blank(h, w)
    cols = list(palette)
    area = h * w
    if kind == "small":
        p = rng.uniform(0.25, 0.55)
        k = rng.sample(cols, rng.randint(1, min(3, len(cols))))
        return make([[rng.choice(k) if rng.random() < p else 0 for _ in range(w)] for _ in range(h)])
    if kind == "dots":
        for _ in range(rng.randint(2, max(3, area // 25))):
            _place(rng, g, [(0, 0)], rng.choice(cols), margin=1)
    elif kind == "pairs":
        for c in rng.sample(cols, rng.randint(2, min(4, len(cols)))):
            for _ in range(20):
                if rng.random() < 0.5:
                    y, x1, x2 = rng.randrange(h), rng.randrange(w), rng.randrange(w)
                    a, b = (y, x1), (y, x2)
                else:
                    x, y1, y2 = rng.randrange(w), rng.randrange(h), rng.randrange(h)
                    a, b = (y1, x), (y2, x)
                if abs(a[0] - b[0]) + abs(a[1] - b[1]) >= 3 and _free(g, [a, b], 1):
                    g[a[0]][a[1]] = g[b[0]][b[1]] = c
                    break
    elif kind == "hollow":
        for _ in range(rng.randint(2, 4)):
            _place(rng, g, _hollow(rng.randint(3, 6), rng.randint(3, 6)), rng.choice(cols))
        for _ in range(rng.randint(0, 2)):
            _place(rng, g, _shape(rng), rng.choice(cols))
    elif kind == "noisy":
        for _ in range(rng.randint(2, 4)):
            _place(rng, g, _shape(rng, 3, 9), rng.choice(cols))
        for _ in range(rng.randint(3, 7)):
            _place(rng, g, [(0, 0)], rng.choice(cols), margin=1)
    elif kind == "sparse":
        for _ in range(rng.randint(2, 4)):
            _place(rng, g, _shape(rng, 1, 5), rng.choice(cols), margin=2)
    else:  # objects / mono
        one = rng.choice(cols) if kind == "mono" else None
        for _ in range(rng.randint(3, 6)):
            _place(rng, g, _shape(rng), one or rng.choice(cols))
    return make(g)


# ---- generation ---------------------------------------------------------------
LIB = all_prims()
# Primitives that paint a new colour: that colour never appears in inputs, so
# "paint colour c" can't be confused with "paint with the odd colour out".
PAINTS = {"color_largest", "color_by_size", "fill_holes", "halo", "boxes", "connect", "count_bar"}
NAMES = sorted(FUNCS)


def _random_prim(rng, final: bool) -> Prim:
    while True:
        name = rng.choice(NAMES)
        if name in FINAL_ONLY and not final:
            continue
        opts = [p for p in LIB if p.name == name]
        return rng.choice(opts)


def _changes(chain, grids) -> bool:
    """Every step must change the grid on >= 2 train inputs and on the test input."""
    for i, prim in enumerate(chain):
        changed_train = 0
        for n, g in enumerate(grids):
            before = run_chain(chain[:i], g)
            after = prim.apply(before)
            if after != before:
                if n < len(grids) - 1:
                    changed_train += 1
            elif n == len(grids) - 1:
                return False
        if changed_train < 2:
            return False
    return True


def consistent_rules(train, palette, max_depth=2):
    """All library rules of length <= max_depth that map every train input to its output."""
    lib = [p for p in all_prims(sorted(palette))]
    x0, y0 = train[0]
    found = []
    level = [((), x0)]
    seen = {x0}
    for depth in range(1, max_depth + 1):
        nxt = []
        for chain, g in level:
            for p in lib:
                try:
                    out = p.apply(g)
                except Invalid:
                    continue
                ch = chain + (p,)
                if out == y0:
                    ok = True
                    for x, y in train[1:]:
                        try:
                            if run_chain(ch, x) != y:
                                ok = False
                                break
                        except Invalid:
                            ok = False
                            break
                    if ok:
                        found.append(ch)
                if depth < max_depth and out not in seen:
                    seen.add(out)
                    nxt.append((ch, out))
        level = nxt
    return found


def generate(seed: int, depth: int = 2, size: str = "m", n_train: int = 4,
             check_ambiguity: bool = True, max_tries: int = 400) -> Task:
    rng = random.Random(seed * 7919 + depth * 31 + sum(map(ord, size)))
    lo, hi = SIZES[size]
    for _ in range(max_tries):
        chain = [_random_prim(rng, final=(i == depth - 1)) for i in range(depth)]
        kind = next((SCENE[p.name] for p in chain if p.name in SCENE), "objects")
        if any(p.name in GROWS for p in chain):
            kind, (a, b) = "small", (3, 6)
        else:
            a, b = lo, hi
        paint = {v for pr in chain if pr.name in PAINTS for k, v in pr.params if k in ("a", "b", "c")}
        free = [c for c in range(1, 10) if c not in paint]
        palette = rng.sample(free, min(len(free), rng.randint(2, 4)))
        grids = []
        for _ in range(n_train + 1):
            grids.append(scene(rng, kind, rng.randint(a, b), rng.randint(a, b), palette))
        try:
            outs = [run_chain(chain, g) for g in grids]
            if not _changes(chain, grids):
                continue
        except Invalid:
            continue
        if any(x == y for x, y in zip(grids, outs)) or len(set(grids)) < len(grids):
            continue
        seen_cols = set().union(*(colors(g) for g in grids[:-1]))
        if not colors(grids[-1]) <= seen_cols:
            continue   # the test may only use colours the examples showed
        train = list(zip(grids[:-1], outs[:-1]))
        task = Task(id=f"d{depth}{size}/{seed}", seed=seed, depth=depth, size=size, chain=chain,
                    train=train, test_in=grids[-1], test_out=outs[-1], effective_depth=depth)
        if check_ambiguity:
            pal = set()
            for x, y in train:
                pal |= colors(x) | colors(y)
            pal |= colors(task.test_in)
            rules = consistent_rules(train, pal, max_depth=max(2, depth))
            bad = False
            for r in rules:
                try:
                    if run_chain(r, task.test_in) != task.test_out:
                        bad = True
                        break
                except Invalid:
                    bad = True
                    break
            if bad:
                continue
            task.n_consistent = len(rules)
            if rules:
                task.effective_depth = min(len(r) for r in rules)
            if task.effective_depth < depth:
                continue   # a shorter rule explains it: not a real depth-`depth` task
        return task
    raise RuntimeError(f"could not generate a task for seed={seed} depth={depth} size={size}")
