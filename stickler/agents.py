"""Agents: oracle (knows the rule), copy (returns the input), claude (sealed CLI), codex (sealed CLI),
openai (any OpenAI-compatible chat API: OpenAI, Gemini, DeepSeek, OpenRouter, Ollama, vLLM...)."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

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
        g = self.task.test_in
        for _ in range(self.task.steps):
            g = run_chain(self.task.chain, g)
        return "```grid\n" + to_text(g) + "\n```"


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
        data = None
        try:
            data = json.loads(proc.stdout)
            reply = data.get("result") or ""
            turns = data.get("num_turns") or 1
        except json.JSONDecodeError:
            reply, turns = proc.stdout.strip(), 1
        if isinstance(data, dict) and data.get("is_error"):
            # API-side stop (safety filter, limits): not a model answer, and not a tool attempt
            raise RuntimeError("API error, no answer: " + (data.get("result") or "")[:160].replace("\n", " "))
        if turns > 1:
            dbg = os.environ.get("STICKLER_DEBUG_DIR")
            if dbg:
                os.makedirs(dbg, exist_ok=True)
                with open(os.path.join(dbg, f"{self.task.id.replace('/', '_')}.json"), "w") as f:
                    f.write(proc.stdout)
            raise RuntimeError(f"model took {turns} turns: it tried to use a tool")
        reply = reply or f"(agent error: {proc.stderr.strip()[:300]})"
        self.transcript.append(reply)
        return reply


class CodexCLIAgent(Agent):
    """`codex exec` sealed as far as the CLI allows: empty dir, read-only sandbox, user config
    (MCP servers, plugins) ignored, extra features off. Codex always has a shell tool, so any
    tool event in the trace voids the answer, the same rule as the Claude runs.

    STICKLER_EFFORT    optional model_reasoning_effort (low/medium/high/xhigh)
    """

    OFF = ["apps", "browser_use", "computer_use", "image_generation", "multi_agent", "plugins",
           "in_app_browser", "goals", "hooks"]
    OK_ITEMS = {"agent_message", "reasoning", "error"}

    def __init__(self, model=None, timeout=900):
        self.model, self.timeout = model, timeout
        self.effort = os.environ.get("STICKLER_EFFORT")
        self.name = f"codex:{model or 'default'}"
        self.usage = {}

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
            cmd = ["codex", "exec", "--json", "--skip-git-repo-check", "--ephemeral",
                   "--ignore-user-config", "--ignore-rules", "-s", "read-only", "-C", tmp,
                   "-c", "web_search=\"disabled\""]
            for f in self.OFF:
                cmd += ["--disable", f]
            if self.model:
                cmd += ["-m", self.model]
            if self.effort:
                cmd += ["-c", f'model_reasoning_effort="{self.effort}"']
            proc = subprocess.run(cmd + ["-"], input=text, capture_output=True, text=True,
                                  timeout=self.timeout, cwd=tmp)
        reply, tools, failed = "", [], None
        for line in proc.stdout.splitlines():
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = ev.get("type")
            if t == "item.completed":
                item = ev.get("item") or {}
                if item.get("type") == "agent_message":
                    reply = item.get("text") or reply
                elif item.get("type") not in self.OK_ITEMS:
                    tools.append(item.get("type"))
            elif t == "item.started" and (ev.get("item") or {}).get("type") not in self.OK_ITEMS:
                tools.append(ev["item"].get("type"))
            elif t == "turn.completed":
                self.usage = ev.get("usage") or {}
            elif t == "turn.failed":
                failed = (ev.get("error") or {}).get("message", "")
        if tools:
            dbg = os.environ.get("STICKLER_DEBUG_DIR")
            if dbg:
                os.makedirs(dbg, exist_ok=True)
                with open(os.path.join(dbg, f"{self.task.id.replace('/', '_')}.jsonl"), "w") as f:
                    f.write(proc.stdout)
            raise RuntimeError(f"model tried to use a tool: {sorted(set(tools))}")
        if failed is not None:
            raise RuntimeError("API error, no answer: " + failed[:160].replace("\n", " "))
        reply = reply or f"(agent error: {proc.stderr.strip()[-300:]})"
        self.transcript.append(reply)
        return reply


class OpenAICompatAgent(Agent):
    """Any OpenAI-compatible /chat/completions endpoint. No tools are offered, same as the Claude runs.

    OPENAI_API_KEY      your key (not needed for a local server)
    OPENAI_BASE_URL     default https://api.openai.com/v1
                        e.g. https://generativelanguage.googleapis.com/v1beta/openai (Gemini),
                        https://api.deepseek.com/v1, https://openrouter.ai/api/v1, http://localhost:11434/v1 (Ollama)
    STICKLER_EFFORT    optional reasoning_effort (low/medium/high) for reasoning models
    """

    def __init__(self, model, timeout=1800):
        if not model:
            raise ValueError("--model is required for --agent openai")
        self.model, self.timeout = model, timeout
        self.base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.key = os.environ.get("OPENAI_API_KEY", "")
        self.effort = os.environ.get("STICKLER_EFFORT")
        self.name = f"openai:{model}"
        self.usage = {}

    def reset(self, task):
        super().reset(task)
        self.messages = []

    def act(self, obs):
        self.messages.append({"role": "user", "content": obs})
        body = {"model": self.model, "messages": self.messages}
        if self.effort:
            body["reasoning_effort"] = self.effort
        headers = {"Content-Type": "application/json"}
        if self.key:
            headers["Authorization"] = f"Bearer {self.key}"
        req = urllib.request.Request(self.base + "/chat/completions", json.dumps(body).encode(), headers)
        for attempt in range(6):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    data = json.load(r)
                break
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503, 504) and attempt < 5:
                    time.sleep(5 * 2 ** attempt)
                    continue
                raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:300]}") from None
        msg = data["choices"][0]["message"]
        if msg.get("tool_calls"):
            raise RuntimeError("model tried to call a tool")
        reply = msg.get("content") or ""
        self.usage = data.get("usage") or {}
        self.messages.append({"role": "assistant", "content": reply})
        return reply


def make_agent(name, model=None):
    if name == "claude":
        return ClaudeCLIAgent(model, timeout=int(os.environ.get("STICKLER_TIMEOUT", 900)))
    if name == "codex":
        return CodexCLIAgent(model, timeout=int(os.environ.get("STICKLER_TIMEOUT", 900)))
    if name == "openai":
        return OpenAICompatAgent(model)
    return {"oracle": OracleAgent, "copy": CopyAgent}[name]()
