"""Agents: oracle (knows the rule), copy (returns the input), claude (sealed CLI)."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile

from .gen import Task
from .grid import to_text
from .prims import run_chain


class Agent:
    name = "agent"

    def reset(self, task: Task):
        self.task = task

    def act(self, obs: str) -> str:
        raise NotImplementedError


class OracleAgent(Agent):
    name = "oracle"

    def act(self, obs):
        return "```grid\n" + to_text(run_chain(self.task.chain, self.task.test_in)) + "\n```"


class CopyAgent(Agent):
    """Baseline: answers with the test input unchanged."""
    name = "copy"

    def act(self, obs):
        return "```grid\n" + to_text(self.task.test_in) + "\n```"


class ClaudeCLIAgent(Agent):
    """`claude -p` with every tool off: no built-ins, no MCP servers, empty working dir."""

    def __init__(self, model=None, timeout=900):
        self.model, self.timeout = model, timeout
        self.name = f"claude:{model or 'default'}"

    def reset(self, task):
        super().reset(task)
        self.transcript = []

    def act(self, obs):
        self.transcript.append(obs)
        text = self.transcript[0]
        for i, t in enumerate(self.transcript[1:]):
            tag = "Your previous reply" if i % 2 == 0 else "Feedback"
            text += f"\n\n## {tag}\n\n{t}"
        with tempfile.TemporaryDirectory() as tmp:
            mcp = os.path.join(tmp, "mcp.json")
            with open(mcp, "w") as f:
                json.dump({"mcpServers": {}}, f)
            cmd = ["claude", "-p", "--output-format", "json", "--tools", "",
                   "--strict-mcp-config", "--mcp-config", mcp, "--no-session-persistence"]
            if self.model:
                cmd += ["--model", self.model]
            proc = subprocess.run(cmd, input=text, capture_output=True, text=True,
                                  timeout=self.timeout, cwd=tmp)
        try:
            data = json.loads(proc.stdout)
            reply = data.get("result") or ""
            turns = data.get("num_turns") or 1
        except json.JSONDecodeError:
            reply, turns = proc.stdout.strip(), 1
        if turns > 1:
            raise RuntimeError(f"model took {turns} turns: it tried to use a tool")
        reply = reply or f"(agent error: {proc.stderr.strip()[:300]})"
        self.transcript.append(reply)
        return reply


def make_agent(name, model=None):
    return {"oracle": OracleAgent, "copy": CopyAgent}[name]() if name != "claude" else ClaudeCLIAgent(model)
