# Progress Diagnostics Through Week7

This report is a lightweight pre-submission diagnostic. It does not choose queries directly; it highlights function state, recent coordinate sensitivity, and where the next round should be cautious.

## Function Summary
| Function | Best | Source | Latest | State | Read |
| --- | --- | --- | --- | --- | --- |
| 1 | 4.250433e-15 | week7 | 4.250433e-15 | momentum (0) | Exploit locally; consider moving mainly along x1 decrease, x2 decrease. |
| 2 | 0.772910 | week6 | 0.722791 | refine (1) | Return toward historical best; use x2 increase, x1 decrease cautiously. |
| 3 | -0.031402 | week6 | -0.050172 | refine (1) | Return toward historical best; use x1 decrease, x2 decrease cautiously. |
| 4 | -3.962742 | week7 | -3.962742 | momentum (0) | Exploit locally; consider moving mainly along x3 increase, x2 increase. |
| 5 | 3.273892e+03 | week7 | 3.273892e+03 | momentum (0) | Exploit locally; consider moving mainly along x3 increase, x4 increase. |
| 6 | -0.499308 | week7 | -0.499308 | momentum (0) | Exploit locally; consider moving mainly along x2 increase, x5 increase. |
| 7 | 1.749176 | week7 | 1.749176 | momentum (0) | Exploit locally; consider moving mainly along x5 increase, x4 increase. |
| 8 | 9.784149 | week2 | 9.784122 | recovery (5) | Reset to best basin before exploring; sensitivity says x8 increase, x5 decrease. |

## Coordinate Sensitivity
| Function | Top Coordinate Signals |
| --- | --- |
| 1 | x1 decrease (0.000), x2 decrease (0.000) |
| 2 | x2 increase (0.306), x1 decrease (0.301) |
| 3 | x1 decrease (0.037), x2 decrease (0.034), x3 increase (0.030) |
| 4 | x3 increase (0.777), x2 increase (0.740), x4 increase (0.646) |
| 5 | x3 increase (0.176), x4 increase (0.154), x2 increase (0.154) |
| 6 | x2 increase (0.754), x5 increase (0.648), x4 decrease (0.568) |
| 7 | x5 increase (0.321), x4 increase (0.284), x1 increase (0.267) |
| 8 | x8 increase (0.184), x5 decrease (0.181), x1 increase (0.168) |

## Notes
- `State` follows the current capstone policy language: momentum, refine, stagnant, or recovery.
- Coordinate signals are estimated from recent weekly moves only, so they should guide manual review rather than override observed best basins.
- A positive coordinate score means recent increases in that coordinate tended to align with better outputs; a negative score means decreases tended to align with better outputs.
