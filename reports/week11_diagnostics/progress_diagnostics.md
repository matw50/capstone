# Progress Diagnostics Through Week11

This report is a lightweight pre-submission diagnostic. It does not choose queries directly; it highlights function state, recent coordinate sensitivity, and where the next round should be cautious.

## Function Summary
| Function | Best | Source | Latest | State | Read |
| --- | --- | --- | --- | --- | --- |
| 1 | 2.129868e-14 | week11 | 2.129868e-14 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x2 decrease. |
| 2 | 0.772910 | week6 | 0.460084 | recovery (5) | Reset to best basin before exploring; sensitivity says x2 decrease, x1 increase. |
| 3 | -0.030043 | week9 | -0.030368 | stagnant (2) | Compare a local point against one bounded alternative; sensitivity says x2 increase, x3 decrease. |
| 4 | -3.878621 | week11 | -3.878621 | momentum (0) | Exploit locally; consider moving mainly along x4 increase, x1 increase. |
| 5 | 3.977521e+03 | week11 | 3.977521e+03 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x2 increase. |
| 6 | -0.478307 | week9 | -0.577899 | stagnant (2) | Compare a local point against one bounded alternative; sensitivity says x3 increase, x2 increase. |
| 7 | 1.893236 | week11 | 1.893236 | momentum (0) | Exploit locally; consider moving mainly along x2 decrease, x5 increase. |
| 8 | 9.784295 | week10 | 9.784265 | refine (1) | Return toward historical best; use x8 decrease, x5 increase cautiously. |

## Coordinate Sensitivity
| Function | Top Coordinate Signals |
| --- | --- |
| 1 | x1 decrease (0.000), x2 decrease (0.000) |
| 2 | x2 decrease (0.099), x1 increase (0.078) |
| 3 | x2 increase (0.122), x3 decrease (0.111), x1 increase (0.089) |
| 4 | x4 increase (0.007), x1 increase (0.007), x2 increase (0.006) |
| 5 | x1 decrease (0.067), x2 increase (0.067), x3 increase (0.067) |
| 6 | x3 increase (0.817), x2 increase (0.793), x5 increase (0.765) |
| 7 | x2 decrease (0.021), x5 increase (0.021), x3 increase (0.021) |
| 8 | x8 decrease (0.003), x5 increase (0.003), x6 decrease (0.002) |

## Notes
- `State` follows the current capstone policy language: momentum, refine, stagnant, or recovery.
- Coordinate signals are estimated from recent weekly moves only, so they should guide manual review rather than override observed best basins.
- A positive coordinate score means recent increases in that coordinate tended to align with better outputs; a negative score means decreases tended to align with better outputs.
