# Stickler report: claude:haiku

Solved 22/24 (92%).

### By depth

| depth | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| 1 | 12 | 92% | 92% | 1.00 |
| 2 | 12 | 92% | 92% | 1.00 |

### By size

| size | n | solved | pass@1 | mean cell acc |
| --- | --- | --- | --- | --- |
| l | 8 | 100% | 100% | 1.00 |
| m | 8 | 100% | 100% | 1.00 |
| xl | 8 | 75% | 75% | 1.00 |

### Every task

| id | solved | cell acc | rule |
| --- | --- | --- | --- |
| table1-l/100 | yes | 1.00 | new column e = running total of c |
| table1-l/102 | yes | 1.00 | new column e = c + d |
| table1-l/104 | yes | 1.00 | new column e = max(b, c) |
| table1-l/106 | yes | 1.00 | new column e = a - b |
| table1-m/0 | yes | 1.00 | new column e = a - d |
| table1-m/2 | yes | 1.00 | new column e = d minus d in the row above (0 on the first row) |
| table1-m/4 | yes | 1.00 | new column e = a if c >= 50, else 0 |
| table1-m/6 | yes | 1.00 | new column e = b + c |
| table2-l/101 | yes | 1.00 | new column e = b if a >= 380, else 0 -> new column f = c - d |
| table2-l/103 | yes | 1.00 | new column e = running total of b -> new column f = e if b >= 550, else 0 |
| table2-l/105 | yes | 1.00 | new column e = running total of c -> keep only rows where e >= 6220 |
| table2-l/107 | yes | 1.00 | new column e = d if a >= 460, else 0 -> new column f = d minus d in the row above (0 on the first row) |
| table2-m/1 | yes | 1.00 | new column e = d minus d in the row above (0 on the first row) -> new column f = c + a |
| table2-m/3 | yes | 1.00 | new column e = a * d -> new column f = e minus e in the row above (0 on the first row) |
| table2-m/5 | yes | 1.00 | new column e = running total of d -> keep only rows where e < 460 |
| table2-m/7 | yes | 1.00 | new column e = d minus d in the row above (0 on the first row) -> new column f = a if e >= 1, else 0 |
| tableh1-xl/300 | yes | 1.00 | new column e = c of this row plus the two rows above |
| tableh1-xl/302 | no | 0.97 | new column e = how many rows above have a bigger b |
| tableh1-xl/304 | yes | 1.00 | new column e = how many rows above have a bigger c |
| tableh1-xl/306 | yes | 1.00 | new column e = total of d over all rows with the same a |
| tableh2-xl/301 | yes | 1.00 | new column e = rank of d (1 = largest) -> new column f = e * d |
| tableh2-xl/303 | yes | 1.00 | new column e = total of d over all rows with the same a -> new column f = running total of e |
| tableh2-xl/305 | yes | 1.00 | new column e = rank of b (1 = largest) -> new column f = b if d >= 4290, else 0 |
| tableh2-xl/307 | no | 0.99 | new column e = rank of d (1 = largest) -> new column f = e if c >= 5100, else 0 |
