# Model Card: State-Policy Trust-Region BBO Optimisation Approach

## Overview
Model name: State-Policy Trust-Region BBO Optimiser

Version: Week 12 results version

Type: Hybrid black-box optimisation workflow using surrogate-generated candidates, diagnostic checks, historical backtesting, and manual basin-aware blending.

Developer: Matthew Winn, as part of the Imperial Professional Certificate in Machine Learning and Artificial Intelligence capstone project.

Task: Sequentially propose query points for eight unknown maximisation functions under a limited query budget.

This is not a single trained production model. It is a documented optimisation approach that combines model-assisted candidate generation with explicit decision rules and human review.

## Intended Use
Suitable uses:
- proposing one next query per black-box function in the capstone challenge
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
The approach evolved over ten submitted rounds.

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

Best observed outputs through Week 12:

| Function | Best Output | Source |
| --- | ---: | --- |
| 1 | `3.039989296956165e-14` | Week 12 |
| 2 | `0.7729097325485852` | Week 6 |
| 3 | `-0.03004312377587237` | Week 9 |
| 4 | `-3.8654468306983207` | Week 12 |
| 5 | `4158.027157384591` | Week 12 |
| 6 | `-0.4783073181880428` | Week 9 |
| 7 | `1.9230918956863867` | Week 12 |
| 8 | `9.7844449115` | Week 12 |

Week 12 produced new bests for Functions 1, 4, 5, 7, and 8. Function 2's controlled alternative recovered strongly without beating the Week 6 best, while Function 6's alternative nearly matched the Week 9 best. Function 3 missed and should return to its Week 9 basin. The final round should be strongly exploitative with no broad search.

External validation:
- COCO/BBOB was used to validate policy changes against random continuation
- the updated state-policy benchmark reached a `75.0%` development win rate and `72.9%` holdout win rate against random continuation
- a more complex ranked policy was tested and rejected because it underperformed the simpler state policy

Current decision: COCO/BBOB is used only when testing a materially new policy. Weekly submissions rely primarily on capstone-specific diagnostics and historical backtests.

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
The approach is maintained through the repository.

Maintenance steps:
- update weekly results after portal feedback
- rerun progress diagnostics and historical backtests
- generate raw candidates for the next round
- run sanity, classifier, and MLP checks
- document manual blending decisions
- update README, weekly notes, and reproduction files
- commit changes with Git

Future improvements could include:
- structured uncertainty calibration across functions
- more systematic candidate menus per function
- improved visualisation of unexplored regions
- automated comparison of exploit, recovery, and bounded-alternative candidates
- clearer separation between model-generated candidates and human-selected final submissions
