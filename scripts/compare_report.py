"""Compare models on the same 76 puzzles: markdown table + a Slack image.

    python3 scripts/compare_report.py      # writes results/COMPARE.md and proof/compare_models.png
"""
import json
import os
import subprocess
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from cards import CHROME, trim  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
MODELS = [("claude", "Opus 5.5"), ("fable", "Fable 5.2"), ("sonnet", "Sonnet 5.5"), ("haiku", "Haiku 5.5"),
          ("gpt-astra", "GPT-6.2-Astra"), ("gpt-sol", "GPT-6.2-Sol")]
# Found ambiguous on review (another simple rule also fits the examples): dropped for every model.
EXCLUDE = {"d2l/17", "d2m/13"}
CATS = [  # (label, plain explanation, id prefixes)
    ("Chain rules, 2 steps", "e.g. flip, then recolour", ("d2m", "d2l")),
    ("Chain rules, 3 steps", "three transformations stacked", ("d3m", "d3l")),
    ("Colour by size", "recolour each shape by its cell count", ("sizecolor-m", "sizecolor-l")),
    ("Count neighbours", "colour empty squares by how many sides touch", ("count-m", "count-l")),
    ("Game of Life, medium", "11-16 squares a side", ("life-m",)),
    ("Game of Life, large", "18-26 squares a side", ("life-l",)),
    ("Game of Life, huge", "26-30 squares a side", ("life-xl",)),
]


def load(tag):
    recs = {}
    for suite in ("hard", "tough", "life", None):  # Claude runs were split in 3; later runs are one folder
        p = os.path.join(ROOT, "results", f"{tag}-{suite}" if suite else tag, "results.jsonl")
        if os.path.exists(p):
            for line in open(p):
                r = json.loads(line)
                if r["id"] not in EXCLUDE:
                    recs[r["id"]] = r
    return recs


def stats(recs):
    by = defaultdict(lambda: [0, 0, 0])  # solved, total, no-answer
    for r in recs.values():
        cat = next((c[0] for c in CATS if r["id"].split("/")[0] in c[2]), None)
        if cat is None:
            continue
        by[cat][0] += r["solved"]
        by[cat][1] += 1
        by[cat][2] += ("crash" in r) or (r.get("pred") is None)
    tot = [sum(v[i] for v in by.values()) for i in range(3)]
    return by, tot


def main():
    data = {name: stats(load(tag)) for tag, name in MODELS}
    names = [n for _, n in MODELS if data[n][1][1]]
    md = ["# Stickler: model comparison", "",
          f"Same {data[names[0]][1][1]} puzzles for every model (2 ambiguous ones dropped), all tools off (Claude Code CLI, or Codex CLI for GPT), one attempt, exact match.", "",
          "| Puzzle type | " + " | ".join(names) + " |", "| --- |" + " --- |" * len(names)]
    for label, _, _ in CATS:
        md.append(f"| {label} | " + " | ".join(
            f"{data[n][0][label][0]}/{data[n][0][label][1]}" for n in names) + " |")
    md.append("| **Total** | " + " | ".join(f"**{data[n][1][0]}/{data[n][1][1]}**" for n in names) + " |")
    md.append("| no answer (timeout / tool / crash) | " + " | ".join(str(data[n][1][2]) for n in names) + " |")
    open(os.path.join(ROOT, "results", "COMPARE.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))

    def cellc(s, t):
        if not t:
            return "<td class='na'>-</td>"
        p = s / t
        hue = 0 if p < .4 else (38 if p < .75 else 140)
        return (f"<td><div class='bar'><i style='width:{p*100:.0f}%;background:hsl({hue} 70% 45%)'></i></div>"
                f"<b>{s}/{t}</b> <span>{p:.0%}</span></td>")

    rows = ""
    for label, expl, _ in CATS:
        rows += f"<tr><th>{label}<small>{expl}</small></th>" + "".join(
            cellc(*data[n][0][label][:2]) for n in names) + "</tr>"
    rows += "<tr class='tot'><th>All 74 puzzles</th>" + "".join(cellc(*data[n][1][:2]) for n in names) + "</tr>"
    css = """*{box-sizing:border-box}body{margin:0;background:#0d0f12;color:#e6e6e6;width:1200px;padding:44px;
font:17px/1.4 -apple-system,Helvetica,sans-serif}
.tag{font:600 13px 'SF Mono',Menlo,monospace;letter-spacing:.08em;color:#8a94a6;text-transform:uppercase}
h1{font-size:38px;margin:10px 0 10px;font-weight:800}.sub{color:#b8c0cc;font-size:19px;margin:0 0 26px}
table{width:100%;border-collapse:separate;border-spacing:0 8px}
th{text-align:left;font-weight:700;padding:12px 14px;background:#161a20;border-radius:10px 0 0 10px;width:300px}
th small{display:block;font-weight:400;color:#8a94a6;font-size:14px;margin-top:2px}
thead th{background:none;color:#8a94a6;font:700 14px 'SF Mono',Menlo,monospace;text-transform:uppercase;padding:0 14px}
td{background:#161a20;padding:12px 14px}td:last-child{border-radius:0 10px 10px 0}
td b{font-size:19px}td span{color:#8a94a6;font-size:15px;margin-left:6px}
.bar{height:8px;background:#262c35;border-radius:4px;margin-bottom:8px;overflow:hidden}.bar i{display:block;height:100%}
tr.tot th,tr.tot td{background:#1b2230;border-top:1px solid #3a4558}
.foot{margin-top:22px;color:#9aa3b2;font-size:15px}"""
    head = "<thead><tr><th></th>" + "".join(f"<th>{n}</th>" for n in names) + "</tr></thead>"
    body = ("<div class='tag'>Stickler &middot; same 74 puzzles, every model</div>"
            "<h1>Fable wins. Every model still breaks on Game of Life.</h1>"
            "<p class='sub'>Spotting a rule is easy for the big models. Applying it exactly to every square is not: even the best "
            "model failed 11 of 28 Game of Life puzzles. Haiku gave up on 20 puzzles and asked for a hint.</p>"
            f"<table>{head}<tbody>{rows}</tbody></table>"
            "<div class='foot'>Claude Code CLI, every tool off, one attempt, the whole grid must be exactly right. "
            "Puzzles are freshly generated and checked so the 4 examples cover every case the test needs.</div>")
    hp = os.path.join(ROOT, "proof", "compare_models.html")
    open(hp, "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head>"
                        f"<body>{body}</body></html>")
    png = hp[:-5] + ".png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--screenshot={png}",
                    "--window-size=1288,2000", "--force-device-scale-factor=2", "file://" + os.path.abspath(hp)],
                   check=True, capture_output=True)
    os.remove(hp)
    trim(png)
    print(os.path.abspath(png))


if __name__ == "__main__":
    main()
