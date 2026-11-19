# Stickler: model comparison

Same 74 puzzles for every model (2 ambiguous ones dropped), Claude Code CLI, all tools off, one attempt, exact match.

| Puzzle type | Opus 5.5 | Fable 5.2 | Sonnet 5.5 | Haiku 5.5 |
| --- | --- | --- | --- | --- |
| Chain rules, 2 steps | 11/14 | 13/14 | 12/14 | 10/14 |
| Chain rules, 3 steps | 16/16 | 14/16 | 8/16 | 9/16 |
| Colour by size | 8/8 | 7/8 | 8/8 | 8/8 |
| Count neighbours | 7/8 | 8/8 | 1/8 | 3/8 |
| Game of Life, medium | 1/4 | 2/4 | 1/4 | 0/4 |
| Game of Life, large | 5/14 | 10/14 | 1/14 | 0/14 |
| Game of Life, huge | 2/10 | 5/10 | 1/10 | 0/10 |
| **Total** | **50/74** | **59/74** | **32/74** | **30/74** |
| no answer (timeout / tool / crash) | 0 | 0 | 0 | 20 |
