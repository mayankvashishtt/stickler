"""Grid helpers. A grid is a tuple of row tuples of ints 0-9; 0 is the background."""
from __future__ import annotations

from typing import List, Tuple

Grid = Tuple[Tuple[int, ...], ...]
MAX = 30


class Invalid(Exception):
    """A transformation does not apply to this grid."""


def make(rows) -> Grid:
    return tuple(tuple(int(v) for v in r) for r in rows)


def blank(h: int, w: int, c: int = 0) -> List[List[int]]:
    return [[c] * w for _ in range(h)]


def dims(g: Grid):
    return len(g), (len(g[0]) if g else 0)


def colors(g: Grid) -> set:
    return {v for r in g for v in r if v != 0}


def objects(g: Grid, diag: bool = False):
    """Connected same-colour components of non-background cells, in reading order.
    Each object is (colour, [(r, c), ...])."""
    h, w = dims(g)
    seen = [[False] * w for _ in range(h)]
    out = []
    steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diag:
        steps += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for r in range(h):
        for c in range(w):
            if g[r][c] == 0 or seen[r][c]:
                continue
            col, stack, cells = g[r][c], [(r, c)], []
            seen[r][c] = True
            while stack:
                y, x = stack.pop()
                cells.append((y, x))
                for dy, dx in steps:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and not seen[ny][nx] and g[ny][nx] == col:
                        seen[ny][nx] = True
                        stack.append((ny, nx))
            out.append((col, sorted(cells)))
    return out


def bbox(cells):
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def to_text(g: Grid) -> str:
    return "\n".join(" ".join(str(v) for v in r) for r in g)


def parse_text(text: str) -> Grid:
    rows = []
    for line in text.strip().splitlines():
        line = line.strip().strip("[](),")
        if not line:
            continue
        cells = [t for t in line.replace(",", " ").split() if t]
        if not all(t.isdigit() and len(t) == 1 for t in cells):
            if line.isdigit():
                cells = list(line)
            else:
                raise ValueError(f"not a grid row: {line!r}")
        rows.append([int(t) for t in cells])
    if not rows or any(len(r) != len(rows[0]) for r in rows):
        raise ValueError("rows have different lengths")
    return make(rows)


def cell_accuracy(pred: Grid, gold: Grid) -> float:
    if dims(pred) != dims(gold):
        return 0.0
    h, w = dims(gold)
    same = sum(pred[r][c] == gold[r][c] for r in range(h) for c in range(w))
    return same / (h * w)
