# Stickler report: codex:gpt-6.2-astra

Solved 22/22 (100%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| 2 | 1 | 100% | 100% | 1.00 |
| 3 | 4 | 100% | 100% | 1.00 |
| count | 4 | 100% | 100% | 1.00 |
| life | 12 | 100% | 100% | 1.00 |
| sizecolor | 1 | 100% | 100% | 1.00 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 9 | 100% | 100% | 1.00 |
| m | 10 | 100% | 100% | 1.00 |
| xl | 3 | 100% | 100% | 1.00 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| fix-count-l/1 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->4, 2->2, 3->8, 4->3 |
| fix-count-m/1 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->3, 2->4, 3->6, 4->9 |
| fix-count-m/2 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->5, 2->4, 3->3, 4->7 |
| fix-count-m/3 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->3, 2->6, 3->8, 4->4 |
| fix-d2m/10 | yes | 1.00 | invert foreground and background -> surround objects with colour 2 |
| fix-d3l/11 | yes | 1.00 | remove isolated single cells -> transpose (swap rows and columns) -> shift by (0,-1) with wrap-around |
| fix-d3m/10 | yes | 1.00 | draw a colour-8 box around each object -> mirror top-bottom -> scale up 2x |
| fix-d3m/15 | yes | 1.00 | everything falls right -> surround objects with colour 1 -> draw a colour-8 box around each object |
| fix-d3m/17 | yes | 1.00 | fill enclosed holes with colour 8 -> surround objects with colour 9 -> mirror left-right |
| fix-life-l/0 | yes | 1.00 | one step of a Life-like automaton: empty cell with [4, 8] live neighbours is born, live cell with [3, 4, 8] survives (8 neighbours) |
| fix-life-l/12 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 6, 8] live neighbours is born, live cell with [0, 1, 4, 8] survives (8 neighbours) |
| fix-life-l/13 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3, 5] live neighbours is born, live cell with [0, 3, 4, 5] survives (8 neighbours) |
| fix-life-l/2 | yes | 1.00 | one step of a Life-like automaton: empty cell with [8] live neighbours is born, live cell with [0, 4] survives (8 neighbours) |
| fix-life-l/3 | yes | 1.00 | one step of a Life-like automaton: empty cell with [7, 8] live neighbours is born, live cell with [0, 5, 6, 7] survives (8 neighbours) |
| fix-life-l/4 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3, 5, 8] live neighbours is born, live cell with [4, 5, 6, 7] survives (8 neighbours) |
| fix-life-l/9 | yes | 1.00 | one step of a Life-like automaton: empty cell with [4, 7, 8] live neighbours is born, live cell with [2, 3, 5, 6] survives (8 neighbours) |
| fix-life-m/1 | yes | 1.00 | one step of a Life-like automaton: empty cell with [5] live neighbours is born, live cell with [5, 6, 8] survives (8 neighbours) |
| fix-life-m/2 | yes | 1.00 | one step of a Life-like automaton: empty cell with [7] live neighbours is born, live cell with [3, 4, 6] survives (8 neighbours) |
| fix-life-xl/13 | yes | 1.00 | one step of a Life-like automaton: empty cell with [8] live neighbours is born, live cell with [1, 7] survives (8 neighbours) |
| fix-life-xl/4 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3, 8] live neighbours is born, live cell with [5, 6] survives (8 neighbours) |
| fix-life-xl/8 | yes | 1.00 | one step of a Life-like automaton: empty cell with [6] live neighbours is born, live cell with [2, 6] survives (8 neighbours) |
| fix-sizecolor-m/2 | yes | 1.00 | each shape is recoloured by its cell count: 1->4, 2->3, 3->3, 4->9, 5->3, 6->9 |
