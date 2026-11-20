# Stickler report: claude:claude-fable-5-2

Solved 6/12 (50%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| trap | 12 | 50% | 50% | 0.95 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| m | 12 | 50% | 50% | 0.95 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| trap-m/0 | no | 0.88 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2] survives (8 neighbours) |
| trap-m/1 | no | 0.88 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2] survives (8 neighbours) |
| trap-m/10 | no | 0.89 | one step of a Life-like automaton: empty cell with [3, 4] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/11 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [3] survives (8 neighbours) |
| trap-m/2 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 3] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/3 | no | 0.90 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2] survives (8 neighbours) |
| trap-m/4 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2] survives (8 neighbours) |
| trap-m/5 | no | 0.99 | one step of a Life-like automaton: empty cell with [2, 3] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/6 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 3] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/7 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2] survives (8 neighbours) |
| trap-m/8 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 3] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/9 | no | 0.90 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2, 3, 4] survives (8 neighbours) |
