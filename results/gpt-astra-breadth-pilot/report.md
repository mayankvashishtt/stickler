# Stickler report: codex:gpt-6.2-astra

Solved 40/40 (100%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| border | 8 | 100% | 100% | 1.00 |
| gravity | 8 | 100% | 100% | 1.00 |
| mirror | 8 | 100% | 100% | 1.00 |
| rays | 8 | 100% | 100% | 1.00 |
| tiling | 8 | 100% | 100% | 1.00 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 20 | 100% | 100% | 1.00 |
| m | 20 | 100% | 100% | 1.00 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| border-l/0 | yes | 1.00 | recolour each shape by 'touches the edge': False -> 2, True -> 7 |
| border-l/1 | yes | 1.00 | recolour each shape by 'touches the edge': False -> 8, True -> 9 |
| border-l/2 | yes | 1.00 | recolour each shape by 'touches the edge': False -> 6, True -> 2 |
| border-l/3 | yes | 1.00 | recolour each shape by 'touches the edge': False -> 8, True -> 1 |
| border-m/0 | yes | 1.00 | recolour each shape by 'touches the edge': False -> 1, True -> 3 |
| border-m/1 | yes | 1.00 | recolour each shape by 'touches the edge': False -> 1, True -> 9 |
| border-m/2 | yes | 1.00 | recolour each shape by 'touches the edge': False -> 4, True -> 7 |
| border-m/3 | yes | 1.00 | recolour each shape by 'touches the edge': False -> 5, True -> 6 |
| gravity-l/0 | yes | 1.00 | every coloured square falls down as far as it can; colour 4 stays where it is and blocks the others |
| gravity-l/1 | yes | 1.00 | every coloured square falls up as far as it can; colour 2 stays where it is and blocks the others |
| gravity-l/2 | yes | 1.00 | every coloured square falls right as far as it can; colour 9 stays where it is and blocks the others |
| gravity-l/3 | yes | 1.00 | every coloured square falls left as far as it can; colour 6 stays where it is and blocks the others |
| gravity-m/0 | yes | 1.00 | every coloured square falls up as far as it can; colour 2 stays where it is and blocks the others |
| gravity-m/1 | yes | 1.00 | every coloured square falls up as far as it can; colour 2 stays where it is and blocks the others |
| gravity-m/2 | yes | 1.00 | every coloured square falls down as far as it can; colour 8 stays where it is and blocks the others |
| gravity-m/3 | yes | 1.00 | every coloured square falls up as far as it can; colour 3 stays where it is and blocks the others |
| mirror-l/0 | yes | 1.00 | the picture is symmetric (quarter-turn); repaint every square of colour 6 from its mirror image |
| mirror-l/1 | yes | 1.00 | the picture is symmetric (quarter-turn); repaint every square of colour 2 from its mirror image |
| mirror-l/2 | yes | 1.00 | the picture is symmetric (both mirrors); repaint every square of colour 5 from its mirror image |
| mirror-l/3 | yes | 1.00 | the picture is symmetric (half-turn); repaint every square of colour 4 from its mirror image |
| mirror-m/0 | yes | 1.00 | the picture is symmetric (both mirrors); repaint every square of colour 5 from its mirror image |
| mirror-m/1 | yes | 1.00 | the picture is symmetric (quarter-turn); repaint every square of colour 7 from its mirror image |
| mirror-m/2 | yes | 1.00 | the picture is symmetric (quarter-turn); repaint every square of colour 6 from its mirror image |
| mirror-m/3 | yes | 1.00 | the picture is symmetric (both mirrors); repaint every square of colour 9 from its mirror image |
| rays-l/0 | yes | 1.00 | each single square draws a line to the edge, stopping at anything in the way: 1 shoots down-right, 5 shoots right, 7 shoots left |
| rays-l/1 | yes | 1.00 | each single square draws a line to the edge, stopping at anything in the way: 4 shoots right, 9 shoots down-right |
| rays-l/2 | yes | 1.00 | each single square draws a line to the edge, stopping at anything in the way: 3 shoots down, 4 shoots up-left |
| rays-l/3 | yes | 1.00 | each single square draws a line to the edge, stopping at anything in the way: 1 shoots up, 9 shoots down-right |
| rays-m/0 | yes | 1.00 | each single square draws a line to the edge, stopping at anything in the way: 7 shoots up-left, 9 shoots down-left |
| rays-m/1 | yes | 1.00 | each single square draws a line to the edge, stopping at anything in the way: 3 shoots down-right, 4 shoots right, 5 shoots up |
| rays-m/2 | yes | 1.00 | each single square draws a line to the edge, stopping at anything in the way: 4 shoots up-right, 6 shoots up-right |
| rays-m/3 | yes | 1.00 | each single square draws a line to the edge, stopping at anything in the way: 4 shoots left, 8 shoots left |
| tiling-l/0 | yes | 1.00 | the picture repeats every 2 rows and 3 columns; fill the empty squares |
| tiling-l/1 | yes | 1.00 | the picture repeats every 4 rows and 4 columns; fill the empty squares |
| tiling-l/2 | yes | 1.00 | the picture repeats every 4 rows and 3 columns; fill the empty squares |
| tiling-l/3 | yes | 1.00 | the picture repeats every 4 rows and 5 columns; fill the empty squares |
| tiling-m/0 | yes | 1.00 | the picture repeats every 5 rows and 2 columns; fill the empty squares |
| tiling-m/1 | yes | 1.00 | the picture repeats every 5 rows and 4 columns; fill the empty squares |
| tiling-m/2 | yes | 1.00 | the picture repeats every 5 rows and 4 columns; fill the empty squares |
| tiling-m/3 | yes | 1.00 | the picture repeats every 3 rows and 4 columns; fill the empty squares |
