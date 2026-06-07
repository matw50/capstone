# Progress Diagnostics Through Week10

This report is a lightweight pre-submission diagnostic. It does not choose queries directly; it highlights function state, recent coordinate sensitivity, and where the next round should be cautious.

## Function Summary
| Function | Best | Source | Latest | State | Read |
| --- | --- | --- | --- | --- | --- |
| 1 | 1.486623e-14 | week10 | 1.486623e-14 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x2 decrease. |
| 2 | 0.772910 | week6 | 0.564314 | recovery (4) | Reset to best basin before exploring; sensitivity says x2 decrease, x1 increase. |
| 3 | -0.030043 | week9 | -0.040910 | refine (1) | Return toward historical best; use x2 increase, x3 decrease cautiously. |
| 4 | -3.894853 | week10 | -3.894853 | momentum (0) | Exploit locally; consider moving mainly along x4 increase, x1 increase. |
| 5 | 3.791027e+03 | week10 | 3.791027e+03 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x2 increase. |
| 6 | -0.478307 | week9 | -0.631145 | refine (1) | Return toward historical best; use x3 increase, x2 increase cautiously. |
| 7 | 1.860769 | week10 | 1.860769 | momentum (0) | Exploit locally; consider moving mainly along x2 decrease, x5 increase. |
| 8 | 9.784295 | week10 | 9.784295 | momentum (0) | Exploit locally; consider moving mainly along x7 increase, x3 decrease. |

## Coordinate Sensitivity
| Function | Top Coordinate Signals |
| --- | --- |
| 1 | x1 decrease (0.000), x2 decrease (0.000) |
| 2 | x2 decrease (0.081), x1 increase (0.062) |
| 3 | x2 increase (0.032), x3 decrease (0.031), x1 increase (0.027) |
| 4 | x4 increase (0.011), x1 increase (0.011), x2 increase (0.007) |
| 5 | x1 decrease (0.070), x2 increase (0.070), x3 increase (0.070) |
| 6 | x3 increase (0.673), x2 increase (0.668), x5 increase (0.658) |
| 7 | x2 decrease (0.023), x5 increase (0.023), x3 increase (0.023) |
| 8 | x7 increase (0.011), x3 decrease (0.010), x4 decrease (0.010) |

## Notes
- `State` follows the current capstone policy language: momentum, refine, stagnant, or recovery.
- Coordinate signals are estimated from recent weekly moves only, so they should guide manual review rather than override observed best basins.
- A positive coordinate score means recent increases in that coordinate tended to align with better outputs; a negative score means decreases tended to align with better outputs.
