# Progress Diagnostics Through Week9

This report is a lightweight pre-submission diagnostic. It does not choose queries directly; it highlights function state, recent coordinate sensitivity, and where the next round should be cautious.

## Function Summary
| Function | Best | Source | Latest | State | Read |
| --- | --- | --- | --- | --- | --- |
| 1 | 1.033647e-14 | week9 | 1.033647e-14 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x2 decrease. |
| 2 | 0.772910 | week6 | 0.580957 | recovery (3) | Reset to best basin before exploring; sensitivity says x2 decrease, x1 decrease. |
| 3 | -0.030043 | week9 | -0.030043 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x3 decrease. |
| 4 | -3.914242 | week9 | -3.914242 | momentum (0) | Exploit locally; consider moving mainly along x4 increase, x1 increase. |
| 5 | 3.611736e+03 | week9 | 3.611736e+03 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x2 increase. |
| 6 | -0.478307 | week9 | -0.478307 | momentum (0) | Exploit locally; consider moving mainly along x2 increase, x5 increase. |
| 7 | 1.825832 | week9 | 1.825832 | momentum (0) | Exploit locally; consider moving mainly along x2 decrease, x5 increase. |
| 8 | 9.784149 | week2 | 9.784077 | recovery (7) | Reset to best basin before exploring; sensitivity says x3 decrease, x7 increase. |

## Coordinate Sensitivity
| Function | Top Coordinate Signals |
| --- | --- |
| 1 | x1 decrease (0.000), x2 decrease (0.000) |
| 2 | x2 decrease (0.081), x1 decrease (0.016) |
| 3 | x1 decrease (0.014), x3 decrease (0.007), x2 decrease (0.000) |
| 4 | x4 increase (0.027), x1 increase (0.021), x2 decrease (0.014) |
| 5 | x1 decrease (0.073), x2 increase (0.073), x3 increase (0.073) |
| 6 | x2 increase (0.643), x5 increase (0.641), x3 increase (0.573) |
| 7 | x2 decrease (0.025), x5 increase (0.025), x3 increase (0.025) |
| 8 | x3 decrease (0.021), x7 increase (0.021), x4 decrease (0.021) |

## Notes
- `State` follows the current capstone policy language: momentum, refine, stagnant, or recovery.
- Coordinate signals are estimated from recent weekly moves only, so they should guide manual review rather than override observed best basins.
- A positive coordinate score means recent increases in that coordinate tended to align with better outputs; a negative score means decreases tended to align with better outputs.
