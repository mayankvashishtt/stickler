# Stickler report: codex:gpt-6.2-sol

Solved 50/74 (68%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| 2 | 14 | 79% | 79% | 0.93 |
| 3 | 16 | 88% | 88% | 0.93 |
| count | 8 | 100% | 100% | 1.00 |
| life | 28 | 46% | 46% | 0.92 |
| sizecolor | 8 | 50% | 50% | 0.99 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 37 | 68% | 68% | 0.94 |
| m | 27 | 85% | 85% | 0.93 |
| xl | 10 | 20% | 20% | 0.98 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| count-l/0 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->4, 2->3, 3->9, 4->1 |
| count-l/1 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->4, 2->2, 3->8, 4->3 |
| count-l/2 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->5, 2->2, 3->7, 4->6 |
| count-l/3 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->3, 2->8, 3->1, 4->2 |
| count-m/0 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->3, 2->2, 3->9, 4->6 |
| count-m/1 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->3, 2->4, 3->6, 4->9 |
| count-m/2 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->5, 2->4, 3->3, 4->7 |
| count-m/3 | yes | 1.00 | each empty cell is coloured by its number of filled side-neighbours: 0->0, 1->3, 2->6, 3->8, 4->4 |
| d2l/10 | yes | 1.00 | invert foreground and background -> mirror top-bottom |
| d2l/11 | no | 1.00 | invert foreground and background -> mirror left-right |
| d2l/12 | yes | 1.00 | mirror top-bottom -> make left-right symmetric |
| d2l/13 | yes | 1.00 | make left-right symmetric -> single cells become 7, larger objects 2 |
| d2l/14 | yes | 1.00 | make left-right symmetric -> every cell shoots a ray down |
| d2l/15 | yes | 1.00 | draw a colour-1 box around each object -> surround objects with colour 8 |
| d2l/16 | yes | 1.00 | surround objects with colour 5 -> tile 2x2 with mirrored copies |
| d2m/10 | no | 0.99 | invert foreground and background -> surround objects with colour 2 |
| d2m/11 | yes | 1.00 | join same-coloured cells in a row/column with colour 3 -> mirror left-right |
| d2m/12 | yes | 1.00 | rotate 90 degrees clockwise -> fill enclosed holes with colour 8 |
| d2m/14 | no | 0.00 | tile 2x2 with mirrored copies -> output a bar of colour 2, one cell per object |
| d2m/15 | yes | 1.00 | every cell shoots a ray down -> rotate 90 degrees clockwise |
| d2m/16 | yes | 1.00 | make left-right symmetric -> scale up 3x |
| d2m/17 | yes | 1.00 | shift by (2,0) with wrap-around -> rotate 180 degrees |
| d3l/10 | no | 0.92 | everything falls up -> shift by (-1,0) with wrap-around -> every cell shoots a ray up |
| d3l/11 | yes | 1.00 | remove isolated single cells -> transpose (swap rows and columns) -> shift by (0,-1) with wrap-around |
| d3l/12 | yes | 1.00 | keep only the most common colour -> make left-right symmetric -> shift by (-1,0) with wrap-around |
| d3l/13 | yes | 1.00 | join same-coloured cells in a row/column with colour 4 -> every cell shoots a ray left -> everything falls down |
| d3l/14 | yes | 1.00 | tile 2x2 with mirrored copies -> shift by (0,2) with wrap-around -> single cells become 5, larger objects 9 |
| d3l/15 | yes | 1.00 | rotate 180 degrees -> transpose (swap rows and columns) -> draw a colour-2 box around each object |
| d3l/16 | yes | 1.00 | join same-coloured cells in a row/column with colour 4 -> remove isolated single cells -> mirror top-bottom |
| d3l/17 | yes | 1.00 | everything falls right -> mirror left-right -> keep only the most common colour |
| d3m/10 | no | 0.00 | draw a colour-8 box around each object -> mirror top-bottom -> scale up 2x |
| d3m/11 | yes | 1.00 | join same-coloured cells in a row/column with colour 3 -> mirror top-bottom -> remove isolated single cells |
| d3m/12 | yes | 1.00 | every cell shoots a ray down -> tile 2x2 with mirrored copies -> transpose (swap rows and columns) |
| d3m/13 | yes | 1.00 | scale up 2x -> transpose (swap rows and columns) -> mirror top-bottom |
| d3m/14 | yes | 1.00 | scale up 3x -> mirror top-bottom -> everything falls right |
| d3m/15 | yes | 1.00 | everything falls right -> surround objects with colour 1 -> draw a colour-8 box around each object |
| d3m/16 | yes | 1.00 | mirror left-right -> single cells become 3, larger objects 6 -> everything falls down |
| d3m/17 | yes | 1.00 | fill enclosed holes with colour 8 -> surround objects with colour 9 -> mirror left-right |
| life-l/0 | no | 0.96 | one step of a Life-like automaton: empty cell with [4, 8] live neighbours is born, live cell with [3, 4, 8] survives (8 neighbours) |
| life-l/1 | no | 0.00 | one step of a Life-like automaton: empty cell with [3, 5] live neighbours is born, live cell with [0, 1, 4, 7] survives (8 neighbours) |
| life-l/10 | no | 0.00 | one step of a Life-like automaton: empty cell with [3, 7] live neighbours is born, live cell with [0, 5, 7] survives (8 neighbours) |
| life-l/11 | yes | 1.00 | one step of a Life-like automaton: empty cell with [1, 6, 7] live neighbours is born, live cell with [1, 2, 3, 5] survives (8 neighbours) |
| life-l/12 | no | 0.97 | one step of a Life-like automaton: empty cell with [2, 6, 8] live neighbours is born, live cell with [0, 1, 4, 8] survives (8 neighbours) |
| life-l/13 | no | 1.00 | one step of a Life-like automaton: empty cell with [3, 5] live neighbours is born, live cell with [0, 3, 4, 5] survives (8 neighbours) |
| life-l/2 | yes | 1.00 | one step of a Life-like automaton: empty cell with [8] live neighbours is born, live cell with [0, 4] survives (8 neighbours) |
| life-l/3 | yes | 1.00 | one step of a Life-like automaton: empty cell with [7, 8] live neighbours is born, live cell with [0, 5, 6, 7] survives (8 neighbours) |
| life-l/4 | yes | 1.00 | one step of a Life-like automaton: empty cell with [3, 5, 8] live neighbours is born, live cell with [4, 5, 6, 7] survives (8 neighbours) |
| life-l/5 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 4, 7] live neighbours is born, live cell with [1, 5] survives (8 neighbours) |
| life-l/6 | no | 1.00 | one step of a Life-like automaton: empty cell with [1, 7] live neighbours is born, live cell with [3, 4] survives (8 neighbours) |
| life-l/7 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 4] live neighbours is born, live cell with [0, 2, 6, 7] survives (8 neighbours) |
| life-l/8 | yes | 1.00 | one step of a Life-like automaton: empty cell with [1, 3, 7] live neighbours is born, live cell with [2, 3, 5, 6] survives (8 neighbours) |
| life-l/9 | no | 0.99 | one step of a Life-like automaton: empty cell with [4, 7, 8] live neighbours is born, live cell with [2, 3, 5, 6] survives (8 neighbours) |
| life-m/0 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 5] live neighbours is born, live cell with [2, 3, 6, 7] survives (8 neighbours) |
| life-m/1 | yes | 1.00 | one step of a Life-like automaton: empty cell with [5] live neighbours is born, live cell with [5, 6, 8] survives (8 neighbours) |
| life-m/2 | yes | 1.00 | one step of a Life-like automaton: empty cell with [7] live neighbours is born, live cell with [3, 4, 6] survives (8 neighbours) |
| life-m/3 | yes | 1.00 | one step of a Life-like automaton: empty cell with [2, 5] live neighbours is born, live cell with [3, 4, 6] survives (8 neighbours) |
| life-xl/10 | yes | 1.00 | one step of a Life-like automaton: empty cell with [1, 4] live neighbours is born, live cell with [0, 2, 3] survives (8 neighbours) |
| life-xl/11 | no | 0.99 | one step of a Life-like automaton: empty cell with [4] live neighbours is born, live cell with [6, 8] survives (8 neighbours) |
| life-xl/12 | no | 1.00 | one step of a Life-like automaton: empty cell with [3, 6, 8] live neighbours is born, live cell with [1, 4] survives (8 neighbours) |
| life-xl/13 | yes | 1.00 | one step of a Life-like automaton: empty cell with [8] live neighbours is born, live cell with [1, 7] survives (8 neighbours) |
| life-xl/4 | no | 1.00 | one step of a Life-like automaton: empty cell with [3, 8] live neighbours is born, live cell with [5, 6] survives (8 neighbours) |
| life-xl/5 | no | 0.99 | one step of a Life-like automaton: empty cell with [2, 5, 7] live neighbours is born, live cell with [0, 4, 7] survives (8 neighbours) |
| life-xl/6 | no | 0.95 | one step of a Life-like automaton: empty cell with [2, 6] live neighbours is born, live cell with [0, 1, 4, 5] survives (8 neighbours) |
| life-xl/7 | no | 0.93 | one step of a Life-like automaton: empty cell with [1, 5] live neighbours is born, live cell with [2, 8] survives (8 neighbours) |
| life-xl/8 | no | 1.00 | one step of a Life-like automaton: empty cell with [6] live neighbours is born, live cell with [2, 6] survives (8 neighbours) |
| life-xl/9 | no | 0.99 | one step of a Life-like automaton: empty cell with [3, 5, 6] live neighbours is born, live cell with [1, 2, 7] survives (8 neighbours) |
| sizecolor-l/0 | no | 1.00 | each shape is recoloured by its cell count: 1->1, 2->7, 3->7, 4->6, 5->8, 6->5 |
| sizecolor-l/1 | no | 0.98 | each shape is recoloured by its cell count: 1->7, 2->2, 3->6, 4->8, 5->8, 6->8 |
| sizecolor-l/2 | no | 0.96 | each shape is recoloured by its cell count: 1->9, 2->2, 3->6, 4->8, 5->6, 6->9 |
| sizecolor-l/3 | yes | 1.00 | each shape is recoloured by its cell count: 1->4, 2->5, 3->1, 4->8, 5->7, 6->6 |
| sizecolor-m/0 | yes | 1.00 | each shape is recoloured by its cell count: 1->7, 2->8, 3->3, 4->9, 5->3, 6->3 |
| sizecolor-m/1 | no | 0.99 | each shape is recoloured by its cell count: 1->8, 2->9, 3->1, 4->8, 5->3, 6->1 |
| sizecolor-m/2 | yes | 1.00 | each shape is recoloured by its cell count: 1->4, 2->3, 3->3, 4->9, 5->3, 6->9 |
| sizecolor-m/3 | yes | 1.00 | each shape is recoloured by its cell count: 1->1, 2->7, 3->5, 4->9, 5->2, 6->2 |

### Crashes

- d3m/10: TimeoutExpired(['codex', 'exec', '--json', '--skip-git-repo-check', '--ephemeral', '--ignore-user-config', '--ignore-rules', '-s', 'read-only', '-C', '/var/folders/j4/bmw357454yj8fbvhlxgclcrc0000gn/T/tmpkn58lm4r', '-c', 'web_search="disabled"', '--disable', 'apps', '--disable', 'browser_use', '--dis
- life-l/1: TimeoutExpired(['codex', 'exec', '--json', '--skip-git-repo-check', '--ephemeral', '--ignore-user-config', '--ignore-rules', '-s', 'read-only', '-C', '/var/folders/j4/bmw357454yj8fbvhlxgclcrc0000gn/T/tmp_oz_3b78', '-c', 'web_search="disabled"', '--disable', 'apps', '--disable', 'browser_use', '--dis
- life-l/10: TimeoutExpired(['codex', 'exec', '--json', '--skip-git-repo-check', '--ephemeral', '--ignore-user-config', '--ignore-rules', '-s', 'read-only', '-C', '/var/folders/j4/bmw357454yj8fbvhlxgclcrc0000gn/T/tmph_8329jv', '-c', 'web_search="disabled"', '--disable', 'apps', '--disable', 'browser_use', '--dis
