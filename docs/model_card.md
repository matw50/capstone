# Model Card: State-Policy Trust-Region BBO Optimisation Approach

## Overview
Model name: State-Policy Trust-Region BBO Optimiser

Version: Final Week 13 results version

Type: Hybrid black-box optimisation workflow using surrogate-generated candidates, diagnostic checks, historical backtesting, and manual basin-aware blending.

Developer: Matthew Winn, as part of the Imperial Professional Certificate in Machine Learning and Artificial Intelligence capstone project.

Task: Sequentially propose query points for eight unknown maximisation functions under a limited query budget.

This is not a single trained production model. It is a documented optimisation approach that combines model-assisted candidate generation with explicit decision rules and human review.

## Intended Use
Suitable uses:
- replaying or adapting the query-selection workflow for low-data black-box optimisation
- documenting a reproducible optimisation strategy
- comparing local exploitation, recovery, and bounded exploration decisions
- demonstrating how limited-feedback optimisation can be managed with transparent rules

Avoided uses:
- automatic deployment without manual review
- claims of global optimality
- use on unrelated black-box functions without retesting assumptions
- high-stakes real-world decisions without stronger validation, uncertainty modelling, and governance

The approach is designed for a low-data, expensive-evaluation setting where each new query has high opportunity cost.

## Model Details And Strategy
The approach evolved over thirteen submitted rounds.

Early rounds used broader exploration and simple surrogate guidance:
- local visual reasoning for lower-dimensional functions
- random-forest surrogate guidance for higher-dimensional functions
- manual ranking of promising observed regions

Middle rounds shifted toward trust-region behaviour:
- anchor on historical best points when latest submissions underperformed
- exploit locally when the latest query produced a new best
- use sanity checks to avoid unsupported jumps
- add logistic regression and RBF SVM region checks as secondary evidence

Later rounds formalised the state policy:
- `momentum`: latest query set a new best, so exploit locally
- `refine`: one non-improving round, return toward the historical best
- `stagnant`: repeated non-improvement, allow one bounded alternative
- `recovery`: failed exploration or prolonged underperformance, reset to the best observed basin

By Week 12, the workflow adds an endgame overlay because only two submissions remain. Momentum and near-miss functions are protected with very small local moves, while repeated recovery failures are allowed one controlled alternative before the final round. This means the candidate generator is used even more conservatively: raw candidates provide direction and contrast, but final choices prioritise basin preservation and opportunity cost.

For Week 13, the strategy becomes fully outcome-focused because no later learning round remains. Proven monotonic trajectories are continued, narrow historical peaks are estimated locally, and uncertain functions receive bounded hypotheses derived from multiple strong observations. Broad surrogate proposals are rejected even when their acquisition scores are high, because historical backtesting and observed results consistently favour micro-local or basin-aware choices.

Candidate generation uses:
- Gaussian-process-style search for lower-dimensional functions
- local random-forest search for higher-dimensional functions
- candidate sanity checks for trust-region distance, nearest-neighbour support, and boundary behaviour
- classifier checks with logistic regression and RBF SVM
- experimental MLP surrogate checks as a caution signal
- historical backtesting to test whether raw candidates are too broad

The final submitted point is manually blended from these signals. Raw generated candidates are treated as recommendations, not automatic submissions.

## Performance
Primary metric: best observed output for each function, because all functions are maximisation tasks.

Secondary metrics and diagnostics:
- whether a weekly query created a new best
- distance to historical best
- nearest-neighbour support around a candidate
- trust-region adherence
- classifier high-region prediction
- historical backtest locality and support deltas

Final best observed outputs:

| Function | Best Output | Source |
| --- | ---: | --- |
| 1 | `4.323136325204454e-14` | Week 13 |
| 2 | `0.7729097325485852` | Week 6 |
| 3 | `-0.03004312377587237` | Week 9 |
| 4 | `-3.855201201240067` | Week 13 |
| 5 | `4303.947078248581` | Week 13 |
| 6 | `-0.47163305056036503` | Week 13 |
| 7 | `1.9502050542862732` | Week 13 |
| 8 | `9.784594749` | Week 13 |

Week 13 produced new bests for Functions 1, 4, 5, 6, 7, and 8. Proven trajectories continued to work for Functions 1, 4, 5, and 7, while tiny local refinement worked for Function 8. The midpoint between two strong Function 6 regions produced a new best. Functions 2 and 3 retained historical bests from Weeks 6 and 9 respectively.

External validation:
- COCO/BBOB was used to validate policy changes against random continuation
- the updated state-policy benchmark reached a `75.0%` development win rate and `72.9%` holdout win rate against random continuation
- a more complex ranked policy was tested and rejected because it underperformed the simpler state policy

Final benchmarking policy: COCO/BBOB was used when testing materially new policies. Routine submissions relied primarily on capstone-specific diagnostics and historical backtests.

## Assumptions And Limitations
Key assumptions:
- recent local improvement is meaningful evidence of a promising basin
- a failed wider move should usually trigger return to the best observed basin
- local trust-region refinement is preferable late in the query budget
- surrogate models are useful for candidate generation but not reliable enough to submit blindly

Limitations:
- the dataset is very small relative to the dimensionality of several functions
- the adaptive sample is biased toward known promising regions
- global optima may exist far away from sampled basins
- surrogate models may overfit or misread local noise
- manual blending improves safety but introduces researcher judgement
- historical backtests cannot evaluate unsubmitted counterfactual outputs

Potential failure modes:
- over-exploiting a local optimum
- missing a better distant region
- trusting a repeated local trend after it has already peaked
- rejecting a useful raw candidate because it appears too broad
- treating classifier or neural-network checks as more certain than the data supports

## Ethical And Responsible AI Considerations
The dataset is synthetic and does not contain human-subject or sensitive personal data. The main responsible AI concern is transparency rather than privacy.

Transparency supports:
- reproducibility of each weekly submission
- clear explanation of why raw candidates were accepted or rejected
- auditability of manual overrides
- honest documentation of negative results, such as the rejected ranked policy
- clear separation between observed outputs and inferred strategy

This model card intentionally describes the approach as a decision workflow rather than a fully autonomous optimiser. That distinction matters in real-world ML settings, where over-trusting model recommendations can lead to poor decisions when data is sparse or biased.

## Maintenance
The completed approach is maintained through the repository as a reproducible portfolio artefact.

Maintenance steps:
- preserve the recorded weekly decisions and returned outputs
- keep the scripts and dependency versions runnable
- regenerate final reports or visualisations when presentation needs change
- document any post-project methodological revisions separately from the historical challenge record
- commit changes with Git

Future improvements could include:
- structured uncertainty calibration across functions
- more systematic candidate menus per function
- improved visualisation of unexplored regions
- automated comparison of exploit, recovery, and bounded-alternative candidates
- clearer separation between model-generated candidates and human-selected final submissions
