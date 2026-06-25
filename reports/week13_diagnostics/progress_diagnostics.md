# Progress Diagnostics Through Week13

This report is a lightweight pre-submission diagnostic. It does not choose queries directly; it highlights function state, recent coordinate sensitivity, and where the next round should be cautious.

## Function Summary
| Function | Best | Source | Latest | State | Read |
| --- | --- | --- | --- | --- | --- |
| 1 | 4.323136e-14 | week13 | 4.323136e-14 | momentum (0) | Exploit locally; consider moving mainly along x2 decrease, x1 decrease. |
| 2 | 0.772910 | week6 | 0.591389 | recovery (7) | Reset to best basin before exploring; sensitivity says x1 increase, x2 decrease. |
| 3 | -0.030043 | week9 | -0.037394 | recovery (4) | Reset to best basin before exploring; sensitivity says x2 increase, x1 increase. |
| 4 | -3.855201 | week13 | -3.855201 | momentum (0) | Exploit locally; consider moving mainly along x4 increase, x1 increase. |
| 5 | 4.303947e+03 | week13 | 4.303947e+03 | momentum (0) | Exploit locally; consider moving mainly along x4 increase, x1 decrease. |
| 6 | -0.471633 | week13 | -0.471633 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x3 increase. |
| 7 | 1.950205 | week13 | 1.950205 | momentum (0) | Exploit locally; consider moving mainly along x2 decrease, x5 increase. |
| 8 | 9.784595 | week13 | 9.784595 | momentum (0) | Exploit locally; consider moving mainly along x8 decrease, x6 decrease. |

## Coordinate Sensitivity
| Function | Top Coordinate Signals |
| --- | --- |
| 1 | x2 decrease (0.000), x1 decrease (0.000) |
| 2 | x1 increase (0.283), x2 decrease (0.227) |
| 3 | x2 increase (0.044), x1 increase (0.043), x3 decrease (0.035) |
| 4 | x4 increase (0.005), x1 increase (0.005), x2 increase (0.005) |
| 5 | x4 increase (0.062), x1 decrease (0.060), x2 increase (0.060) |
| 6 | x1 decrease (0.275), x3 increase (0.272), x4 decrease (0.261) |
| 7 | x2 decrease (0.018), x5 increase (0.018), x3 increase (0.018) |
| 8 | x8 decrease (0.003), x6 decrease (0.003), x5 increase (0.002) |

## Notes
- `State` follows the current capstone policy language: momentum, refine, stagnant, or recovery.
- Coordinate signals are estimated from recent weekly moves only, so they should guide manual review rather than override observed best basins.
- A positive coordinate score means recent increases in that coordinate tended to align with better outputs; a negative score means decreases tended to align with better outputs.
