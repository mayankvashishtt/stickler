#!/bin/bash
# Run one model on the extra layers. Usage: [AGENT=codex] scripts/layers.sh <model> <tag> [workers]
m=$1; tag=$2; W=${3:-4}; A=${AGENT:-claude}
python3 -m stickler bench --agent $A --model $m --suite steps --workers $W --out results/$tag-steps
python3 -m stickler bench --agent $A --model $m --suite fix --workers $W --out results/$tag-fix
python3 -m stickler bench --agent $A --model $m --suite trap --workers $W --out results/$tag-trap
