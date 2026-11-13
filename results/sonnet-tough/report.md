# GridForge report: claude:sonnet

Solved 11/24 (46%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| count | 8 | 12% | 12% | 0.98 |
| life | 8 | 25% | 25% | 0.91 |
| sizecolor | 8 | 100% | 100% | 1.00 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 12 | 50% | 50% | 0.98 |
| m | 12 | 42% | 42% | 0.95 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| count-l/0 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->4, 2->3, 3->9, 4->1 |
| count-l/1 | no | 0.98 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->4, 2->2, 3->8, 4->3 |
| count-l/2 | no | 0.98 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->5, 2->2, 3->7, 4->6 |
| count-l/3 | no | 0.98 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->3, 2->8, 3->1, 4->2 |
| count-m/0 | no | 0.95 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->3, 2->2, 3->9, 4->6 |
| count-m/1 | no | 0.99 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->3, 2->4, 3->6, 4->9 |
| count-m/2 | no | 0.99 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->5, 2->4, 3->3, 4->7 |
| count-m/3 | no | 0.97 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->3, 2->6, 3->8, 4->4 |
| life-l/0 | no | 0.96 | one step of a Life-like automaton: empty cell with [4, 8] live neighbours is born, live cell with [3, 4, 8] survives (8 neighbours) |
| life-l/1 | no | 0.88 | one step of a Life-like automaton: empty cell with [3, 5] live neighbours is born, live cell with [0, 1, 4, 7] survives (8 neighbours) |
| life-l/2 | yes | 1.00 | one step of a Life-like automaton: empty cell with [8] live neighbours is born, live cell with [0, 4] survives (8 neighbours) |
| life-l/3 | no | 0.99 | one step of a Life-like automaton: empty cell with [7, 8] live neighbours is born, live cell with [0, 5, 6, 7] survives (8 neighbours) |
| life-m/0 | no | 0.92 | one step of a Life-like automaton: empty cell with [2, 5] live neighbours is born, live cell with [2, 3, 6, 7] survives (8 neighbours) |
| life-m/1 | yes | 1.00 | one step of a Life-like automaton: empty cell with [5] live neighbours is born, live cell with [5, 6, 8] survives (8 neighbours) |
| life-m/2 | no | 0.99 | one step of a Life-like automaton: empty cell with [7] live neighbours is born, live cell with [3, 4, 6] survives (8 neighbours) |
| life-m/3 | no | 0.55 | one step of a Life-like automaton: empty cell with [2, 5] live neighbours is born, live cell with [3, 4, 6] survives (8 neighbours) |
| sizecolor-l/0 | yes | 1.00 | each shape is recoloured by its cell count: 1->1, 2->7, 3->7, 4->6, 5->8, 6->5 |
| sizecolor-l/1 | yes | 1.00 | each shape is recoloured by its cell count: 1->7, 2->2, 3->6, 4->8, 5->8, 6->8 |
| sizecolor-l/2 | yes | 1.00 | each shape is recoloured by its cell count: 1->9, 2->2, 3->6, 4->8, 5->6, 6->9 |
| sizecolor-l/3 | yes | 1.00 | each shape is recoloured by its cell count: 1->4, 2->5, 3->1, 4->8, 5->7, 6->6 |
| sizecolor-m/0 | yes | 1.00 | each shape is recoloured by its cell count: 1->7, 2->8, 3->3, 4->9, 5->3, 6->3 |
| sizecolor-m/1 | yes | 1.00 | each shape is recoloured by its cell count: 1->8, 2->9, 3->1, 4->8, 5->3, 6->1 |
| sizecolor-m/2 | yes | 1.00 | each shape is recoloured by its cell count: 1->4, 2->3, 3->3, 4->9, 5->3, 6->9 |
| sizecolor-m/3 | yes | 1.00 | each shape is recoloured by its cell count: 1->1, 2->7, 3->5, 4->9, 5->2, 6->2 |
