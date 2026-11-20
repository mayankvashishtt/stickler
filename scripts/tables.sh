#!/bin/bash
# Tables level (control test) on the four Claude models in parallel, then GPT once its layers run ends.
W=${1:-3}
for x in claude-fable-5-2:fable claude-opus-5-5:claude sonnet:sonnet haiku:haiku; do
  python3 -m stickler bench --agent claude --model ${x%%:*} --suite tables --workers $W --out results/${x##*:}-tables &
done
wait
