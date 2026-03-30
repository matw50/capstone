# Week 2 Notes

## Summary
The Week 2 candidates were generated using the trust-region query script and then manually reviewed before selecting the final submission set.

## Lower-Dimensional Visuals
These plots show the accumulated data through Week 2 for Functions 1 to 4. The smaller observed datasets for Functions 1 to 3 are included directly below the plots.

### Function 1
![Function 1 Week 2 scatter](lower_dim/function_1_scatter.png)

Observed data:
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
![Function 2 Week 2 scatter](lower_dim/function_2_scatter.png)

Observed data:
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
![Function 3 Week 2 scatter](lower_dim/function_3_scatter.png)

Observed data:
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
![Function 4 Week 2 pairplot](lower_dim/function_4_pairplot.png)

Observed dataset size: 32 rows x 4 features. I left the full table out here because the pairplot is the more useful summary at this size.

## Why Manual Overrides Were Used
The raw script output was not used unchanged for every function. The main reason is that the remaining query budget is limited, so broad or unstable jumps are harder to justify at this stage.

For lower-dimensional functions, the Gaussian Process suggestions were inspected for whether they stayed close enough to the best historical basin. For higher-dimensional functions, the Random Forest trust-region suggestions were used more directly when they remained local and consistent with the strongest observed region.

## Functions Where the Script Was Overridden
### Functions 1, 2, and 3
The raw Gaussian Process outputs were judged too aggressive or too far from the most credible historical region, so they were replaced with more conservative local refinements.

### Function 4
The script output was considered plausible and was kept with only slight rounding.

### Functions 5, 6, and 8
The script output aligned well with the current best region and was used directly.

### Function 7
The script output stayed near the standout historical best basin, so it was kept in spirit but rounded into a cleaner local move.

## Working Principle
The Week 2 submission follows a trust-region strategy:
- exploit tightly where Week 1 improved performance
- refine cautiously where Week 1 was close but not better
- return to the best historical region where Week 1 clearly underperformed

This reflects a more sample-efficient strategy for the later rounds of the capstone project.
