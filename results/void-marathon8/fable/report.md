# Stickler report: claude:claude-fable-5-2

Solved 0/10 (0%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| steps8 | 10 | 0% | 0% | 0.13 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| xl | 10 | 0% | 0% | 0.13 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| steps8-xl/30 | no | 0.56 | one step of a Life-like automaton: empty cell with [1, 4, 8] live neighbours is born, live cell with [0, 3, 7] survives (8 neighbours) (applied 8 times) |
| steps8-xl/31 | no | 0.00 | one step of a Life-like automaton: empty cell with [2, 3, 4] live neighbours is born, live cell with [0, 5, 6] survives (8 neighbours) (applied 8 times) |
| steps8-xl/32 | no | 0.00 | one step of a Life-like automaton: empty cell with [2, 5] live neighbours is born, live cell with [1, 3, 6, 7] survives (8 neighbours) (applied 8 times) |
| steps8-xl/33 | no | 0.00 | one step of a Life-like automaton: empty cell with [2, 6] live neighbours is born, live cell with [1, 3, 7] survives (8 neighbours) (applied 8 times) |
| steps8-xl/34 | no | 0.71 | one step of a Life-like automaton: empty cell with [3, 6] live neighbours is born, live cell with [0, 1, 2] survives (8 neighbours) (applied 8 times) |
| steps8-xl/35 | no | 0.00 | one step of a Life-like automaton: empty cell with [1] live neighbours is born, live cell with [1, 3, 4, 7] survives (8 neighbours) (applied 8 times) |
| steps8-xl/36 | no | 0.00 | one step of a Life-like automaton: empty cell with [1, 4, 8] live neighbours is born, live cell with [1, 7] survives (8 neighbours) (applied 8 times) |
| steps8-xl/37 | no | 0.00 | one step of a Life-like automaton: empty cell with [1, 2, 5] live neighbours is born, live cell with [0, 2, 4, 7] survives (8 neighbours) (applied 8 times) |
| steps8-xl/38 | no | 0.00 | one step of a Life-like automaton: empty cell with [2] live neighbours is born, live cell with [0, 1, 2, 7] survives (8 neighbours) (applied 8 times) |
| steps8-xl/39 | no | 0.00 | one step of a Life-like automaton: empty cell with [1, 3, 8] live neighbours is born, live cell with [0, 4, 8] survives (8 neighbours) (applied 8 times) |

### Crashes

- steps8-xl/33: RuntimeError('model took 3 turns: it tried to use a tool')
- steps8-xl/32: RuntimeError('model took 3 turns: it tried to use a tool')
- steps8-xl/37: RuntimeError('model took 3 turns: it tried to use a tool')
- steps8-xl/31: RuntimeError('model took 4 turns: it tried to use a tool')
- steps8-xl/38: RuntimeError('model took 3 turns: it tried to use a tool')
- steps8-xl/36: RuntimeError('model took 4 turns: it tried to use a tool')
- steps8-xl/35: RuntimeError('model took 3 turns: it tried to use a tool')
- steps8-xl/39: RuntimeError('model took 3 turns: it tried to use a tool')
