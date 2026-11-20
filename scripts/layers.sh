#!/bin/bash
# Run one Claude model on the two extra layers. Usage: scripts/layers.sh <model> <tag> [workers]
m=$1; tag=$2; W=${3:-4}
python3 -m stickler bench --agent claude --model $m --suite steps --workers $W --out results/$tag-steps
python3 -m stickler bench --agent claude --model $m --suite fix --workers $W --out results/$tag-fix
python3 -m stickler bench --agent claude --model $m --suite trap --workers $W --out results/$tag-trap
