# Stickler: model comparison

Same 74 puzzles for every model (2 ambiguous ones dropped), all tools off (Claude Code CLI, or Codex CLI for GPT), one attempt, exact match.

| Puzzle type | Opus 5.5 | Fable 5.2 | Sonnet 5.5 | Haiku 5.5 | GPT-6.2-Astra | GPT-6.2-Sol |
| --- | --- | --- | --- | --- | --- | --- |
| Chain rules, 2 steps | 11/14 | 13/14 | 12/14 | 10/14 | 12/14 | 11/14 |
| Chain rules, 3 steps | 16/16 | 14/16 | 8/16 | 9/16 | 15/16 | 14/16 |
| Colour by size | 8/8 | 7/8 | 8/8 | 8/8 | 8/8 | 4/8 |
| Count neighbours | 7/8 | 8/8 | 1/8 | 3/8 | 7/8 | 8/8 |
| Game of Life, medium | 1/4 | 2/4 | 1/4 | 0/4 | 3/4 | 4/4 |
| Game of Life, large | 5/14 | 10/14 | 1/14 | 0/14 | 13/14 | 7/14 |
| Game of Life, huge | 2/10 | 5/10 | 1/10 | 0/10 | 9/10 | 2/10 |
| **Total** | **50/74** | **59/74** | **32/74** | **30/74** | **67/74** | **50/74** |
| no answer (timeout / tool / crash) | 0 | 0 | 0 | 20 | 0 | 3 |
