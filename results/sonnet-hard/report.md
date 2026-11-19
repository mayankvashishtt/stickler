# Stickler report: claude:sonnet

Solved 20/32 (62%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| 2 | 16 | 75% | 75% | 0.93 |
| 3 | 16 | 50% | 50% | 0.96 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 16 | 62% | 62% | 0.97 |
| m | 16 | 62% | 62% | 0.92 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| d2l/10 | yes | 1.00 | invert foreground and background -> mirror top-bottom |
| d2l/11 | yes | 1.00 | invert foreground and background -> mirror left-right |
| d2l/12 | yes | 1.00 | mirror top-bottom -> make left-right symmetric |
| d2l/13 | yes | 1.00 | make left-right symmetric -> single cells become 7, larger objects 2 |
| d2l/14 | yes | 1.00 | make left-right symmetric -> every cell shoots a ray down |
| d2l/15 | yes | 1.00 | draw a colour-1 box around each object -> surround objects with colour 8 |
| d2l/16 | yes | 1.00 | surround objects with colour 5 -> tile 2x2 with mirrored copies |
| d2l/17 | no | 0.99 | invert foreground and background -> make left-right symmetric |
| d2m/10 | no | 0.99 | invert foreground and background -> surround objects with colour 2 |
| d2m/11 | yes | 1.00 | join same-coloured cells in a row/column with colour 3 -> mirror left-right |
| d2m/12 | yes | 1.00 | rotate 90 degrees clockwise -> fill enclosed holes with colour 8 |
| d2m/13 | no | 0.96 | join same-coloured cells in a row/column with colour 8 -> mirror top-bottom |
| d2m/14 | no | 0.00 | tile 2x2 with mirrored copies -> output a bar of colour 2, one cell per object |
| d2m/15 | yes | 1.00 | every cell shoots a ray down -> rotate 90 degrees clockwise |
| d2m/16 | yes | 1.00 | make left-right symmetric -> scale up 3x |
| d2m/17 | yes | 1.00 | shift by (2,0) with wrap-around -> rotate 180 degrees |
| d3l/10 | yes | 1.00 | everything falls up -> shift by (-1,0) with wrap-around -> every cell shoots a ray up |
| d3l/11 | no | 0.99 | remove isolated single cells -> transpose (swap rows and columns) -> shift by (0,-1) with wrap-around |
| d3l/12 | yes | 1.00 | keep only the most common colour -> make left-right symmetric -> shift by (-1,0) with wrap-around |
| d3l/13 | no | 0.87 | join same-coloured cells in a row/column with colour 4 -> every cell shoots a ray left -> everything falls down |
| d3l/14 | no | 0.83 | tile 2x2 with mirrored copies -> shift by (0,2) with wrap-around -> single cells become 5, larger objects 9 |
| d3l/15 | yes | 1.00 | rotate 180 degrees -> transpose (swap rows and columns) -> draw a colour-2 box around each object |
| d3l/16 | no | 0.93 | join same-coloured cells in a row/column with colour 4 -> remove isolated single cells -> mirror top-bottom |
| d3l/17 | no | 0.96 | everything falls right -> mirror left-right -> keep only the most common colour |
| d3m/10 | yes | 1.00 | draw a colour-8 box around each object -> mirror top-bottom -> scale up 2x |
| d3m/11 | yes | 1.00 | join same-coloured cells in a row/column with colour 3 -> mirror top-bottom -> remove isolated single cells |
| d3m/12 | yes | 1.00 | every cell shoots a ray down -> tile 2x2 with mirrored copies -> transpose (swap rows and columns) |
| d3m/13 | yes | 1.00 | scale up 2x -> transpose (swap rows and columns) -> mirror top-bottom |
| d3m/14 | yes | 1.00 | scale up 3x -> mirror top-bottom -> everything falls right |
| d3m/15 | no | 0.98 | everything falls right -> surround objects with colour 1 -> draw a colour-8 box around each object |
| d3m/16 | no | 0.82 | mirror left-right -> single cells become 3, larger objects 6 -> everything falls down |
| d3m/17 | no | 0.99 | fill enclosed holes with colour 8 -> surround objects with colour 9 -> mirror left-right |
