# Week 1 Approach

## Main Principle
The main principle I used was an adaptive balance between exploitation and limited exploration. For the lower-dimensional functions, I relied mainly on exploitation by using scatter plots and local visual reasoning to refine around the best observed regions. For the higher-dimensional functions, I used a random-forest surrogate model to score candidate points and select queries that were predicted to perform well, while still allowing some variation from previously observed inputs. Overall, my heuristic was to exploit where the data showed a clear promising region and use more model-guided exploration where the structure was less interpretable.

## Lower-Dimensional Visuals
These plots show the observed data through Week 1 for Functions 1 to 4. The smaller observed datasets for Functions 1 to 3 are included directly below the plots.

### Function 1
![Function 1 Week 1 scatter](lower_dim/function_1_scatter.png)

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
```

### Function 2
![Function 2 Week 1 scatter](lower_dim/function_2_scatter.png)

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
```

### Function 3
![Function 3 Week 1 scatter](lower_dim/function_3_scatter.png)

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
```

### Function 4
![Function 4 Week 1 pairplot](lower_dim/function_4_pairplot.png)

Observed dataset size: 31 rows x 4 features. I left the full table out here because it is large enough to be harder to read than the pairplot itself.

## Most Challenging Functions
The most challenging functions were Function 1 and Function 8, but for different reasons. Function 1 was difficult because the outputs were extremely sparse, with almost all observed values close to zero, which made it hard to infer the shape of the function or identify a broader promising region. Function 8 was challenging because its eight-dimensional input space made the response surface difficult to interpret directly, even with more observations than some of the earlier functions. Function 7 was also challenging for similar reasons, though it showed a clearer standout point. Additional information that would have helped includes more observations per function, some indication of output noise, or uncertainty-aware model diagnostics to distinguish stable high-performing regions from local effects.

## Future Strategy
In future rounds, I plan to keep the same adaptive workflow but update the balance between exploitation and exploration based on the new observations. If a query improves on a promising local region, I will continue refining around that area with smaller, more exploitative moves. If a query performs worse than expected, I will increase exploration by testing a different promising region or by giving the surrogate model more freedom to search less-sampled parts of the space. As uncertainty decreases with each new observation, I expect to become more selective and locally focused for functions that show stable structure, while keeping broader exploration for the functions that remain ambiguous.
