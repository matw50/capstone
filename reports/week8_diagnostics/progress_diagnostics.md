# Progress Diagnostics Through Week8

This report is a lightweight pre-submission diagnostic. It does not choose queries directly; it highlights function state, recent coordinate sensitivity, and where the next round should be cautious.

## Function Summary
| Function | Best | Source | Latest | State | Read |
| --- | --- | --- | --- | --- | --- |
| 1 | 7.158418e-15 | week8 | 7.158418e-15 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x2 decrease. |
| 2 | 0.772910 | week6 | 0.666645 | stagnant (2) | Compare a local point against one bounded alternative; sensitivity says x2 increase, x1 decrease. |
| 3 | -0.031402 | week6 | -0.037502 | stagnant (2) | Compare a local point against one bounded alternative; sensitivity says x1 decrease, x2 decrease. |
| 4 | -3.936865 | week8 | -3.936865 | momentum (0) | Exploit locally; consider moving mainly along x4 increase, x1 increase. |
| 5 | 3.439429e+03 | week8 | 3.439429e+03 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x2 increase. |
| 6 | -0.499308 | week7 | -0.531829 | refine (1) | Return toward historical best; use x5 increase, x2 increase cautiously. |
| 7 | 1.788580 | week8 | 1.788580 | momentum (0) | Exploit locally; consider moving mainly along x2 decrease, x5 increase. |
| 8 | 9.784149 | week2 | 9.783938 | recovery (6) | Reset to best basin before exploring; sensitivity says x8 increase, x5 decrease. |

## Coordinate Sensitivity
| Function | Top Coordinate Signals |
| --- | --- |
| 1 | x1 decrease (0.000), x2 decrease (0.000) |
| 2 | x2 increase (0.331), x1 decrease (0.304) |
| 3 | x1 decrease (0.016), x2 decrease (0.012), x3 increase (0.004) |
| 4 | x4 increase (0.080), x1 increase (0.065), x2 decrease (0.020) |
| 5 | x1 decrease (0.076), x2 increase (0.076), x3 increase (0.076) |
| 6 | x5 increase (0.745), x2 increase (0.739), x4 decrease (0.610) |
| 7 | x2 decrease (0.026), x5 increase (0.026), x4 increase (0.026) |
| 8 | x8 increase (0.146), x5 decrease (0.139), x1 increase (0.109) |

## Notes
- `State` follows the current capstone policy language: momentum, refine, stagnant, or recovery.
- Coordinate signals are estimated from recent weekly moves only, so they should guide manual review rather than override observed best basins.
- A positive coordinate score means recent increases in that coordinate tended to align with better outputs; a negative score means decreases tended to align with better outputs.
