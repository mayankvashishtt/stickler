# Stickler report: codex:gpt-6.2-astra

Solved 11/12 (92%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| trap | 12 | 92% | 92% | 0.99 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| m | 12 | 92% | 92% | 0.99 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| trap-m/0 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2] survives (8 neighbours) |
| trap-m/1 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2] survives (8 neighbours) |
| trap-m/10 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3, 4] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/11 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [3] survives (8 neighbours) |
| trap-m/2 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 3] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/3 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2] survives (8 neighbours) |
| trap-m/4 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2] survives (8 neighbours) |
| trap-m/5 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 3] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/6 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 3] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/7 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2] survives (8 neighbours) |
| trap-m/8 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 3] live neighbours is born, live cell with [2, 3] survives (8 neighbours) |
| trap-m/9 | no | 0.90 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [2, 3, 4] survives (8 neighbours) |
