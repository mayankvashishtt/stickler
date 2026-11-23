# Stickler: how sure are the rankings?

74 puzzles, one attempt each, 10,000 bootstrap resamples. Range = middle 95%.

| Model | Solved | 95% range |
| --- | --- | --- |
| GPT-6.2-Astra | 67 | 62 to 71 |
| Fable 5.2 | 59 | 52 to 65 |
| Opus 5.5 | 50 | 42 to 58 |
| GPT-6.2-Sol | 50 | 42 to 58 |
| Sonnet 5.5 | 32 | 24 to 40 |
| Haiku 5.5 | 30 | 22 to 38 |

Neighbours on the table, paired:

| A vs B | A minus B | 95% range | A ahead in |
| --- | --- | --- | --- |
| GPT-6.2-Astra vs Fable 5.2 | +8 | +1 to +16 | 98% of resamples |
| Fable 5.2 vs Opus 5.5 | +9 | +2 to +16 | 99% of resamples |
| Opus 5.5 vs GPT-6.2-Sol | +0 | -9 to +9 | 46% of resamples |
| GPT-6.2-Sol vs Sonnet 5.5 | +18 | +8 to +28 | 100% of resamples |
| Sonnet 5.5 vs Haiku 5.5 | +2 | -5 to +9 | 66% of resamples |

A gap is clear when its range does not include 0. One attempt per puzzle; runs repeated 3 times
would also capture a model's own run-to-run luck.
