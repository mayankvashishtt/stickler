# Stickler report: claude:default

Solved 23/27 (85%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| 1 | 9 | 89% | 89% | 0.97 |
| 2 | 9 | 89% | 89% | 0.99 |
| 3 | 9 | 78% | 78% | 0.93 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 9 | 78% | 78% | 0.98 |
| m | 9 | 78% | 78% | 0.92 |
| s | 9 | 100% | 100% | 1.00 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| d1l/0 | yes | 1.00 | draw a colour-9 box around each object |
| d1l/1 | yes | 1.00 | surround objects with colour 2 |
| d1l/2 | yes | 1.00 | invert foreground and background |
| d1m/0 | yes | 1.00 | join same-coloured cells in a row/column with colour 1 |
| d1m/1 | no | 0.77 | surround objects with colour 7 |
| d1m/2 | yes | 1.00 | draw a colour-5 box around each object |
| d1s/0 | yes | 1.00 | output a bar of colour 3, one cell per object |
| d1s/1 | yes | 1.00 | make left-right symmetric |
| d1s/2 | yes | 1.00 | remove isolated single cells |
| d2l/0 | yes | 1.00 | everything falls left -> mirror top-bottom |
| d2l/1 | no | 0.93 | fill enclosed holes with colour 6 -> keep only the most common colour |
| d2l/2 | yes | 1.00 | rotate 180 degrees -> transpose (swap rows and columns) |
| d2m/0 | yes | 1.00 | rotate 90 degrees clockwise -> invert foreground and background |
| d2m/1 | yes | 1.00 | surround objects with colour 2 -> single cells become 2, larger objects 1 |
| d2m/2 | yes | 1.00 | rotate 90 degrees clockwise -> join same-coloured cells in a row/column with colour 8 |
| d2s/0 | yes | 1.00 | make left-right symmetric -> join same-coloured cells in a row/column with colour 6 |
| d2s/1 | yes | 1.00 | keep only the most common colour -> mirror left-right |
| d2s/2 | yes | 1.00 | surround objects with colour 9 -> shift by (0,2) with wrap-around |
| d3l/0 | yes | 1.00 | every cell shoots a ray up -> shift by (2,0) with wrap-around -> mirror left-right |
| d3l/1 | no | 0.87 | every cell shoots a ray right -> rotate 90 degrees clockwise -> keep only the most common colour |
| d3l/2 | yes | 1.00 | rotate 90 degrees clockwise -> remove isolated single cells -> single cells become 4, larger objects 9 |
| d3m/0 | yes | 1.00 | transpose (swap rows and columns) -> remove isolated single cells -> every cell shoots a ray down |
| d3m/1 | no | 0.52 | join same-coloured cells in a row/column with colour 7 -> mirror left-right -> every cell shoots a ray up |
| d3m/2 | yes | 1.00 | crop to the largest object -> scale up 2x -> rotate 90 degrees clockwise |
| d3s/0 | yes | 1.00 | make left-right symmetric -> transpose (swap rows and columns) -> make left-right symmetric |
| d3s/1 | yes | 1.00 | shift by (1,1) with wrap-around -> every cell shoots a ray left -> mirror left-right |
| d3s/2 | yes | 1.00 | scale up 2x -> everything falls left -> rotate 90 degrees clockwise |
