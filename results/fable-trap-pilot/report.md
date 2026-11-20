# Stickler report: claude:claude-fable-5-2

Solved 2/5 (40%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| trap | 5 | 40% | 40% | 0.93 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| m | 5 | 40% | 40% | 0.93 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| trap-m/0 | no | 0.87 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2] survives (8 neighbours) |
| trap-m/10 | no | 0.89 | one step of a Life-like automaton: empty cell with [3, 4] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/11 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [3] survives (8 neighbours) |
| trap-m/2 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 3] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/9 | no | 0.90 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2, 3, 4] survives (8 neighbours) |
