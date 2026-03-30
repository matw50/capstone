# Week 3 Notes

## Summary
Week 3 starts from the raw trust-region candidates in `candidates.json`, but the final submission is a blended set based on manual sanity checks and the Week 1 to Week 2 convergence curves.

## Lower-Dimensional Visuals
These plots show the accumulated observed data through Week 2 for Functions 1 to 4. The smaller observed datasets for Functions 1 to 3 are included directly below the plots.

### Function 1
![Function 1 Week 3 scatter](lower_dim/function_1_scatter.png)

Observed data through Week 2:
```text
1  [0.319404, 0.762959] -> 1.3226770395454077e-79
2  [0.574329, 0.879898] -> 1.0330782375230975e-46
3  [0.731024, 0.733000] -> 7.710875114502849e-16
4  [0.840353, 0.264732] -> 3.341771007676023e-124
5  [0.650114, 0.681526] -> -0.0036060626443634764
6  [0.410437, 0.147554] -> -2.1592490357331095e-54
7  [0.312691, 0.078723] -> -2.0890932702320842e-91
8  [0.683418, 0.861057] -> 2.5350011535584046e-40
9  [0.082507, 0.403488] -> 3.6067711901420254e-81
10 [0.883890, 0.582254] -> 6.229856468168659e-48
11 [0.750000, 0.740000] -> -9.555047198348835e-21
12 [0.735000, 0.770000] -> -1.1791010396339067e-22
```

### Function 2
![Function 2 Week 3 scatter](lower_dim/function_2_scatter.png)

Observed data through Week 2:
```text
1  [0.665800, 0.123969] -> 0.5389961189269181
2  [0.877791, 0.778628] -> 0.42058623962798264
3  [0.142699, 0.349005] -> -0.06562362443733738
4  [0.845275, 0.711120] -> 0.293992912410866
5  [0.454647, 0.290455] -> 0.2149645101004509
6  [0.577713, 0.771973] -> 0.023105549798190586
7  [0.438166, 0.685018] -> 0.24461934400448035
8  [0.341750, 0.028698] -> 0.0387490151561584
9  [0.338648, 0.213867] -> -0.013857618149729824
10 [0.702637, 0.926564] -> 0.6112052157614438
11 [0.740000, 0.880000] -> 0.4507276047939478
12 [0.700000, 0.930000] -> 0.5879458606326573
```

### Function 3
![Function 3 Week 3 scatter](lower_dim/function_3_scatter.png)

Observed data through Week 2:
```text
1  [0.171525, 0.343917, 0.248737] -> -0.11212220046256897
2  [0.242114, 0.644074, 0.272433] -> -0.08796286022736445
3  [0.534906, 0.398501, 0.173389] -> -0.111414654295324
4  [0.492581, 0.611593, 0.340176] -> -0.034835313350078584
5  [0.134622, 0.219917, 0.458206] -> -0.04800758439218157
6  [0.345523, 0.941360, 0.269363] -> -0.11062091307282658
7  [0.151837, 0.439991, 0.990882] -> -0.3989255131463011
8  [0.645503, 0.397143, 0.919771] -> -0.11386851478863991
9  [0.746912, 0.284196, 0.226300] -> -0.13146060864136055
10 [0.170477, 0.697032, 0.149169] -> -0.09418956091057398
11 [0.220549, 0.297825, 0.343555] -> -0.04694740582651916
12 [0.666014, 0.671985, 0.246295] -> -0.10596503573558178
13 [0.046809, 0.231360, 0.770618] -> -0.11804825644688696
14 [0.600097, 0.725136, 0.066089] -> -0.036377828071632486
15 [0.965995, 0.861120, 0.566829] -> -0.05675837155397648
16 [0.550000, 0.680000, 0.220000] -> -0.13856523089457012
17 [0.505000, 0.715000, 0.315000] -> -0.05560582825392717
```

### Function 4
![Function 4 Week 3 pairplot](lower_dim/function_4_pairplot.png)

Observed dataset size through Week 2: 32 rows x 4 features. I left the full table out here because the pairplot is the more useful summary at this size.

## Convergence View
Convergence plots were generated in `week3/convergence/` for each function plus a combined panel. These plots were used as a quick visual check on whether recent local moves were improving, flattening out, or moving away from the best historical basin.

The plots show:
- blue line: observed outputs by evaluation order
- red line: best-so-far output
- green markers: submitted weekly queries (`W1`, `W2`)
- gold star: current best observed point

### Combined View
![All functions convergence](convergence/all_functions_convergence.png)

### Function 1
![Function 1 convergence](convergence/function_1_convergence.png)

### Function 2
![Function 2 convergence](convergence/function_2_convergence.png)

### Function 3
![Function 3 convergence](convergence/function_3_convergence.png)

### Function 4
![Function 4 convergence](convergence/function_4_convergence.png)

### Function 5
![Function 5 convergence](convergence/function_5_convergence.png)

### Function 6
![Function 6 convergence](convergence/function_6_convergence.png)

### Function 7
![Function 7 convergence](convergence/function_7_convergence.png)

### Function 8
![Function 8 convergence](convergence/function_8_convergence.png)

## Blending Rule
- Keep tight local exploitation for functions with confirmed momentum.
- Reset toward the best historical basin when the last move clearly underperformed.
- Use cautious interpolation between the best historical point and the latest improving point when the signal is positive but still below the historical best.

## Function Groups
### Cautious local refinement
Functions 1, 2, and 3 stay close to their best-known regions. Function 1 remains sparse, Function 2 is very close to the best basin, and Function 3 has improved but still has not matched the historical best.

### Reset to best-known basin
Functions 4 and 6 were pulled back toward the best historical point because Week 2 moved away from the strongest region rather than improving it.

### Momentum functions
Functions 5, 7, and 8 keep exploiting locally. Function 5 and Function 8 are clear momentum cases. Function 7 improved strongly in Week 2, but the manual blend keeps it between the historical best point and the recent recovery point rather than trusting the raw candidate at the boundary.
