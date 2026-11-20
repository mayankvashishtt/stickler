# Stickler report: claude:claude-fable-5-2

Solved 4/10 (40%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| steps5 | 10 | 40% | 40% | 0.73 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 4 | 25% | 25% | 0.85 |
| xl | 6 | 50% | 50% | 0.65 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| steps5-l/20 | yes | 1.00 | one step of a Life-like automaton: empty cell with [4, 7] live neighbours is born, live cell with [1, 2, 7] survives (8 neighbours) (applied 5 times) |
| steps5-l/21 | no | 0.96 | one step of a Life-like automaton: empty cell with [1, 7] live neighbours is born, live cell with [1, 2, 3] survives (8 neighbours) (applied 5 times) |
| steps5-l/22 | no | 0.43 | one step of a Life-like automaton: empty cell with [1, 3] live neighbours is born, live cell with [0, 2, 4, 5] survives (8 neighbours) (applied 5 times) |
| steps5-l/23 | no | 1.00 | one step of a Life-like automaton: empty cell with [1, 8] live neighbours is born, live cell with [2, 8] survives (8 neighbours) (applied 5 times) |
| steps5-xl/24 | no | 0.87 | one step of a Life-like automaton: empty cell with [1, 2, 7] live neighbours is born, live cell with [4, 5] survives (8 neighbours) (applied 5 times) |
| steps5-xl/25 | no | 0.00 | one step of a Life-like automaton: empty cell with [1, 2, 5] live neighbours is born, live cell with [2, 6] survives (8 neighbours) (applied 5 times) |
| steps5-xl/26 | yes | 1.00 | one step of a Life-like automaton: empty cell with [6, 7, 8] live neighbours is born, live cell with [2, 6] survives (8 neighbours) (applied 5 times) |
| steps5-xl/27 | yes | 1.00 | one step of a Life-like automaton: empty cell with [4] live neighbours is born, live cell with [3, 8] survives (8 neighbours) (applied 5 times) |
| steps5-xl/28 | no | 0.00 | one step of a Life-like automaton: empty cell with [2, 6] live neighbours is born, live cell with [3, 4, 7, 8] survives (8 neighbours) (applied 5 times) |
| steps5-xl/29 | yes | 1.00 | one step of a Life-like automaton: empty cell with [8] live neighbours is born, live cell with [0, 4, 5, 6] survives (8 neighbours) (applied 5 times) |

### Crashes

- steps5-xl/25: RuntimeError('model took 2 turns: it tried to use a tool')
- steps5-xl/28: RuntimeError('model took 3 turns: it tried to use a tool')
