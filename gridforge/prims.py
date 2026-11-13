"""Primitive grid transformations. Every task's hidden rule is a chain of these.

Each primitive is a (name, params) pair with a deterministic apply(). Primitives
raise Invalid when they do not apply, so a generated chain is always well defined.
`describe()` gives plain English, used only in reports, never shown to the model.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple

from .grid import MAX, Grid, Invalid, bbox, blank, colors, dims, make, objects

DIRS = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


# ---- geometry ---------------------------------------------------------------
def flip_h(g, _):
    return make(r[::-1] for r in g)


def flip_v(g, _):
    return make(g[::-1])


def rot90(g, _):
    return make(zip(*g[::-1]))


def rot180(g, _):
    return make(r[::-1] for r in g[::-1])


def transpose(g, _):
    return make(zip(*g))


def shift(g, p):
    dy, dx = p["dy"], p["dx"]
    h, w = dims(g)
    out = blank(h, w)
    for r in range(h):
        for c in range(w):
            out[(r + dy) % h][(c + dx) % w] = g[r][c]
    return make(out)


# ---- colour -----------------------------------------------------------------
def swap(g, p):
    a, b = p["a"], p["b"]
    cs = colors(g)
    if a not in cs and b not in cs:
        raise Invalid("neither colour present")
    m = {a: b, b: a}
    return make((m.get(v, v) for v in r) for r in g)


def invert(g, _):
    cs = colors(g)
    if len(cs) != 1:
        raise Invalid("needs exactly one colour")
    (c,) = cs
    return make((0 if v else c for v in r) for r in g)


def keep_majority(g, _):
    cnt = Counter(v for r in g for v in r if v)
    if len(cnt) < 2:
        raise Invalid("needs 2+ colours")
    (top, n1), (_, n2) = cnt.most_common(2)
    if n1 == n2:
        raise Invalid("tie")
    return make((v if v == top else 0 for v in r) for r in g)


def color_largest(g, p):
    objs = objects(g)
    if len(objs) < 2:
        raise Invalid("needs 2+ objects")
    sizes = sorted((len(cells) for _, cells in objs), reverse=True)
    if sizes[0] == sizes[1]:
        raise Invalid("tie for largest")
    out = [list(r) for r in g]
    for _, cells in objs:
        if len(cells) == sizes[0]:
            for y, x in cells:
                out[y][x] = p["c"]
    return make(out)


def color_by_size(g, p):
    """Objects of exactly one cell become colour a, all others colour b."""
    objs = objects(g)
    if not objs:
        raise Invalid("empty")
    out = [list(r) for r in g]
    for _, cells in objs:
        for y, x in cells:
            out[y][x] = p["a"] if len(cells) == 1 else p["b"]
    return make(out)


# ---- objects ----------------------------------------------------------------
def crop_largest(g, _):
    objs = objects(g)
    if len(objs) < 2:
        raise Invalid("needs 2+ objects")
    sizes = sorted((len(c) for _, c in objs), reverse=True)
    if sizes[0] == sizes[1]:
        raise Invalid("tie")
    cells = next(c for _, c in objs if len(c) == sizes[0])
    r0, c0, r1, c1 = bbox(cells)
    return make(row[c0:c1 + 1] for row in g[r0:r1 + 1])


def crop_smallest(g, _):
    objs = objects(g)
    if len(objs) < 2:
        raise Invalid("needs 2+ objects")
    sizes = sorted(len(c) for _, c in objs)
    if sizes[0] == sizes[1]:
        raise Invalid("tie")
    cells = next(c for _, c in objs if len(c) == sizes[0])
    r0, c0, r1, c1 = bbox(cells)
    return make(row[c0:c1 + 1] for row in g[r0:r1 + 1])


def denoise(g, _):
    objs = objects(g, diag=True)
    singles = [cells for _, cells in objs if len(cells) == 1]
    if not singles or len(singles) == len(objs):
        raise Invalid("no noise / only noise")
    out = [list(r) for r in g]
    for cells in singles:
        (y, x), = cells
        out[y][x] = 0
    return make(out)


def gravity(g, p):
    dy, dx = DIRS[p["d"]]
    h, w = dims(g)
    out = blank(h, w)
    if dx == 0:
        for c in range(w):
            col = [g[r][c] for r in range(h) if g[r][c]]
            rows = range(h - len(col), h) if dy > 0 else range(len(col))
            for r, v in zip(rows, col):
                out[r][c] = v
    else:
        for r in range(h):
            row = [v for v in g[r] if v]
            cols = range(w - len(row), w) if dx > 0 else range(len(row))
            for c, v in zip(cols, row):
                out[r][c] = v
    return make(out)


def fill_holes(g, p):
    """Background regions not connected to the border are filled with colour c."""
    h, w = dims(g)
    outside = [[False] * w for _ in range(h)]
    stack = [(r, c) for r in range(h) for c in (0, w - 1)] + [(r, c) for c in range(w) for r in (0, h - 1)]
    while stack:
        y, x = stack.pop()
        if not (0 <= y < h and 0 <= x < w) or outside[y][x] or g[y][x]:
            continue
        outside[y][x] = True
        stack += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    out = [list(r) for r in g]
    hit = False
    for y in range(h):
        for x in range(w):
            if g[y][x] == 0 and not outside[y][x]:
                out[y][x] = p["c"]
                hit = True
    if not hit:
        raise Invalid("no holes")
    return make(out)


def halo(g, p):
    """Background cells touching an object (8 neighbours) become colour c."""
    h, w = dims(g)
    out = [list(r) for r in g]
    for y in range(h):
        for x in range(w):
            if g[y][x]:
                continue
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and g[ny][nx]:
                        out[y][x] = p["c"]
    return make(out)


def boxes(g, p):
    """Draw each object's bounding box (one cell outside it) in colour c, on background only."""
    objs = objects(g)
    if not objs:
        raise Invalid("empty")
    h, w = dims(g)
    out = [list(r) for r in g]
    for _, cells in objs:
        r0, c0, r1, c1 = bbox(cells)
        r0, c0, r1, c1 = r0 - 1, c0 - 1, r1 + 1, c1 + 1
        for y in range(r0, r1 + 1):
            for x in range(c0, c1 + 1):
                if (y in (r0, r1) or x in (c0, c1)) and 0 <= y < h and 0 <= x < w and out[y][x] == 0:
                    out[y][x] = p["c"]
    return make(out)


def shoot(g, p):
    """Every non-background cell extends a ray in direction d until a non-background cell or the edge."""
    dy, dx = DIRS[p["d"]]
    h, w = dims(g)
    out = [list(r) for r in g]
    hit = False
    for y in range(h):
        for x in range(w):
            if not g[y][x]:
                continue
            ny, nx = y + dy, x + dx
            while 0 <= ny < h and 0 <= nx < w and g[ny][nx] == 0:
                if out[ny][nx] == 0:
                    out[ny][nx] = g[y][x]
                    hit = True
                ny, nx = ny + dy, nx + dx
    if not hit:
        raise Invalid("nothing to extend")
    return make(out)


def connect(g, p):
    """Two same-coloured cells in one row or column are joined by a line of colour c."""
    h, w = dims(g)
    out = [list(r) for r in g]
    hit = False
    pos = {}
    for y in range(h):
        for x in range(w):
            if g[y][x]:
                pos.setdefault(g[y][x], []).append((y, x))
    for col, cells in pos.items():
        for i, (y1, x1) in enumerate(cells):
            for y2, x2 in cells[i + 1:]:
                if y1 == y2:
                    seg = [(y1, x) for x in range(min(x1, x2) + 1, max(x1, x2))]
                elif x1 == x2:
                    seg = [(y, x1) for y in range(min(y1, y2) + 1, max(y1, y2))]
                else:
                    continue
                if seg and all(g[y][x] == 0 for y, x in seg):
                    for y, x in seg:
                        out[y][x] = p["c"]
                    hit = True
    if not hit:
        raise Invalid("no pairs")
    return make(out)


# ---- size-changing ----------------------------------------------------------
def scale(g, p):
    k = p["k"]
    h, w = dims(g)
    if h * k > MAX or w * k > MAX:
        raise Invalid("too big")
    return make([v for v in r for _ in range(k)] for r in g for _ in range(k))


def mirror_tile(g, _):
    h, w = dims(g)
    if 2 * h > MAX or 2 * w > MAX:
        raise Invalid("too big")
    top = [list(r) + list(r[::-1]) for r in g]
    return make(top + top[::-1])


def symmetrize(g, _):
    """Overlay the grid with its left-right mirror (background cells take the mirror's colour)."""
    m = flip_h(g, None)
    out = make((a if a else b for a, b in zip(r1, r2)) for r1, r2 in zip(g, m))
    return out


def count_bar(g, p):
    """Output a 1 x n row of colour c, n = number of objects."""
    n = len(objects(g))
    if n == 0:
        raise Invalid("empty")
    return make([[p["c"]] * n])


@dataclass(frozen=True)
class Prim:
    name: str
    params: Tuple[Tuple[str, object], ...] = ()

    @property
    def p(self) -> Dict:
        return dict(self.params)

    def apply(self, g: Grid) -> Grid:
        out = FUNCS[self.name][0](g, self.p)
        h, w = dims(out)
        if h == 0 or w == 0 or h > MAX or w > MAX:
            raise Invalid("bad size")
        return out

    def describe(self) -> str:
        return FUNCS[self.name][1].format(**self.p)

    def __str__(self):
        args = ",".join(f"{k}={v}" for k, v in self.params)
        return f"{self.name}({args})"


# name -> (function, description, param space, final_only, scene kinds it suits)
FUNCS: Dict[str, Tuple[Callable, str]] = {
    "flip_h": (flip_h, "mirror left-right"),
    "flip_v": (flip_v, "mirror top-bottom"),
    "rot90": (rot90, "rotate 90 degrees clockwise"),
    "rot180": (rot180, "rotate 180 degrees"),
    "transpose": (transpose, "transpose (swap rows and columns)"),
    "shift": (shift, "shift by ({dy},{dx}) with wrap-around"),
    "swap": (swap, "swap colours {a} and {b}"),
    "invert": (invert, "invert foreground and background"),
    "keep_majority": (keep_majority, "keep only the most common colour"),
    "color_largest": (color_largest, "paint the largest object colour {c}"),
    "color_by_size": (color_by_size, "single cells become {a}, larger objects {b}"),
    "crop_largest": (crop_largest, "crop to the largest object"),
    "crop_smallest": (crop_smallest, "crop to the smallest object"),
    "denoise": (denoise, "remove isolated single cells"),
    "gravity": (gravity, "everything falls {d}"),
    "fill_holes": (fill_holes, "fill enclosed holes with colour {c}"),
    "halo": (halo, "surround objects with colour {c}"),
    "boxes": (boxes, "draw a colour-{c} box around each object"),
    "shoot": (shoot, "every cell shoots a ray {d}"),
    "connect": (connect, "join same-coloured cells in a row/column with colour {c}"),
    "scale": (scale, "scale up {k}x"),
    "mirror_tile": (mirror_tile, "tile 2x2 with mirrored copies"),
    "symmetrize": (symmetrize, "make left-right symmetric"),
    "count_bar": (count_bar, "output a bar of colour {c}, one cell per object"),
}

# Which input scenes each primitive needs to do something interesting.
SCENE = {
    "fill_holes": "hollow", "connect": "pairs", "shoot": "dots", "invert": "mono",
    "denoise": "noisy", "keep_majority": "objects", "color_by_size": "noisy",
    "crop_largest": "objects", "crop_smallest": "objects", "color_largest": "objects",
    "count_bar": "objects", "symmetrize": "objects", "boxes": "sparse",
    "halo": "sparse", "scale": "small", "mirror_tile": "small",
}
FINAL_ONLY = {"count_bar"}
SHRINKS = {"crop_largest", "crop_smallest", "count_bar"}
GROWS = {"scale", "mirror_tile"}


def all_prims(palette=range(1, 10)) -> List[Prim]:
    """Every instantiated primitive (used for generation and the ambiguity filter)."""
    out = []
    for n in ("flip_h", "flip_v", "rot90", "rot180", "transpose", "invert", "keep_majority",
              "crop_largest", "crop_smallest", "denoise", "mirror_tile", "symmetrize"):
        out.append(Prim(n))
    for d in DIRS:
        out.append(Prim("gravity", (("d", d),)))
        out.append(Prim("shoot", (("d", d),)))
    for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (2, 0), (0, 2)):
        out.append(Prim("shift", (("dy", dy), ("dx", dx))))
    pal = list(palette)
    for c in pal:
        for n in ("color_largest", "fill_holes", "halo", "boxes", "connect", "count_bar"):
            out.append(Prim(n, (("c", c),)))
    for i, a in enumerate(pal):
        for b in pal[i + 1:]:
            out.append(Prim("swap", (("a", a), ("b", b))))
    for a in pal:
        for b in pal:
            if a != b:
                out.append(Prim("color_by_size", (("a", a), ("b", b))))
    for k in (2, 3):
        out.append(Prim("scale", (("k", k),)))
    return out


def run_chain(chain, g: Grid) -> Grid:
    for prim in chain:
        g = prim.apply(g)
    return g
