"""Two self-explaining Slack images for the Game of Life failures.

    python3 scripts/slack_cards.py      # writes proof/slack_1_one_cell.png, proof/slack_2_wrong_rule.png
"""
import glob
import html
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from cards import CHROME, PALETTE, grid_html, trim  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
N8 = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]

CSS = """
*{box-sizing:border-box}body{margin:0;background:#0d0f12;color:#e6e6e6;
font:18px/1.5 -apple-system,'SF Pro Text',Helvetica,sans-serif;padding:44px;width:1200px}
.tag{font:600 13px 'SF Mono',Menlo,monospace;letter-spacing:.08em;color:#8a94a6;text-transform:uppercase}
h1{font-size:40px;line-height:1.15;margin:10px 0 12px;font-weight:800;letter-spacing:-.01em}
h1 em{font-style:normal;color:#ff6b6b}
.sub{font-size:20px;color:#b8c0cc;margin:0 0 28px;max-width:1050px}
.task{background:#161a20;border:1px solid #262c35;border-radius:12px;padding:16px 20px;margin-bottom:24px;color:#cfd6e0}
.task b{color:#fff}
.row{display:flex;gap:18px;align-items:flex-start}
.panel{background:#161a20;border:1px solid #262c35;border-radius:12px;padding:14px 16px}
.panel.bad{border-color:#7a2d33;background:#1d1214}.panel.good{border-color:#2c6b45;background:#0f1d15}
.lbl{font:700 13px 'SF Mono',Menlo,monospace;color:#8a94a6;letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px}
.bad .lbl{color:#ff8a8a}.good .lbl{color:#7ee2a5}
.g{display:inline-grid;gap:1px;background:#2a2f37;border:1px solid #2a2f37}
.g div{width:var(--s);height:var(--s)}
.g div.x{outline:3px solid #ff3b3b;outline-offset:-3px}
.g div.f{outline:3px solid #fff;outline-offset:-3px}
.why{display:flex;gap:28px;align-items:center;margin-top:24px;background:#1d1214;border:1px solid #7a2d33;
border-radius:14px;padding:22px 26px}
.why h2{margin:0 0 8px;font-size:24px}
.why p{margin:6px 0;color:#d6dbe3}
.quote{font:15px/1.55 'SF Mono',Menlo,monospace;color:#e8dcc4;white-space:pre-wrap;margin-top:8px}
.two{display:flex;gap:18px;margin-top:24px}.two .panel{flex:1}
.big{font:800 34px -apple-system,Helvetica,sans-serif}
.foot{margin-top:26px;padding-top:18px;border-top:1px solid #262c35;color:#9aa3b2;font-size:16px}
.foot b{color:#fff}
"""


def load(task_id):
    for f in glob.glob(os.path.join(ROOT, "results/*/results.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if r["id"] == task_id:
                return r
    raise SystemExit(f"{task_id} not found")


def wrong(exp, pred):
    return sum(1 for r in range(len(exp)) for c in range(len(exp[0])) if exp[r][c] != pred[r][c])


def three(rec, s):
    exp, pred = rec["expected"], rec["pred"]
    return (f"<div class='row'>"
            f"<div class='panel'><div class='lbl'>New grid (input)</div>{grid_html(rec['test_in'], s)}</div>"
            f"<div class='panel bad'><div class='lbl'>Claude's answer</div>{grid_html(pred, s, diff_against=exp)}</div>"
            f"<div class='panel good'><div class='lbl'>Correct answer</div>{grid_html(exp, s)}</div></div>")


def zoom(g, y, x, k=2, s=46):
    """Cut a (2k+1)^2 window around (y, x); the centre cell gets a white outline."""
    h, w = len(g), len(g[0])
    cells, cols = [], 0
    for r in range(y - k, y + k + 1):
        for c in range(x - k, x + k + 1):
            inside = 0 <= r < h and 0 <= c < w
            col = PALETTE[g[r][c]] if inside else "#0d0f12"
            cells.append(f"<div style='background:{col}'{' class=f' if (r, c) == (y, x) else ''}></div>")
        cols = 2 * k + 1
    return (f"<div class='g' style='--s:{s}px;grid-template-columns:repeat({cols},{s}px)'>"
            + "".join(cells) + "</div>")


def page(body):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"


FOOT = ("<div class='foot'><b>Claude solved 5 of 20 of these puzzles.</b> Model: Claude Opus 5.5 (Claude Code), "
        "every tool switched off. Each puzzle is freshly generated and checked so that only one answer fits the "
        "4 examples. GridForge benchmark.</div>")

TASK = ("<div class='task'><b>The task:</b> a secret rule turns one grid into another. Claude sees 4 examples, "
        "must work out the rule, then apply it to a new grid. The rule: every square looks at its 8 neighbours "
        "and decides to light up or go dark. Exact answer required.</div>")


def card_one_cell():
    rec = load("life-l/13")
    exp, pred, g = rec["expected"], rec["pred"], rec["test_in"]
    n = len(exp) * len(exp[0])
    y, x = next((r, c) for r in range(len(exp)) for c in range(len(exp[0])) if exp[r][c] != pred[r][c])
    nb = sum(1 for a, b in N8 if 0 <= y + a < len(g) and 0 <= x + b < len(g[0]) and g[y + a][x + b])
    claude_rule = ("- A 7 cell survives if it has 0, 3, 4 or 5 neighbouring 7s.\n"
                   "- A 0 cell becomes 7 if it has exactly 3 or 5 neighbouring 7s.")
    body = (
        "<div class='tag'>Where Claude broke &middot; 1 of 2</div>"
        f"<h1>Claude got {n - 1} of {n} squares right.<br><em>It still failed.</em></h1>"
        "<p class='sub'>It figured out the secret rule perfectly and wrote it down. Then, applying it by hand, "
        "it miscounted one square.</p>" + TASK + three(rec, 14) +
        "<div class='why'>" + zoom(g, y, x) +
        "<div><h2>The one wrong square (white outline, zoomed in from the input)</h2>"
        f"<p>It is empty and has <b>{nb} lit neighbours</b>. Claude's own rule says that means it lights up. "
        "Claude left it dark.</p>"
        "<p style='color:#9aa3b2;margin-top:12px'>The rule Claude wrote, word for word:</p>"
        f"<div class='quote'>{html.escape(claude_rule)}</div></div></div>" + FOOT)
    return page(body), "slack_1_one_cell"


def card_wrong_rule():
    rec = load("life-xl/12")
    exp, pred = rec["expected"], rec["pred"]
    n, bad = len(exp) * len(exp[0]), wrong(exp, pred)
    body = (
        "<div class='tag'>Where Claude broke &middot; 2 of 2</div>"
        f"<h1>Claude checked its theory on 7 squares<br>and called it done. <em>{bad} of {n} wrong.</em></h1>"
        "<p class='sub'>On a bigger grid it guessed a neat-sounding rule, tested it on a handful of squares, "
        "and never noticed the examples already contradict it.</p>" + TASK + three(rec, 10) +
        "<div class='two'>"
        "<div class='panel bad'><div class='lbl'>What Claude decided</div>"
        "<div class='quote'>\"A cell becomes 4 if an odd number of its\n8 neighbours are 4, and 0 otherwise.\"</div>"
        "<p style='margin:12px 0 0;color:#d6dbe3'>This guess is already wrong on <b>224 squares of Example 1</b> "
        "alone. Claude checked 7.</p></div>"
        "<div class='panel good'><div class='lbl'>The real rule</div>"
        "<p style='margin:0;color:#d6dbe3'>Empty square lights up with <b>3, 6 or 8</b> lit neighbours.<br>"
        "Lit square stays lit with <b>1 or 4</b>.<br>Everything else goes dark.</p></div>"
        "</div>" + FOOT)
    return page(body), "slack_2_wrong_rule"


def shoot(doc, name):
    out = os.path.join(ROOT, "proof")
    hp, png = os.path.join(out, name + ".html"), os.path.join(out, name + ".png")
    open(hp, "w").write(doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--screenshot={png}",
                    "--window-size=1288,2400", "--force-device-scale-factor=2", "file://" + os.path.abspath(hp)],
                   check=True, capture_output=True)
    os.remove(hp)
    trim(png)
    print(os.path.abspath(png))


if __name__ == "__main__":
    for doc, name in (card_one_cell(), card_wrong_rule()):
        shoot(doc, name)
