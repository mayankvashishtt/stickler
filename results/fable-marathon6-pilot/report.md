# Stickler report: claude:claude-fable-5-2

Solved 3/3 (100%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| steps6 | 3 | 100% | 100% | 1.00 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 3 | 100% | 100% | 1.00 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| steps6-l/40 | yes | 1.00 | one step of a Life-like automaton: empty cell with [1, 7] live neighbours is born, live cell with [0, 1, 3] survives (8 neighbours) (applied 6 times) |
| steps6-l/41 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 4] live neighbours is born, live cell with [1, 4] survives (8 neighbours) (applied 6 times) |
| steps6-l/42 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 6] live neighbours is born, live cell with [1, 2, 7] survives (8 neighbours) (applied 6 times) |
