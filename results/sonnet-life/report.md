# GridForge report: claude:sonnet

Solved 1/20 (5%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| life | 20 | 5% | 5% | 0.77 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 10 | 0% | 0% | 0.73 |
| xl | 10 | 10% | 10% | 0.81 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| life-l/10 | no | 0.93 | one step of a Life-like automaton: empty cell with [3, 7] live neighbours is born, live cell with [0, 5, 7] survives (8 neighbours) |
| life-l/11 | no | 0.54 | one step of a Life-like automaton: empty cell with [1, 6, 7] live neighbours is born, live cell with [1, 2, 3, 5] survives (8 neighbours) |
| life-l/12 | no | 1.00 | one step of a Life-like automaton: empty cell with [2, 6, 8] live neighbours is born, live cell with [0, 1, 4, 8] survives (8 neighbours) |
| life-l/13 | no | 0.55 | one step of a Life-like automaton: empty cell with [3, 5] live neighbours is born, live cell with [0, 3, 4, 5] survives (8 neighbours) |
| life-l/4 | no | 0.62 | one step of a Life-like automaton: empty cell with [3, 5, 8] live neighbours is born, live cell with [4, 5, 6, 7] survives (8 neighbours) |
| life-l/5 | no | 0.97 | one step of a Life-like automaton: empty cell with [2, 4, 7] live neighbours is born, live cell with [1, 5] survives (8 neighbours) |
| life-l/6 | no | 0.69 | one step of a Life-like automaton: empty cell with [1, 7] live neighbours is born, live cell with [3, 4] survives (8 neighbours) |
| life-l/7 | no | 0.88 | one step of a Life-like automaton: empty cell with [2, 4] live neighbours is born, live cell with [0, 2, 6, 7] survives (8 neighbours) |
| life-l/8 | no | 0.53 | one step of a Life-like automaton: empty cell with [1, 3, 7] live neighbours is born, live cell with [2, 3, 5, 6] survives (8 neighbours) |
| life-l/9 | no | 0.64 | one step of a Life-like automaton: empty cell with [4, 7, 8] live neighbours is born, live cell with [2, 3, 5, 6] survives (8 neighbours) |
| life-xl/10 | no | 0.64 | one step of a Life-like automaton: empty cell with [1, 4] live neighbours is born, live cell with [0, 2, 3] survives (8 neighbours) |
| life-xl/11 | no | 0.99 | one step of a Life-like automaton: empty cell with [4] live neighbours is born, live cell with [6, 8] survives (8 neighbours) |
| life-xl/12 | no | 0.99 | one step of a Life-like automaton: empty cell with [3, 6, 8] live neighbours is born, live cell with [1, 4] survives (8 neighbours) |
| life-xl/13 | yes | 1.00 | one step of a Life-like automaton: empty cell with [8] live neighbours is born, live cell with [1, 7] survives (8 neighbours) |
| life-xl/4 | no | 1.00 | one step of a Life-like automaton: empty cell with [3, 8] live neighbours is born, live cell with [5, 6] survives (8 neighbours) |
| life-xl/5 | no | 0.59 | one step of a Life-like automaton: empty cell with [2, 5, 7] live neighbours is born, live cell with [0, 4, 7] survives (8 neighbours) |
| life-xl/6 | no | 0.70 | one step of a Life-like automaton: empty cell with [2, 6] live neighbours is born, live cell with [0, 1, 4, 5] survives (8 neighbours) |
| life-xl/7 | no | 0.58 | one step of a Life-like automaton: empty cell with [1, 5] live neighbours is born, live cell with [2, 8] survives (8 neighbours) |
| life-xl/8 | no | 0.98 | one step of a Life-like automaton: empty cell with [6] live neighbours is born, live cell with [2, 6] survives (8 neighbours) |
| life-xl/9 | no | 0.68 | one step of a Life-like automaton: empty cell with [3, 5, 6] live neighbours is born, live cell with [1, 2, 7] survives (8 neighbours) |
