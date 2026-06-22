# Progress Diagnostics Through Week12

This report is a lightweight pre-submission diagnostic. It does not choose queries directly; it highlights function state, recent coordinate sensitivity, and where the next round should be cautious.

## Function Summary
| Function | Best | Source | Latest | State | Read |
| --- | --- | --- | --- | --- | --- |
| 1 | 3.039989e-14 | week12 | 3.039989e-14 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x2 decrease. |
| 2 | 0.772910 | week6 | 0.657158 | recovery (6) | Reset to best basin before exploring; sensitivity says x1 increase, x2 decrease. |
| 3 | -0.030043 | week9 | -0.040371 | recovery (3) | Reset to best basin before exploring; sensitivity says x2 increase, x3 decrease. |
| 4 | -3.865447 | week12 | -3.865447 | momentum (0) | Exploit locally; consider moving mainly along x2 increase, x3 increase. |
| 5 | 4.158027e+03 | week12 | 4.158027e+03 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x2 increase. |
| 6 | -0.478307 | week9 | -0.479135 | recovery (3) | Reset to best basin before exploring; sensitivity says x1 decrease, x3 increase. |
| 7 | 1.923092 | week12 | 1.923092 | momentum (0) | Exploit locally; consider moving mainly along x2 decrease, x5 increase. |
| 8 | 9.784445 | week12 | 9.784445 | momentum (0) | Exploit locally; consider moving mainly along x6 decrease, x8 decrease. |

## Coordinate Sensitivity
| Function | Top Coordinate Signals |
| --- | --- |
| 1 | x1 decrease (0.000), x2 decrease (0.000) |
| 2 | x1 increase (0.287), x2 decrease (0.223) |
| 3 | x2 increase (0.082), x3 decrease (0.070), x1 increase (0.058) |
| 4 | x2 increase (0.006), x3 increase (0.006), x4 increase (0.006) |
| 5 | x1 decrease (0.065), x2 increase (0.065), x3 increase (0.065) |
| 6 | x1 decrease (0.432), x3 increase (0.423), x4 decrease (0.387) |
| 7 | x2 decrease (0.020), x5 increase (0.020), x3 increase (0.020) |
| 8 | x6 decrease (0.005), x8 decrease (0.004), x5 increase (0.004) |

## Notes
- `State` follows the current capstone policy language: momentum, refine, stagnant, or recovery.
- Coordinate signals are estimated from recent weekly moves only, so they should guide manual review rather than override observed best basins.
- A positive coordinate score means recent increases in that coordinate tended to align with better outputs; a negative score means decreases tended to align with better outputs.
