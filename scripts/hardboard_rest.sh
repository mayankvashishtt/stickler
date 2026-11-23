#!/bin/bash
# Re-run the Hard board puzzles lost to the Claude usage limit, then the remaining Claude models.
cd "$(dirname "$0")/.."
python3 -m stickler run --agent claude --model claude-fable-5-2 --families hood --seeds 10-11 --sizes xl --workers 2 --out results/fable-hardboard-redo
python3 - <<'PY'
import json
redo = {json.loads(l)["id"]: l for l in open("results/fable-hardboard-redo/results.jsonl")}
lines = [redo.get(json.loads(l)["id"], l) if "limit" in json.loads(l).get("crash", "") else l
         for l in open("results/fable-hardboard/results.jsonl")]
open("results/fable-hardboard/results.jsonl", "w").writelines(x if x.endswith("\n") else x + "\n" for x in lines)
print("merged", list(redo))
PY
for x in claude-opus-5-5:claude sonnet:sonnet haiku:haiku; do
  python3 -m stickler bench --agent claude --model ${x%%:*} --suite hardboard --workers 4 --out results/${x##*:}-hardboard &
done
wait
echo ALL-DONE
