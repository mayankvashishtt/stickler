# Stickler report: claude:haiku

Solved 0/12 (0%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| steps3 | 12 | 0% | 0% | 0.15 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 4 | 0% | 0% | 0.00 |
| m | 8 | 0% | 0% | 0.22 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| steps3-l/10 | no | 0.00 | one step of a Life-like automaton: empty cell with [3, 6] live neighbours is born, live cell with [0, 2, 5, 6] survives (8 neighbours) (applied 3 times) |
| steps3-l/11 | no | 0.00 | one step of a Life-like automaton: empty cell with [3, 5] live neighbours is born, live cell with [2, 8] survives (8 neighbours) (applied 3 times) |
| steps3-l/8 | no | 0.00 | one step of a Life-like automaton: empty cell with [1, 4, 8] live neighbours is born, live cell with [2, 6] survives (8 neighbours) (applied 3 times) |
| steps3-l/9 | no | 0.00 | one step of a Life-like automaton: empty cell with [5, 8] live neighbours is born, live cell with [0, 3, 4, 7] survives (8 neighbours) (applied 3 times) |
| steps3-m/0 | no | 0.00 | one step of a Life-like automaton: empty cell with [2, 5] live neighbours is born, live cell with [3, 4, 6] survives (8 neighbours) (applied 3 times) |
| steps3-m/1 | no | 0.80 | one step of a Life-like automaton: empty cell with [3] live neighbours is born, live cell with [1, 3, 7, 8] survives (8 neighbours) (applied 3 times) |
| steps3-m/2 | no | 0.00 | one step of a Life-like automaton: empty cell with [3, 4] live neighbours is born, live cell with [0, 6] survives (8 neighbours) (applied 3 times) |
| steps3-m/3 | no | 0.00 | one step of a Life-like automaton: empty cell with [3, 4] live neighbours is born, live cell with [1, 4] survives (8 neighbours) (applied 3 times) |
| steps3-m/4 | no | 0.00 | one step of a Life-like automaton: empty cell with [2, 4, 8] live neighbours is born, live cell with [1, 4] survives (8 neighbours) (applied 3 times) |
| steps3-m/5 | no | 0.98 | one step of a Life-like automaton: empty cell with [5] live neighbours is born, live cell with [1, 5] survives (8 neighbours) (applied 3 times) |
| steps3-m/6 | no | 0.00 | one step of a Life-like automaton: empty cell with [4, 6] live neighbours is born, live cell with [3, 6] survives (8 neighbours) (applied 3 times) |
| steps3-m/7 | no | 0.00 | one step of a Life-like automaton: empty cell with [6] live neighbours is born, live cell with [1, 5, 7] survives (8 neighbours) (applied 3 times) |

### Crashes

- steps3-l/11: RuntimeError('model took 2 turns: it tried to use a tool')
