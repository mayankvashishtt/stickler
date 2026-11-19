"""Screenshot cards of real Claude failures: examples, test input, Claude's grid, correct grid.

    python3 scripts/cards.py results/claude-pilot/results.jsonl proof/
"""
import html
import json
import os
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PALETTE = ["#111418", "#1e88e5", "#e53935", "#43a047", "#fdd835", "#8e8e8e",
           "#d81b60", "#fb8c00", "#4fc3f7", "#8d1c1c"]

CSS = """
*{box-sizing:border-box}body{margin:0;background:#0d0f12;color:#e6e6e6;
font:16px/1.45 -apple-system,'SF Pro Text',Helvetica,sans-serif;padding:34px;width:1200px}
.tag{font:600 12px 'SF Mono',Menlo,monospace;letter-spacing:.08em;color:#8a94a6;text-transform:uppercase}
h1{font-size:30px;margin:4px 0 20px;font-weight:700}
.row{display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap}
.panel{background:#161a20;border:1px solid #262c35;border-radius:12px;padding:14px 16px}
.panel.bad{border-color:#6b2a2f;background:#1d1214}.panel.good{border-color:#2c6b45;background:#0f1d15}
.lbl{font:600 12px 'SF Mono',Menlo,monospace;color:#8a94a6;letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px}
.bad .lbl{color:#ff8a8a}.good .lbl{color:#7ee2a5}
.g{display:inline-grid;gap:1px;background:#2a2f37;border:1px solid #2a2f37}
.g div{width:var(--s);height:var(--s)}
.g div.x{outline:2px solid #ff3b3b;outline-offset:-2px}
.arrow{font-size:26px;color:#5a6270;align-self:center}
.sec{margin:22px 0 10px}
.quote{font:14px/1.5 'SF Mono',Menlo,monospace;color:#e8dcc4;white-space:pre-wrap}
.foot{color:#8a94a6;font-size:13px;margin-top:18px}
.big{font:700 22px 'SF Mono',Menlo,monospace}
"""


def grid_html(g, size, diff_against=None):
    h, w = len(g), len(g[0])
    cells = []
    for r in range(h):
        for c in range(w):
            bad = diff_against is not None and (r >= len(diff_against) or c >= len(diff_against[0])
                                                or diff_against[r][c] != g[r][c])
            cells.append(f"<div style='background:{PALETTE[g[r][c]]}'{' class=x' if bad else ''}></div>")
    return (f"<div class='g' style='--s:{size}px;grid-template-columns:repeat({w},{size}px)'>"
            + "".join(cells) + "</div>")


def cell(g, budget):
    return max(6, min(26, budget // max(len(g), len(g[0]))))


def last_reasoning(reply, n=6):
    text = reply.split("```grid")[0].strip()
    lines = [l for l in text.splitlines() if l.strip()]
    return "\n".join(lines[-n:])


def card(rec, out_dir):
    exp, pred, test = rec["expected"], rec["pred"], rec["test_in"]
    ex_panels = ""
    for i, (x, y) in enumerate(rec["train"][:3], 1):
        s = cell(max(x, y, key=lambda g: len(g) * len(g[0])), 150)
        ex_panels += (f"<div class='panel'><div class='lbl'>Example {i}</div><div class='row'>"
                      f"{grid_html(x, s)}<div class='arrow'>&rarr;</div>{grid_html(y, s)}</div></div>")
    s = cell(max(test, exp, key=lambda g: len(g) * len(g[0])), 330)
    if pred is not None:
        wrong = (sum(1 for r in range(len(exp)) for c in range(len(exp[0]))
                     if r >= len(pred) or c >= len(pred[0]) or pred[r][c] != exp[r][c])
                 if (len(pred), len(pred[0])) == (len(exp), len(exp[0])) else None)
        pred_html = grid_html(pred, s, diff_against=exp)
        verdict = (f"{wrong} of {len(exp) * len(exp[0])} cells wrong" if wrong is not None
                   else f"wrong size: {len(pred)}x{len(pred[0])}, should be {len(exp)}x{len(exp[0])}")
    else:
        pred_html, verdict = "<div class='big'>no grid</div>", rec.get("error") or "no answer"
    body = (
        f"<div class='tag'>Real run &middot; Stickler</div>"
        f"<h1>Claude got this puzzle wrong</h1>"
        f"<div class='lbl'>The examples it was given</div><div class='row'>{ex_panels}</div>"
        f"<div class='sec row'>"
        f"<div class='panel'><div class='lbl'>Test input</div>{grid_html(test, s)}</div>"
        f"<div class='panel bad'><div class='lbl'>Claude's answer &middot; {html.escape(verdict)}</div>{pred_html}</div>"
        f"<div class='panel good'><div class='lbl'>Correct answer</div>{grid_html(exp, s)}</div></div>"
        f"<div class='panel'><div class='lbl'>End of Claude's reasoning, verbatim</div>"
        f"<div class='quote'>{html.escape(last_reasoning(rec['replies'][-1]))}</div></div>"
        f"<div class='panel' style='margin-top:14px'><div class='lbl'>Hidden rule</div>"
        f"<div class='quote'>{html.escape(rec['rule'])}</div></div>"
        f"<div class='foot'>Claude Opus 5.5 via Claude Code CLI, all tools off. Puzzle {html.escape(rec['id'])}, "
        f"generated from a seed, checked so every simple rule that fits the examples gives this same answer.</div>")
    name = "fail_" + rec["id"].replace("/", "_")
    hp = os.path.join(out_dir, name + ".html")
    with open(hp, "w") as f:
        f.write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
    png = os.path.join(out_dir, name + ".png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--screenshot={png}",
                    "--window-size=1268,2600", "--force-device-scale-factor=2", "file://" + os.path.abspath(hp)],
                   check=True, capture_output=True)
    os.remove(hp)
    trim(png)
    return png


def trim(png, pad=60):
    """Cut the empty background below the content."""
    from PIL import Image
    im = Image.open(png).convert("RGB")
    w, h = im.size
    bg = im.getpixel((w - 1, h - 1))
    px = im.load()
    bottom = h - 1
    while bottom > 0 and all(px[x, bottom] == bg for x in range(0, w, 7)):
        bottom -= 1
    im.crop((0, 0, w, min(h, bottom + pad))).save(png)


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    only = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
    for line in open(src):
        r = json.loads(line)
        if r.get("replies") and not r["solved"] and (only is None or r["id"] in only):
            print(card(r, out))
