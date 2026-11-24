# Stickler report: codex:gpt-6.2-astra

Solved 11/24 (46%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| hood | 24 | 46% | 46% | 0.98 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 12 | 50% | 50% | 0.98 |
| xl | 12 | 42% | 42% | 0.98 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| hood-l/0 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (knight): empty cell with [3, 8] live neighbours is born, live cell with [3] survives |
| hood-l/1 | no | 0.99 | Life-like automaton on a hidden neighbourhood (vline): empty cell with [3] live neighbours is born, live cell with [0, 1, 3] survives |
| hood-l/10 | no | 1.00 | Life-like automaton on a hidden neighbourhood (knight): empty cell with [2, 8] live neighbours is born, live cell with [3, 8] survives |
| hood-l/11 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (vline): empty cell with [3, 4] live neighbours is born, live cell with [0, 2] survives |
| hood-l/2 | no | 0.98 | Life-like automaton on a hidden neighbourhood (knight): empty cell with [2, 8] live neighbours is born, live cell with [6, 7] survives |
| hood-l/3 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (knight): empty cell with [3, 7] live neighbours is born, live cell with [7, 8] survives |
| hood-l/4 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (vline): empty cell with [2, 4] live neighbours is born, live cell with [0, 2] survives |
| hood-l/5 | no | 0.97 | Life-like automaton on a hidden neighbourhood (hline): empty cell with [1, 3] live neighbours is born, live cell with [0] survives |
| hood-l/6 | no | 0.93 | Life-like automaton on a hidden neighbourhood (n4): empty cell with [2, 3] live neighbours is born, live cell with [1, 4] survives |
| hood-l/7 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (diag): empty cell with [1] live neighbours is born, live cell with [1] survives |
| hood-l/8 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (n4): empty cell with [1] live neighbours is born, live cell with [2, 4] survives |
| hood-l/9 | no | 0.94 | Life-like automaton on a hidden neighbourhood (n4): empty cell with [1] live neighbours is born, live cell with [1, 3] survives |
| hood-xl/0 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (hline): empty cell with [3, 4] live neighbours is born, live cell with [0] survives |
| hood-xl/1 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (diag): empty cell with [3, 4] live neighbours is born, live cell with [0, 1] survives |
| hood-xl/10 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (diag): empty cell with [2] live neighbours is born, live cell with [0, 3, 4] survives |
| hood-xl/11 | no | 1.00 | Life-like automaton on a hidden neighbourhood (vline): empty cell with [3] live neighbours is born, live cell with [0, 3] survives |
| hood-xl/2 | no | 1.00 | Life-like automaton on a hidden neighbourhood (vline): empty cell with [4] live neighbours is born, live cell with [0, 3, 4] survives |
| hood-xl/3 | no | 1.00 | Life-like automaton on a hidden neighbourhood (hline): empty cell with [3] live neighbours is born, live cell with [3] survives |
| hood-xl/4 | no | 1.00 | Life-like automaton on a hidden neighbourhood (knight): empty cell with [4, 5] live neighbours is born, live cell with [0, 5, 8] survives |
| hood-xl/5 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (vline): empty cell with [2, 3] live neighbours is born, live cell with [0, 2, 4] survives |
| hood-xl/6 | yes | 1.00 | Life-like automaton on a hidden neighbourhood (n4): empty cell with [4] live neighbours is born, live cell with [0, 1, 4] survives |
| hood-xl/7 | no | 0.96 | Life-like automaton on a hidden neighbourhood (knight): empty cell with [3, 6] live neighbours is born, live cell with [0, 6] survives |
| hood-xl/8 | no | 0.88 | Life-like automaton on a hidden neighbourhood (knight): empty cell with [6] live neighbours is born, live cell with [0, 5] survives |
| hood-xl/9 | no | 0.90 | Life-like automaton on a hidden neighbourhood (vline): empty cell with [1, 3] live neighbours is born, live cell with [4] survives |
