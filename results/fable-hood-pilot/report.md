# Stickler report: claude:claude-fable-5-2

Solved 7/8 (88%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| hood | 8 | 88% | 88% | 1.00 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 4 | 75% | 75% | 1.00 |
| m | 4 | 100% | 100% | 1.00 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| hood-l/0 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (knight): empty cell with [3, 8] live neighbours is born, live cell with [3] survives |
| hood-l/1 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (vline): empty cell with [3] live neighbours is born, live cell with [0, 1, 3] survives |
| hood-l/2 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (knight): empty cell with [2, 8] live neighbours is born, live cell with [6, 7] survives |
| hood-l/3 | no | 1.00 | Life-like automaton on a hidden neighbourhood (knight): empty cell with [3, 7] live neighbours is born, live cell with [7, 8] survives |
| hood-m/0 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (hline): empty cell with [4] live neighbours is born, live cell with [2, 4] survives |
| hood-m/1 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (knight): empty cell with [5, 6] live neighbours is born, live cell with [5, 6, 8] survives |
| hood-m/2 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (n4): empty cell with [1, 2] live neighbours is born, live cell with [1, 4] survives |
| hood-m/3 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (n4): empty cell with [2] live neighbours is born, live cell with [1, 3, 4] survives |
