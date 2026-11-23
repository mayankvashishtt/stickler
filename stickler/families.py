"""More puzzle families, so the benchmark is not mostly Game of Life.

    gravity   coloured squares fall in one direction; one colour may stay put (walls)
    mirror    a symmetric picture with patches covered up: paint the covered squares back
    rays      single squares shoot a line to the edge; the direction depends on the colour
    tiling    a repeating pattern with holes: fill the holes
    border    shapes touching the edge get one colour, the rest another

Fairness, the same idea as everywhere else in Stickler: each family lists every rule of its
kind (every direction, every symmetry, every period, every colour map, ...). Every listed rule
that fits all the examples must give the same answer on the test. So the examples always pin
the answer down, and the model's job is to find the rule and apply it exactly.
"""
from __future__ import annotations

import itertools
import random
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple

from .grid import Grid, blank, dims, make, objects

DIRS8 = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1),
         "up-left": (-1, -1), "up-right": (-1, 1), "down-left": (1, -1), "down-right": (1, 1)}
DIRS4 = ("down", "up", "left", "right")


@dataclass(frozen=True)
class Rule:
    """Duck-types Prim: apply(), describe(), str()."""
    family: str
    params: Tuple
    text: str
    fn: Callable = None

    def apply(self, g: Grid) -> Optional[Grid]:
        return self.fn(g)

    def describe(self) -> str:
        return self.text

    def __str__(self):
        return f"{self.family}{self.params}"


# ---- gravity -------------------------------------------------------------------
def _gravity(g, d, fixed):
    h, w = dims(g)
    out = blank(h, w)
    dy, dx = DIRS8[d]
    lines = ([[(y, x) for y in range(h)] for x in range(w)] if dx == 0
             else [[(y, x) for x in range(w)] for y in range(h)])
    for line in lines:
        if dy > 0 or dx > 0:
            line = line[::-1]                          # walk from the side things fall towards
        seg = []
        for cell in line + [None]:
            if cell is None or g[cell[0]][cell[1]] == fixed:
                # close the segment: pack its moving squares at its start, keep their order
                movers = [g[a][b] for a, b in seg if g[a][b]]
                for i, (a, b) in enumerate(seg):
                    out[a][b] = movers[i] if i < len(movers) else 0
                seg = []
                if cell is not None:
                    out[cell[0]][cell[1]] = fixed
            else:
                seg.append(cell)
    return make(out)


def gravity_rule(d, fixed):
    wall = f"; colour {fixed} stays where it is and blocks the others" if fixed else ""
    return Rule("gravity", (d, fixed), f"every coloured square falls {d} as far as it can{wall}",
                lambda g: _gravity(g, d, fixed))


def gravity_candidates(train):
    cols = {v for a, _ in train for r in a for v in r if v} | {None}
    return [gravity_rule(d, f) for d in DIRS4 for f in cols]


def gravity_make(rng, h, w):
    cols = rng.sample(range(1, 10), rng.randint(2, 3))
    fixed = rng.choice([None, None] + [c for c in range(1, 10) if c not in cols])
    rule = gravity_rule(rng.choice(DIRS4), fixed)

    def grid():
        g = blank(h, w)
        for y in range(h):
            for x in range(w):
                r = rng.random()
                if fixed and r < 0.07:
                    g[y][x] = fixed
                elif r < 0.25:
                    g[y][x] = rng.choice(cols)
        return make(g)
    return rule, grid


# ---- mirror --------------------------------------------------------------------
def _orbits(h, w, kind):
    """The squares a given square must match under each symmetry."""
    maps = {"left-right": [lambda y, x: (y, w - 1 - x)],
            "top-bottom": [lambda y, x: (h - 1 - y, x)],
            "half-turn": [lambda y, x: (h - 1 - y, w - 1 - x)],
            "both mirrors": [lambda y, x: (y, w - 1 - x), lambda y, x: (h - 1 - y, x),
                             lambda y, x: (h - 1 - y, w - 1 - x)],
            "diagonal": [lambda y, x: (x, y)],
            "quarter-turn": [lambda y, x: (x, h - 1 - y), lambda y, x: (h - 1 - y, w - 1 - x),
                             lambda y, x: (w - 1 - x, y)]}[kind]
    return maps


def _mirror(g, kind, mask):
    h, w = dims(g)
    if kind in ("diagonal", "quarter-turn") and h != w:
        return None
    out = [list(r) for r in g]
    for y in range(h):
        for x in range(w):
            if g[y][x] != mask:
                continue
            vals = {g[a][b] for f in _orbits(h, w, kind) for a, b in [f(y, x)] if g[a][b] != mask}
            if len(vals) != 1:
                return None                            # nothing visible to copy from, or a clash
            out[y][x] = vals.pop()
    return make(out)


MIRRORS = ("left-right", "top-bottom", "half-turn", "both mirrors", "diagonal", "quarter-turn")


def mirror_rule(kind, mask):
    return Rule("mirror", (kind, mask), f"the picture is symmetric ({kind}); repaint every square of colour "
                f"{mask} from its mirror image", lambda g: _mirror(g, kind, mask))


def mirror_candidates(train):
    masks = {v for a, b in train for ra, rb in zip(a, b) for v, u in zip(ra, rb) if v != u}
    return [mirror_rule(k, m) for k in MIRRORS for m in masks]


def mirror_make(rng, h, w):
    kind = rng.choice(MIRRORS)
    if kind in ("diagonal", "quarter-turn"):
        w = h
    mask = rng.randint(1, 9)
    cols = rng.sample([c for c in range(0, 10) if c != mask], rng.randint(3, 5))
    rule = mirror_rule(kind, mask)

    def grid():
        g = [[None] * w for _ in range(h)]
        for y in range(h):
            for x in range(w):
                if g[y][x] is None:
                    v = rng.choice(cols)
                    g[y][x] = v
                    for f in _orbits(h, w, kind):
                        a, b = f(y, x)
                        g[a][b] = v
        full = make(g)
        for _ in range(rng.randint(2, 4)):             # cover up a few patches
            ph, pw = rng.randint(2, max(2, h // 4)), rng.randint(2, max(2, w // 4))
            y0, x0 = rng.randint(0, h - ph), rng.randint(0, w - pw)
            for y in range(y0, y0 + ph):
                for x in range(x0, x0 + pw):
                    g[y][x] = mask
        return [make(g), full]                         # list, not tuple: a Grid is a tuple
    return rule, grid


# ---- rays ----------------------------------------------------------------------
def _rays(g, dmap):
    h, w = dims(g)
    out = [list(r) for r in g]
    for y in range(h):
        for x in range(w):
            c = g[y][x]
            if c and c in dmap:
                dy, dx = DIRS8[dmap[c]]
                a, b = y + dy, x + dx
                while 0 <= a < h and 0 <= b < w and g[a][b] == 0:
                    if out[a][b] not in (0, c):
                        return None                    # two rays cross: not a clean task
                    out[a][b] = c
                    a, b = a + dy, b + dx
    return make(out)


def rays_rule(dmap):
    txt = ", ".join(f"{c} shoots {d}" for c, d in sorted(dmap))
    return Rule("rays", tuple(sorted(dmap)), f"each single square draws a line to the edge, stopping at "
                f"anything in the way: {txt}", lambda g: _rays(g, dict(dmap)))


def rays_candidates(train):
    cols = sorted({v for a, _ in train for r in a for v in r if v})
    movers = [c for c in cols if any(v == c for a, b in train for ra, rb in zip(a, b)
                                     for v, u in zip(rb, ra) if v != u)]
    still = [c for c in cols if c not in movers]
    out = []
    for dirs in itertools.product(DIRS8, repeat=len(movers)):
        out.append(rays_rule(tuple(zip(movers, dirs))))
    # a colour that never moved in the examples might still move on the test: list that too
    for c in still:
        for d in DIRS8:
            for base in out[:]:
                out.append(rays_rule(tuple(sorted(base.params + ((c, d),)))))
    return out


def rays_make(rng, h, w):
    cols = rng.sample(range(1, 10), rng.randint(2, 3))
    block = rng.choice([c for c in range(1, 10) if c not in cols])
    dmap = tuple(sorted((c, rng.choice(list(DIRS8))) for c in cols))
    rule = rays_rule(dmap)

    def grid():
        g = blank(h, w)
        for y in range(h):
            for x in range(w):
                if rng.random() < 0.06:
                    g[y][x] = block
        for _ in range(rng.randint(3, 6)):
            y, x = rng.randrange(h), rng.randrange(w)
            g[y][x] = rng.choice(cols)
        return make(g)
    return rule, grid


# ---- tiling --------------------------------------------------------------------
def _tile(g, py, px):
    h, w = dims(g)
    seen = {}
    for y in range(h):
        for x in range(w):
            if g[y][x]:
                if seen.setdefault((y % py, x % px), g[y][x]) != g[y][x]:
                    return None
    out = [list(r) for r in g]
    for y in range(h):
        for x in range(w):
            if not g[y][x]:
                if (y % py, x % px) not in seen:
                    return None
                out[y][x] = seen[(y % py, x % px)]
    return make(out)


def tiling_rule(py, px):
    return Rule("tiling", (py, px), f"the picture repeats every {py} rows and {px} columns; fill the empty "
                "squares", lambda g: _tile(g, py, px))


def tiling_candidates(train):
    return [tiling_rule(a, b) for a in range(1, 9) for b in range(1, 9)]


def tiling_make(rng, h, w):
    py, px = rng.randint(2, 5), rng.randint(2, 5)
    rule = tiling_rule(py, px)

    def grid():
        tile = [[rng.randint(1, 9) for _ in range(px)] for _ in range(py)]
        g = [[tile[y % py][x % px] for x in range(w)] for y in range(h)]
        for _ in range(rng.randint(2, 4)):
            ph, pw = rng.randint(2, max(2, h // 3)), rng.randint(2, max(2, w // 3))
            y0, x0 = rng.randint(0, h - ph), rng.randint(0, w - pw)
            for y in range(y0, y0 + ph):
                for x in range(x0, x0 + pw):
                    g[y][x] = 0
        return make(g)
    return rule, grid


# ---- border --------------------------------------------------------------------
def _touch(cells, h, w):
    return any(y in (0, h - 1) or x in (0, w - 1) for y, x in cells)


FEATS = {"touches the edge": lambda cells, h, w: _touch(cells, h, w),
         "size": lambda cells, h, w: len(cells),
         "height": lambda cells, h, w: max(y for y, _ in cells) - min(y for y, _ in cells) + 1,
         "width": lambda cells, h, w: max(x for _, x in cells) - min(x for _, x in cells) + 1}


def _by_feature(g, feat, table):
    h, w = dims(g)
    out = [list(r) for r in g]
    for _, cells in objects(g):
        k = FEATS[feat](cells, h, w)
        if k not in table:
            return None
        for y, x in cells:
            out[y][x] = table[k]
    return make(out)


def border_rule(table, feat="touches the edge"):
    txt = ", ".join(f"{k} -> {v}" for k, v in sorted(table, key=str))
    return Rule("border", (feat, table), f"recolour each shape by '{feat}': {txt}",
                lambda g: _by_feature(g, feat, dict(table)))


def border_candidates(train):
    out = []
    for feat in FEATS:
        t, ok = {}, True
        for a, b in train:
            h, w = dims(a)
            for _, cells in objects(a):
                vals = {b[y][x] for y, x in cells}
                k = FEATS[feat](cells, h, w)
                if len(vals) != 1 or t.setdefault(k, vals.pop()) != b[cells[0][0]][cells[0][1]]:
                    ok = False
        if ok:
            out.append(border_rule(tuple(t.items()), feat))
    return out


def border_make(rng, h, w):
    from .gen import _blob, _place
    colour = rng.randint(1, 9)
    a, b = rng.sample([c for c in range(1, 10) if c != colour], 2)
    rule = border_rule(((True, a), (False, b)))

    def grid():
        g = blank(h, w)
        for _ in range(rng.randint(h * w // 40, h * w // 22)):
            _place(rng, g, _blob(rng, rng.randint(2, 7)), colour, margin=0, tries=30)
        return make(g)
    return rule, grid


# ---- generator -----------------------------------------------------------------
FAMILIES = {"gravity": (gravity_make, gravity_candidates), "mirror": (mirror_make, mirror_candidates),
            "rays": (rays_make, rays_candidates), "tiling": (tiling_make, tiling_candidates),
            "border": (border_make, border_candidates)}


def fair(family, train, test_in, test_out) -> bool:
    _, cands = FAMILIES[family]
    seen_true = False
    for r in cands(train):
        if any(r.apply(a) != b for a, b in train):
            continue
        p = r.apply(test_in)
        if p is None:
            return False          # a rule that fits the examples leaves the test undecided
        if p != test_out:
            return False          # a rule that fits the examples gives a different answer
        seen_true = True
    return seen_true


def generate_family(seed: int, family: str, size: str = "m", n_train: int = 3, max_tries: int = 400):
    from .gen import SIZES, Task
    make_rule, _ = FAMILIES[family]
    rng = random.Random(seed * 7919 + sum(map(ord, family)) * 31 + sum(map(ord, size)))
    lo, hi = SIZES[size]
    for _ in range(max_tries):
        rule, grid = make_rule(rng, rng.randint(lo, hi), rng.randint(lo, hi))
        pairs = []
        for _ in range(n_train + 1):
            x = grid()
            if isinstance(x, list):                    # mirror makes [covered, full]
                x, y = x
                if rule.apply(x) != y:
                    break
            y = rule.apply(x)
            if y is None or y == x:
                break
            pairs.append((x, y))
        if len(pairs) != n_train + 1:
            continue
        train, (ti, to) = pairs[:-1], pairs[-1]
        if not fair(family, train, ti, to):
            continue
        return Task(id=f"{family}-{size}/{seed}", seed=seed, depth=family, size=size, chain=[rule],
                    train=train, test_in=ti, test_out=to, effective_depth=0)
    raise RuntimeError(f"no fair {family} task for seed {seed}")
