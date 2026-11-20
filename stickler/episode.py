"""Prompt building, answer parsing and grading, plus a multi-turn RL environment."""
from __future__ import annotations

import re
from typing import Optional, Tuple

from .gen import Task
from .grid import Grid, cell_accuracy, dims, parse_text, to_text

INSTRUCTIONS = """You are solving a grid puzzle. Each grid is rows of digits 0-9 (0 is background,
other digits are colours). Every example input is turned into its output by the same hidden rule.
Work out the rule, then apply it to the test input.

You cannot run code. Reason it out.

End your reply with the output grid in a fenced block labelled `grid`, one row per line,
digits separated by spaces, for example:

```grid
0 1 0
1 1 1
```"""


def prompt(task: Task) -> str:
    parts = [INSTRUCTIONS, ""]
    for i, (x, y) in enumerate(task.train, 1):
        hx, wx = dims(x)
        hy, wy = dims(y)
        parts += [f"## Example {i}", f"Input ({hx}x{wx}):", "```", to_text(x), "```",
                  f"Output ({hy}x{wy}):", "```", to_text(y), "```", ""]
    h, w = dims(task.test_in)
    parts += [f"## Test", f"Input ({h}x{w}):", "```", to_text(task.test_in), "```", ""]
    if task.steps > 1:
        parts += [f"The examples show ONE application of the rule. For the test, apply the rule "
                  f"{task.steps} times in a row: each output becomes the next input.",
                  f"What is the grid after {task.steps} steps? Give only the final grid."]
    elif task.given is not None:
        n = task.given_wrong
        parts += ["## A proposed answer",
                  "Someone applied the rule to the test input and got this grid:", "```", to_text(task.given), "```",
                  f"Exactly {n} square{'s are' if n > 1 else ' is'} wrong. Find {'them' if n > 1 else 'it'} "
                  "and give the fully corrected output grid."]
    else:
        parts += ["What is the output grid?"]
    return "\n".join(parts)


def parse_answer(reply: str) -> Tuple[Optional[Grid], Optional[str]]:
    blocks = re.findall(r"```grid\s*\n(.*?)```", reply, re.S)
    if not blocks:
        blocks = re.findall(r"```[a-z]*\s*\n(.*?)```", reply, re.S)
    if not blocks:
        return None, "no grid block found"
    try:
        return parse_text(blocks[-1]), None
    except ValueError as e:
        return None, str(e)


def grade(task: Task, reply: str) -> dict:
    g, err = parse_answer(reply)
    if g is None:
        return {"solved": False, "cell_acc": 0.0, "error": err, "pred": None}
    return {"solved": g == task.test_out, "cell_acc": round(cell_accuracy(g, task.test_out), 4),
            "error": None if dims(g) == dims(task.test_out) else
            f"wrong size {dims(g)} vs {dims(task.test_out)}", "pred": g}


class GridEnv:
    """reset() -> prompt; step(reply) -> (obs, reward, done, info).

    Reward is 1.0 for an exact grid; otherwise 0.5 * share of correct cells (0 if the
    size is wrong), so partial progress is visible but never confused with a solve.
    Feedback says how many cells are wrong, never which ones.
    """

    def __init__(self, task: Task, max_turns: int = 1):
        self.task, self.max_turns = task, max_turns

    def reset(self) -> str:
        self.turn = 0
        self.history = []
        return prompt(self.task)

    def step(self, reply: str):
        self.turn += 1
        res = grade(self.task, reply)
        self.history.append(res)
        reward = 1.0 if res["solved"] else 0.5 * res["cell_acc"]
        done = res["solved"] or self.turn >= self.max_turns
        if res["solved"]:
            obs = "Correct."
        elif res["pred"] is None:
            obs = f"Could not read your grid: {res['error']}. Reply again with a ```grid block."
        elif res["error"]:
            obs = f"Wrong: {res['error']}. Try again."
        else:
            h, w = dims(self.task.test_out)
            wrong = round((1 - res["cell_acc"]) * h * w)
            obs = f"Wrong: {wrong} of {h * w} cells differ. Try again."
        return obs, reward, done, res
