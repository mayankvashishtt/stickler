#!/bin/bash
# Run one model over the three suites Opus already did (same seeds -> identical puzzles).
m=$1; tag=$2; W=${3:-5}
python3 -m gridforge run --agent claude --model $m --seeds 10-17 --depths 2,3 --sizes m,l --workers $W --out results/$tag-hard
python3 -m gridforge run --agent claude --model $m --families life,count,sizecolor --seeds 0-3 --sizes m,l --workers $W --out results/$tag-tough
python3 -m gridforge run --agent claude --model $m --families life --seeds 4-13 --sizes l,xl --workers $W --out results/$tag-life
