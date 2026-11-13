"""Execution-heavy puzzle families: easy to state, long to apply exactly.

Each family's rule is a lookup table keyed by a local feature of a cell or object.
Fairness check (replaces the chain library's ambiguity filter):

  * the true table must cover every key the test input needs (no unseen cases), and
  * every *other* natural feature table that is consistent with all train pairs and
    covers the test must give the same test output.

So the examples always pin the answer down; what is hard is applying it to every cell.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

from .grid import Grid, blank, dims, make, objects


# ---- features -----------------------------------------------------------------
def _n(g, y, x, offs):
    h, w = dims(g)
    return sum(1 for dy, dx in offs if 0 <= y + dy < h and 0 <= x + dx < w and g[y + dy][x + dx])


N8 = [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy, dx) != (0, 0)]
N4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
ND = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

CELL_FEATURES: Dict[str, Callable] = {
    "alive+n8": lambda g, y, x: (bool(g[y][x]), _n(g, y, x, N8)),
    "alive+n4": lambda g, y, x: (bool(g[y][x]), _n(g, y, x, N4)),
    "alive+diag": lambda g, y, x: (bool(g[y][x]), _n(g, y, x, ND)),
    "alive+n4+diag": lambda g, y, x: (bool(g[y][x]), _n(g, y, x, N4), _n(g, y, x, ND)),
}


def _cells(g):
    h, w = dims(g)
    return [(y, x) for y in range(h) for x in range(w)]


def _cell_table(feat, pairs):
    """Learn key -> output value from train pairs; None if contradictory."""
    t = {}
    for x, y in pairs:
        if dims(x) != dims(y):
            return None
        for r, c in _cells(x):
            k = feat(x, r, c)
            if t.setdefault(k, y[r][c]) != y[r][c]:
                return None
    return t


def _apply_cell_table(feat, table, g) -> Optional[Grid]:
    h, w = dims(g)
    out = blank(h, w)
    for r, c in _cells(g):
        k = feat(g, r, c)
        if k not in table:
            return None
        out[r][c] = table[k]
    return make(out)


OBJ_FEATURES: Dict[str, Callable] = {
    "size": lambda cells: len(cells),
    "height": lambda cells: max(y for y, _ in cells) - min(y for y, _ in cells) + 1,
    "width": lambda cells: max(x for _, x in cells) - min(x for _, x in cells) + 1,
    "bbox_area": lambda cells: ((max(y for y, _ in cells) - min(y for y, _ in cells) + 1)
                                * (max(x for _, x in cells) - min(x for _, x in cells) + 1)),
}


def _obj_table(feat, pairs):
    t = {}
    for x, y in pairs:
        if dims(x) != dims(y):
            return None
        for _, cells in objects(x):
            vals = {y[r][c] for r, c in cells}
            if len(vals) != 1:
                return None
            k = feat(cells)
            if t.setdefault(k, vals.pop()) != y[cells[0][0]][cells[0][1]]:
                return None
    return t


def _apply_obj_table(feat, table, g):
    out = [list(r) for r in g]
    for _, cells in objects(g):
        k = feat(cells)
        if k not in table:
            return None
        for r, c in cells:
            out[r][c] = table[k]
    return make(out)


# ---- rules --------------------------------------------------------------------
@dataclass(frozen=True)
class LocalRule:
    """Duck-types Prim: apply(), describe(), str()."""
    family: str
    params: Tuple

    def apply(self, g: Grid) -> Grid:
        p = dict(self.params)
        if self.family == "life":
            born, stay, c = set(p["born"]), set(p["stay"]), p["c"]
            h, w = dims(g)
            out = blank(h, w)
            for y, x in _cells(g):
                n = _n(g, y, x, N8)
                out[y][x] = c if ((g[y][x] and n in stay) or (not g[y][x] and n in born)) else 0
            return make(out)
        if self.family == "count":
            cmap = dict(p["map"])
            h, w = dims(g)
            out = [list(r) for r in g]
            for y, x in _cells(g):
                if not g[y][x]:
                    out[y][x] = cmap[_n(g, y, x, N4)]
            return make(out)
        if self.family == "sizecolor":
            cmap = dict(p["map"])
            out = [list(r) for r in g]
            for _, cells in objects(g):
                for y, x in cells:
                    out[y][x] = cmap[len(cells)]
            return make(out)
        raise ValueError(self.family)

    def describe(self) -> str:
        p = dict(self.params)
        if self.family == "life":
            return (f"one step of a Life-like automaton: empty cell with {sorted(p['born'])} live "
                    f"neighbours is born, live cell with {sorted(p['stay'])} survives (8 neighbours)")
        if self.family == "count":
            return "each empty cell is coloured by its number of filled side-neighbours: " + \
                ", ".join(f"{k}->{v}" for k, v in sorted(dict(p["map"]).items()))
        return "each shape is recoloured by its cell count: " + \
            ", ".join(f"{k}->{v}" for k, v in sorted(dict(p["map"]).items()))

    def __str__(self):
        return f"{self.family}{self.params}"


def _rand_grid(rng, h, w, density, colour):
    return make([[colour if rng.random() < density else 0 for _ in range(w)] for _ in range(h)])


def _shapes_grid(rng, h, w, colour, sizes):
    from .gen import _blob, _place
    g = blank(h, w)
    for _ in range(rng.randint(h * w // 30, h * w // 18)):
        _place(rng, g, _blob(rng, rng.choice(sizes)), colour, margin=1, tries=30)
    return make(g)


def fair(family: str, train, test_in, test_out) -> bool:
    if family in ("life", "count"):
        feats = CELL_FEATURES
        learn, use = _cell_table, _apply_cell_table
    else:
        feats = OBJ_FEATURES
        learn, use = _obj_table, _apply_obj_table
    true_key = "alive+n8" if family == "life" else ("alive+n4" if family == "count" else "size")
    ok_true = False
    for name, f in feats.items():
        t = learn(f, train)
        if t is None:
            continue
        pred = use(f, t, test_in)
        if pred is None:          # this feature leaves some test case unseen
            if name == true_key:
                return False
            continue
        if pred != test_out:
            return False          # another natural rule fits the examples but disagrees
        if name == true_key:
            ok_true = True
    return ok_true


def generate_hard(seed: int, family: str, size: str = "l", n_train: int = 4, max_tries: int = 3000):
    from .gen import SIZES, Task
    rng = random.Random(seed * 104729 + sum(map(ord, family)) * 13 + sum(map(ord, size)))
    lo, hi = SIZES[size]
    for _ in range(max_tries):
        colour = rng.randint(1, 9)
        if family == "life":
            born = tuple(sorted(rng.sample(range(1, 9), rng.randint(1, 3))))
            stay = tuple(sorted(rng.sample(range(0, 9), rng.randint(2, 4))))
            rule = LocalRule("life", (("born", born), ("stay", stay), ("c", colour)))
            make_in = lambda: _rand_grid(rng, rng.randint(lo, hi), rng.randint(lo, hi),
                                         rng.uniform(0.25, 0.45), colour)
        elif family == "count":
            cols = rng.sample([c for c in range(1, 10) if c != colour], 4)
            rule = LocalRule("count", (("map", ((0, 0),) + tuple((k, cols[k - 1]) for k in range(1, 5))),))
            make_in = lambda: _rand_grid(rng, rng.randint(lo, hi), rng.randint(lo, hi),
                                         rng.uniform(0.3, 0.5), colour)
        else:
            sizes = list(range(1, 7))
            cols = [rng.choice([c for c in range(1, 10) if c != colour]) for _ in sizes]
            rule = LocalRule("sizecolor", (("map", tuple(zip(sizes, cols))),))
            make_in = lambda: _shapes_grid(rng, rng.randint(lo, hi), rng.randint(lo, hi), colour, sizes)
        grids = [make_in() for _ in range(n_train + 1)]
        outs = [rule.apply(g) for g in grids]
        if any(x == y for x, y in zip(grids, outs)) or not any(any(r) for r in outs[-1]):
            continue
        train = list(zip(grids[:-1], outs[:-1]))
        if not fair(family, train, grids[-1], outs[-1]):
            continue
        return Task(id=f"{family}-{size}/{seed}", seed=seed, depth=family, size=size, chain=[rule],
                    train=train, test_in=grids[-1], test_out=outs[-1], effective_depth=0)
    raise RuntimeError(f"no fair {family} task for seed {seed}")
