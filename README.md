# Capstone

This repository tracks data, weekly submissions, returned outputs, and helper scripts for the capstone black-box optimisation challenge.

## Programme Context
This capstone sits within the Professional Certificate in Machine Learning and Artificial Intelligence, a 25-module programme jointly developed by Imperial College Business School Executive Education and the Imperial College London Department of Computing.

The wider programme is designed to build both technical and practical capability in ML and AI. It moves from foundations, to common machine learning methods, to more advanced topics such as deep learning and generative AI. The capstone project acts as the practical culmination of that learning journey by simulating a real-world ML competition where models and optimisation strategies must be refined over time.

The programme is structured in three phases:
- Phase 1 introduces foundational ML and AI concepts and shows how they are used in data science projects.
- Phase 2 focuses on common ML methods and how they can create business value.
- Phase 3 explores advanced AI topics including deep learning and generative AI, with attention to real-world implementation.

Across the programme, the broader learning goals include:
- evaluating the feasibility of machine learning solutions for business challenges
- choosing suitable ML methods to improve predictive performance and decision-making
- analysing complex datasets with machine learning
- refining models in Python
- understanding the mathematical, probabilistic, and statistical foundations of ML and AI
- considering the real-world implications of AI, including responsible use
- understanding large language models, including architecture, scale, training, and emergent behaviour

## What Is This Challenge About?
This capstone project mimics a Bayesian optimisation-style competition in which the goal is to find the maximum of eight unknown functions, also known as black-box functions. The functions are unknown in advance, so there are no equations or direct visualisations available at the start. Instead, the challenge begins with a small amount of initial data and the task is to make informed guesses about which inputs to try next.

Each function represents a real-world style optimisation problem where evaluations are expensive or limited, such as radiation detection, robot control, or drug discovery. The goal is not to find a perfect solution immediately, but to demonstrate a thoughtful, iterative optimisation process over time.

## What Will We Do?
This project works with eight synthetic black-box functions. Each function takes an input vector and returns a single output value. The task is to identify the input values that produce the highest possible output.

Every function is a maximisation problem. The internal form of the function is hidden, so the only information available comes from observed input-output pairs.

Each function is:
- a maximisation task
- initially represented by a small set of known data points
- of increasing dimensionality, from 2D to 8D

Over time, the dataset grows as new weekly query points are submitted and their outputs are returned.

## Career Relevance
This capstone is directly relevant to my current role as a Senior Engineering Manager in online ads experimentation at Meta. A large part of experimentation work in practice involves making decisions under uncertainty, balancing exploration against exploitation, and improving systems without having full visibility into the underlying response surface in advance. That is very similar to the operating conditions in this project.

The value of the capstone is not only in the specific optimisation methods, but in the decision process it develops. It reinforces how to use limited evidence, structure iteration, sanity-check model outputs, and refine a strategy over time rather than over-trusting any single model recommendation. Those are highly transferable skills for experimentation systems, ranking, measurement, and other ML-adjacent product and platform decisions.

## Environment Setup

Install the Python dependencies with:

```bash
python3 -m pip install -r requirements.txt
```

The repository currently uses:
- `numpy` for array handling and geometric checks
- `scikit-learn` for surrogate models, classifier checks, and the experimental MLP surrogate
- `matplotlib` for convergence and low-dimensional plots

## Documentation
- [Dataset Datasheet](docs/datasheet.md): documents the motivation, composition, collection process, intended uses, distribution, and maintenance of the BBO capstone dataset.
- [Model Card](docs/model_card.md): documents the state-policy trust-region optimisation approach, intended use, performance, assumptions, limitations, and responsible AI considerations.

## Current Status
| Item | Status |
|---|---|
| Latest completed round | Week 13 results recorded |
| Next submission prepared | Challenge complete |
| Current optimisation phase | Final analysis and portfolio documentation |
| Main operating pattern | Completed adaptive trust-region workflow |
| Extra validation in latest round | Trust-region, nearest-neighbour, logistic regression, RBF SVM, experimental MLP ensemble checks, COCO/BBOB benchmarking, and historical backtesting |

## Best Results So Far
| Function | Best Output So Far | Source | Current Read |
|---|---|---|---|
| 1 | `4.323136325204454e-14` | Week 13 | Final trajectory continuation produced another new best |
| 2 | `0.7729097325485852` | Week 6 | Week 12 alternative recovered strongly but remained below the historical best |
| 3 | `-0.03004312377587237` | Week 9 | Week 12 missed; final query should return to the Week 9 basin |
| 4 | `-3.855201201240067` | Week 13 | Exact local trajectory improved through the final round |
| 5 | `4303.947078248581` | Week 13 | Strongest momentum function, improving to the boundary |
| 6 | `-0.47163305056036503` | Week 13 | Midpoint hypothesis solved the long-running recovery problem |
| 7 | `1.9502050542862732` | Week 13 | Linear local trajectory improved through the final round |
| 8 | `9.784594749` | Week 13 | Tiny sensitivity-guided refinement produced a new best |

## External Benchmarking
To sanity-check whether the current capstone policy behaves like a useful optimizer outside the course portal, I added a COCO/BBOB benchmark harness.

Benchmark framing:
- use the Week 6 style local policy
- start from `10` random initial evaluations
- allow `13` sequential guided evaluations
- compare against a random continuation baseline

Current result:
- requested dimensions: `2,3,4,5,6,8`
- actual dimensions available in standard `bbob`: `2,3,5`
- problems evaluated: `72`
- capstone policy versus random continuation: `48` wins, `17` losses, `7` ties
- win rate: `66.7%`
- final target hits: `2` for the capstone policy, `0` for random continuation

Updated state-policy result:
- concrete decision rules were added after reviewing the first benchmark run
- development benchmark on instance `1`: `54` wins, `16` losses, `2` ties
- development win rate: `75.0%`
- holdout benchmark on unseen instances `2,3,4,5`: `210` wins, `55` losses, `23` ties
- holdout win rate: `72.9%`
- interpretation: the updated rules improved the development benchmark and held up well on unseen instances, which suggests the change is not just benchmark overfitting

Ranked-policy experiment:
- I also tested a more complex ranked candidate-selection layer that compared local, wider, and second-basin candidates using surrogate score, neighbour support, alignment, and boundary checks
- smoke benchmark: ranked policy beat the state policy on `7` of `24` problems, lost on `14`, and tied on `3`
- development benchmark: ranked policy beat the state policy on `24` of `72` problems, lost on `44`, and tied on `4`
- interpretation: the ranked layer beat random continuation, but it underperformed the simpler state-policy approach, so it is documented as an explored but rejected option for current capstone submissions

Current benchmarking decision:
- COCO/BBOB is now treated as a policy-change validation tool, not a routine weekly step
- I will rerun COCO/BBOB only when introducing a materially new rule or candidate-selection policy
- the weekly default is to use capstone-specific progress diagnostics, historical backtests, sanity checks, and classifier/MLP secondary checks
- this avoids overfitting the external benchmark and keeps attention on the actual capstone response history

Artifacts:
- [Benchmark README](benchmarks/coco/README.md)
- [Benchmark Summary](benchmarks/coco/week6_style_budget13/summary.json)
- [Benchmark Results CSV](benchmarks/coco/week6_style_budget13/results.csv)
- [Benchmark Histories](benchmarks/coco/week6_style_budget13/histories.json)
- [State Policy Dev Summary](benchmarks/coco/state_policy_dev_instance1_v5/summary.json)
- [State Policy Holdout Summary](benchmarks/coco/state_policy_holdout_instances2to5_v5/summary.json)
- [Ranked Policy Smoke Summary](benchmarks/coco/ranked_smoke/summary.json)
- [Ranked Policy Dev Summary](benchmarks/coco/ranked_policy_dev_instance1/summary.json)
- [Week 7 State Policy Backtest](reports/week7_backtest/state_policy_backtest.md)
- [Week 8 Progress Diagnostics](reports/week8_diagnostics/progress_diagnostics.md)
- [Week 8 State Policy Backtest](reports/week8_backtest/state_policy_backtest.md)
- [Week 9 Progress Diagnostics](reports/week9_diagnostics/progress_diagnostics.md)
- [Week 9 State Policy Backtest](reports/week9_backtest/state_policy_backtest.md)
- [Week 10 Progress Diagnostics](reports/week10_diagnostics/progress_diagnostics.md)
- [Week 10 State Policy Backtest](reports/week10_backtest/state_policy_backtest.md)
- [Week 11 Progress Diagnostics](reports/week11_diagnostics/progress_diagnostics.md)
- [Week 11 State Policy Backtest](reports/week11_backtest/state_policy_backtest.md)
- [Week 12 Progress Diagnostics](reports/week12_diagnostics/progress_diagnostics.md)
- [Week 12 State Policy Backtest](reports/week12_backtest/state_policy_backtest.md)
- [Week 13 Progress Diagnostics](reports/week13_diagnostics/progress_diagnostics.md)
- [Week 13 State Policy Backtest](reports/week13_backtest/state_policy_backtest.md)

## Weekly Index
| Week | Status | Folder | Notes | Reproduction | Results |
|---|---|---|---|---|---|
| 1 | Completed | [week1](week1/) | [notes](week1/notes.md) | [reproduction](week1/reproduction.md) | [results](week1/results.json) |
| 2 | Completed | [week2](week2/) | [notes](week2/notes.md) | [reproduction](week2/reproduction.md) | [results](week2/results.json) |
| 3 | Completed | [week3](week3/) | [notes](week3/notes.md) | [reproduction](week3/reproduction.md) | [results](week3/results.json) |
| 4 | Completed | [week4](week4/) | [notes](week4/notes.md) | [reproduction](week4/reproduction.md) | [results](week4/results.json) |
| 5 | Completed | [week5](week5/) | [notes](week5/notes.md) | [reproduction](week5/reproduction.md) | [results](week5/results.json) |
| 6 | Completed | [week6](week6/) | [notes](week6/notes.md) | [reproduction](week6/reproduction.md) | [results](week6/results.json) |
| 7 | Completed | [week7](week7/) | [notes](week7/notes.md) | [reproduction](week7/reproduction.md) | [results](week7/results.json) |
| 8 | Completed | [week8](week8/) | [notes](week8/notes.md) | [reproduction](week8/reproduction.md) | [results](week8/results.json) |
| 9 | Completed | [week9](week9/) | [notes](week9/notes.md) | [reproduction](week9/reproduction.md) | [results](week9/results.json) |
| 10 | Completed | [week10](week10/) | [notes](week10/notes.md) | [reproduction](week10/reproduction.md) | [results](week10/results.json) |
| 11 | Completed | [week11](week11/) | [notes](week11/notes.md) | [reproduction](week11/reproduction.md) | [results](week11/results.json) |
| 12 | Completed | [week12](week12/) | [notes](week12/notes.md) | [reproduction](week12/reproduction.md) | [results](week12/results.json) |
| 13 | Completed | [week13](week13/) | [notes](week13/notes.md) | [reproduction](week13/reproduction.md) | [results](week13/results.json) |

## Reproduce Latest Round
To reproduce the final Week 13 submission from the recorded Week 12 data:

1. Generate raw candidates:
```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week12 \
  --output-file week13/candidates.json \
  --seed 42 \
  --policy-variant state
```
2. Run geometric sanity checks:
```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week12 \
  --candidate-file week13/candidates.json
```
3. Run classifier region checks:
```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week12 \
  --candidate-file week13/candidates.json \
  --svm
```
4. Run the experimental neural-net surrogate check:
```bash
/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week12 \
  --candidate-file week13/candidates.json
```
5. Apply the final-round rules in [week13/reproduction.md](week13/reproduction.md) to produce [week13/inputs.json](week13/inputs.json).
6. Re-run the same sanity, classifier, and neural-network checks on [week13/inputs.json](week13/inputs.json).

## Inputs And Outputs
Each week, the project receives one proposed input per function and later returns one scalar output per function.

Inputs:
- one query per function per round
- each query is an input vector with values constrained to the unit interval
- dimensionality increases by function, from 2D up to 8D
- the portal format is a hyphen-separated decimal string such as `0.123456-0.654321`

Outputs:
- one scalar response value for each submitted query
- the returned value acts as the performance signal used for optimisation
- larger values are better because every function is a maximisation task

Examples:
- 2D query: `0.735000-0.770000`
- 4D query: `0.576000-0.429000-0.426000-0.225000`
- 8D query: `0.076137-0.036885-0.051524-0.069041-0.640532-0.823614-0.026805-0.370276`

## Challenge Constraints
The main objective is to maximise each unknown function while working under tight information and query constraints.

Key constraints:
- the true function form is hidden
- feedback is delayed until after submission
- only one new query can be submitted per function in each round
- the total number of rounds is limited, so each query has to be used carefully
- dimensionality increases across the functions, which makes higher-dimensional search substantially harder

These constraints make the project a practical exploration versus exploitation problem rather than a standard supervised learning task.

## Lessons Learned So Far
- Raw model outputs are useful starting points, but they are not reliable enough to submit unchanged in every round.
- Trust-region logic has been much more effective than broad search once a few credible basins emerged.
- Classifier-style region checks help as supporting evidence, especially in later rounds, but should not override geometric and basin-aware sanity checks.

## Decision Log
| Week | Main Strategy | What Changed | Outcome / Interpretation | Notes And Reproduction |
|---|---|---|---|---|
| 1 | Adaptive hybrid: local visual reasoning for lower-dimensional functions, random-forest surrogate guidance for higher-dimensional functions | Started with broad exploitation plus limited exploration because only the initial observations were available | Functions 5, 6, and 8 responded well; Functions 1, 3, and 7 showed that the initial direction was not yet strong enough | [Week 1 Approach](week1/approach.md), [Week 1 Reproduction](week1/reproduction.md), [Week 1 Inputs](week1/inputs.json) |
| 2 | Trust-region strategy | Shifted to tighter local search: exploit where Week 1 improved, refine cautiously where it was close, and reset toward the best historical basin where Week 1 underperformed | The sanity checks led to a safer manual override for Function 5, which then produced the strongest Week 2 improvement | [Week 2 Approach](week2/approach.md), [Week 2 Notes](week2/notes.md), [Week 2 Reproduction](week2/reproduction.md), [Week 2 Inputs](week2/inputs.json) |
| 3 | Manually blended trust-region submission | Kept the trust-region framework but overrode unstable raw model suggestions, especially for lower-dimensional functions, using sanity checks and convergence review | Current Week 3 set is designed to stay local, avoid unjustified basin jumps, and preserve momentum where evidence is strongest | [Week 3 Notes](week3/notes.md), [Week 3 Reproduction](week3/reproduction.md), [Week 3 Inputs](week3/inputs.json) |
| 4 | Late-stage trust-region with classifier-assisted review | Added logistic-regression and SVM region checks as secondary evidence, but kept trust-region, neighbour, and boundary checks as the primary filters before blending the final submission | Week 4 produced new bests for Functions 5 and 7, confirming the hard-exploitation logic there. Function 4 improved again but did not beat the historical best, and Function 8 remained very close to its best basin. | [Week 4 Approach](week4/approach.md), [Week 4 Notes](week4/notes.md), [Week 4 Reproduction](week4/reproduction.md), [Week 4 Inputs](week4/inputs.json) |
| 5 | Historical-best anchored trust-region submission | Adapted the rule so the historical best point is the default anchor, with recent results used as directional evidence rather than automatically becoming the next search centre | Week 5 produced new bests for Functions 2, 5, and 7. Function 6 remained stalled, which led to the Week 6 correction probe. | [Week 5 Approach](week5/approach.md), [Week 5 Notes](week5/notes.md), [Week 5 Reproduction](week5/reproduction.md), [Week 5 Inputs](week5/inputs.json) |
| 6 | Historical-best anchoring with Function 6 correction | Kept the historical-best anchoring rule, but added a deliberate lower-`x2`, lower-`x3` correction probe for Function 6 after repeated near-identical local nudges failed | Week 6 produced new bests for Functions 1, 2, 3, 4, 5, and 7. Function 8 stayed very close to its historical best. Function 6 underperformed, making it the clear outlier in the round. | [Week 6 Approach](week6/approach.md), [Week 6 Notes](week6/notes.md), [Week 6 Reproduction](week6/reproduction.md), [Week 6 Inputs](week6/inputs.json) |
| 7 | Benchmark-backed state-policy with manual basin-preserving overrides | Converted the benchmark lessons into explicit `momentum`, `refine`, and `recovery` rules, then clipped raw candidates back toward proven basins when the capstone evidence was narrower than the generic benchmark suggested | Week 7 produced new bests for Functions 1, 4, 5, 6, and 7. Function 6 was the biggest strategic win because the recovery reset beat all previous observations. Functions 2 and 3 dipped, while Function 8 stayed almost exactly on its best basin. | [Week 7 Approach](week7/approach.md), [Week 7 Notes](week7/notes.md), [Week 7 Reproduction](week7/reproduction.md), [Week 7 Inputs](week7/inputs.json) |
| 8 | Backtest-informed micro-local trust-region submission | Added a true historical backtest. It showed that the raw state-policy generator is directionally useful but usually wider than the successful manual submissions, so final candidates were clipped tightly around proven basins. | Week 8 produced new bests for Functions 1, 4, 5, and 7. Functions 2, 3, 6, and 8 missed, setting up stagnant/refine/recovery handling for Week 9. | [Week 8 Approach](week8/approach.md), [Week 8 Notes](week8/notes.md), [Week 8 Reproduction](week8/reproduction.md), [Week 8 Inputs](week8/inputs.json) |
| 9 | Week 8-state-adapted blended submission | Kept micro-local exploitation for momentum functions, allowed one bounded alternative for stagnant Function 2, returned Function 6 to its Week 7 best basin, and kept Function 8 anchored near its Week 2 best. | Week 9 produced new bests for Functions 1, 3, 4, 5, 6, and 7. Function 2's bounded alternative failed, and Function 8 remains close but below its Week 2 best. | [Week 9 Approach](week9/approach.md), [Week 9 Notes](week9/notes.md), [Week 9 Reproduction](week9/reproduction.md), [Week 9 Inputs](week9/inputs.json) |
| 10 | Week 9 momentum/recovery blend | Continued micro-local exploitation for Functions 1, 3, 4, 5, 6, and 7; reset Function 2 near the Week 6 best; and kept Function 8 tightly anchored around the Week 2 best. | Week 10 produced new bests for Functions 1, 4, 5, 7, and 8. Function 8 finally beat its Week 2 best. Functions 3 and 6 missed and should return toward their Week 9 best basins. | [Week 10 Approach](week10/approach.md), [Week 10 Notes](week10/notes.md), [Week 10 Reproduction](week10/reproduction.md), [Week 10 Inputs](week10/inputs.json) |
| 11 | Week 10 micro-local momentum/refine blend | Continued tiny local exploitation for Functions 1, 4, 5, 7, and 8; reset Function 2 near the Week 6 best; returned Functions 3 and 6 toward their Week 9 best basins. | Week 11 produced new bests for Functions 1, 4, 5, and 7. Function 3 was a near miss, Function 8 was a tiny miss, and Functions 2 and 6 remain the hardest recovery/stagnant cases. | [Week 11 Notes](week11/notes.md), [Week 11 Reproduction](week11/reproduction.md), [Week 11 Inputs](week11/inputs.json) |
| 12 | Penultimate-round endgame submission | Preserved winning basins for Functions 1, 4, 5, and 7; kept Functions 3 and 8 very close to their best basins; allowed one controlled alternative for Functions 2 and 6 after repeated recovery failures. | Week 12 produced new bests for Functions 1, 4, 5, 7, and 8. Function 2 recovered strongly, Function 6 nearly matched its best, and Function 3 missed. | [Week 12 Approach](week12/approach.md), [Week 12 Notes](week12/notes.md), [Week 12 Reproduction](week12/reproduction.md), [Week 12 Inputs](week12/inputs.json) |
| 13 | Final-round exploitation | Continued proven trajectories for Functions 1, 4, 5, and 7; used a tiny sensitivity-guided step for Function 8; used local peak interpolation for Function 2; and tested bounded final hypotheses for Functions 3 and 6. | The final round produced new bests for Functions 1, 4, 5, 6, 7, and 8. The Function 6 midpoint hypothesis was the most important final-round success. | [Week 13 Approach](week13/approach.md), [Week 13 Notes](week13/notes.md), [Week 13 Reproduction](week13/reproduction.md), [Week 13 Inputs](week13/inputs.json) |

## Repository Workflow
The repository is organised to support the weekly optimisation cycle:

1. Start from the original arrays stored in `initial_data/`.
2. Scaffold or standardize the target `weekN/` folder so the core files are present.
3. Record each round of submitted points and returned outputs in that `weekN/` folder.
4. Generate appended `.npy` files for that week so the updated dataset is ready for the next round.
5. Use the helper scripts in `scripts/` to keep the workflow repeatable and organised.

## Repository Layout
- `initial_data/`: original `.npy` arrays for each function
- `week1/`: Week 1 submission, outputs, appended datasets, lower-dimensional plots, approach notes, and reproduction notes
- `week2/`: Week 2 submission, outputs, appended datasets, raw candidates, lower-dimensional plots, notes, reflections, and reproduction notes
- `week3/`: Week 3 submission, outputs, appended datasets, raw candidates, lower-dimensional plots, convergence plots, notes, and reproduction notes
- `week4/`: Week 4 submission, outputs, appended datasets, raw candidates, approach notes, and reproduction notes
- `week5/`: Week 5 submission, outputs, appended datasets, raw candidates, approach notes, and reproduction notes
- `week6/`: Week 6 submission, outputs, appended datasets, raw candidates, approach notes, and reproduction notes
- `week7/`: Week 7 completed round with submission, outputs, appended datasets, raw candidates, approach notes, and reproduction notes
- `week8/`: completed round with raw candidates, final submission, returned outputs, appended arrays, approach notes, and reproduction steps
- `week9/`: completed round with raw candidates, final submission, returned outputs, appended arrays, approach notes, and reproduction steps
- `week10/`: completed round with raw candidates, final submission, returned outputs, appended arrays, approach notes, and reproduction steps
- `week11/`: completed round with raw candidates, final submission, returned outputs, appended arrays, notes, and reproduction steps
- `week12/`: completed penultimate round with raw candidates, final submission, returned outputs, appended arrays, notes, and reproduction steps
- `week13/`: completed final round with reference candidates, final submission, returned outputs, appended arrays, notes, and reproduction steps
- `benchmarks/`: external optimizer checks, including COCO/BBOB runs against baselines
- `docs/`: datasheet and model card documentation
- `reports/`: generated diagnostic reports used before preparing later-round submissions
- `scripts/`: helper scripts for filling week folders, generating candidates, running checks, plotting views, and appending results
- `requirements.txt`: lightweight Python dependency list for reproducing the workflow
- `REPO_INVENTORY.md`: notes on the current repository structure and script usage

## Scripts
### [`scripts/run_coco_benchmark.py`](scripts/run_coco_benchmark.py)
Runs the current capstone policy against the COCO/BBOB benchmark suite using a capstone-like budget. It compares the policy against a random continuation baseline, prints progress and ETA while it runs, and writes a CSV plus JSON summaries under `benchmarks/coco/`.

### [`scripts/analyze_progress_diagnostics.py`](scripts/analyze_progress_diagnostics.py)
Generates a pre-submission diagnostic report from the accumulated capstone results. It summarizes the current policy state for each function, recent coordinate sensitivity, and historical round behaviour. The Week 7 report is saved at [reports/week7_diagnostics/progress_diagnostics.md](reports/week7_diagnostics/progress_diagnostics.md).

### [`scripts/backtest_state_policy.py`](scripts/backtest_state_policy.py)
Runs a leakage-safe historical replay of the current state-policy generator. At each historical week boundary, it uses only the data available at that point, generates the policy candidate, and compares it with the actual next submission using locality and nearest-neighbour support. The Week 7 report is saved at [reports/week7_backtest/state_policy_backtest.md](reports/week7_backtest/state_policy_backtest.md).

### [`scripts/scaffold_week_structure.py`](scripts/scaffold_week_structure.py)
Creates or standardizes the core files expected in each `weekN/` folder. It is useful when setting up future rounds or repairing scaffold consistency after the repository structure changes.

### [`scripts/fill_week_from_text.py`](scripts/fill_week_from_text.py)
Populates a `weekN/` scaffold from a pasted text block containing submitted inputs and returned outputs. This is the quickest way to turn portal feedback into structured repo files.

### [`scripts/append_week_results.py`](scripts/append_week_results.py)
Reads `initial_data` and a `weekN/results.json` file, then writes appended `.npy` arrays to a chosen output directory. This keeps the weekly accumulated datasets ready for the next round of analysis.

### [`scripts/generate_candidate_queries.py`](scripts/generate_candidate_queries.py)
Generates raw next-round candidate queries from the accumulated data. It now uses a state-machine trust-region policy with explicit `bootstrap`, `momentum`, `refine`, `stagnant`, and `recovery` modes, combining Gaussian-process-style search for lower-dimensional functions with random-forest-guided search for higher-dimensional ones.

### [`scripts/sanity_check_candidates.py`](scripts/sanity_check_candidates.py)
Runs lightweight checks on proposed submissions before they are locked. It reports distance from the best-known point, trust-region adherence, nearby observed outcomes, and boundary behaviour.

### [`scripts/classifier_region_check.py`](scripts/classifier_region_check.py)
Adds a secondary region-classification check for proposed candidates. It converts each function into a temporary high-performing versus not high-performing classification problem, then scores candidates using logistic regression and, optionally, an RBF-kernel SVM.

### [`scripts/neural_net_surrogate_check.py`](scripts/neural_net_surrogate_check.py)
Runs an experimental small neural-network surrogate check. It fits a bootstrap ensemble of regularised MLP regressors and reports the predicted output, uncertainty, and percentile of a proposed candidate. This is used only as a secondary sanity check because the datasets are still small.

### [`scripts/plot_convergence.py`](scripts/plot_convergence.py)
Generates convergence plots for all functions, showing observed outputs over time, best-so-far curves, weekly submission markers, and the current best point. These plots are used to review whether a function is still improving locally or needs a reset.

### [`scripts/plot_low_dim_views.py`](scripts/plot_low_dim_views.py)
Generates exploratory visuals for the lower-dimensional functions. It creates 2D scatter plots for Functions 1 and 2, a 3D scatter plot for Function 3, and a pairwise scatter matrix for Function 4.

## Approach
The aim of this repository is to support a disciplined experimental workflow rather than a single fixed optimiser. Different optimisation methods may be used over time depending on the dimension and behaviour of each function, including local search, surrogate models, and Bayesian-optimisation-inspired reasoning.

The main objective is to maintain a clear record of:
- what was submitted each week
- what outputs were returned
- how the dataset changed over time
- what optimisation strategy was used and how it evolved

## Technical Approach
Across the first seven rounds of preparation, the strategy evolved from a broader adaptive search toward a more disciplined trust-region workflow.

Methods considered or used:
- local visual reasoning for lower-dimensional functions
- surrogate modelling with random forests for higher-dimensional functions
- Gaussian-process-style reasoning for lower-dimensional trust-region search
- manual sanity checks on distance from the best known basin, nearby outcomes, and boundary behaviour
- explicit trust-region adherence checks on every proposed candidate
- nearest-neighbour outcome checks to verify whether a candidate still sits inside a strong local basin
- classifier-based region checks using logistic regression and an RBF SVM as secondary evidence in later rounds
- experimental neural-network surrogate checks using small bootstrapped MLP ensembles as another secondary signal
- a rule that classifier outputs must not override the geometric and basin-aware checks when they conflict
- Bayesian-optimisation-inspired thinking about exploration versus exploitation, even when not using a full formal acquisition loop

I have also treated this section as a living record of the decision process. The emphasis is not on committing early to one perfect optimiser, but on updating the method as more observations arrive. In practice, that has meant using more exploration at the beginning, then gradually shifting toward tighter local refinement as the query budget becomes more valuable.

Other model families, including regression-style approximations, SVM-style region classification, and more formal Bayesian optimisation methods, are relevant as supporting tools. By Week 4, the most effective pattern had become a layered decision process: generate raw candidates from the trust-region model, run geometric sanity checks first, add classifier-style region checks second, and only then produce a manually blended final submission. In practice, that combination of surrogate guidance, visual inspection for low-dimensional cases, and explicit rules against unstable basin jumps has worked better than trusting any single model output on its own.

By Week 5, the rule was adapted again: when an earlier point remains the historical best, the next query is anchored on that historical best rather than the most recent query. Recent results are still useful, but mainly as directional evidence for how to perturb the best-known basin.

By Week 6, Function 6 became the main exception to the standard local-nudge pattern. It kept the best-known high-`x4`, low-`x5` structure, but deliberately probed lower `x2` and lower `x3` because repeated tiny moves around the same point did not improve the result. The returned Week 6 output showed that this correction probe underperformed, while the same round produced new bests for six of the other seven functions.

By Week 7, the recovery reset for Function 6 worked and produced a new best. Week 7 also produced new bests for Functions 1, 4, 5, and 7. Functions 2 and 3 dipped after Week 6, and Function 8 remained almost flat against its historical best. To prepare for Week 8, I added a coordinate-sensitivity and progress diagnostic report. Its current read is: keep local momentum for Functions 1, 4, 5, 6, and 7; refine back toward the Week 6 best regions for Functions 2 and 3; and treat Function 8 as a recovery/reset-to-best-basin case.

To test whether this hand-built policy generalizes beyond the capstone data, I also benchmarked it externally on COCO/BBOB with a capstone-like budget of `10` random initial evaluations plus `13` sequential guided evaluations. The current policy beat a random continuation baseline on two-thirds of the tested BBOB problems, which gives some evidence that the local trust-region logic is doing useful work beyond the specific course functions.

After reviewing those benchmark results, I turned the strategy into a clearer decision-rule policy:
- `momentum`: if the latest query set a new best, exploit locally around that point
- `refine`: after one non-improving round, return to the historical best basin and make a smaller local move
- `stagnant`: after two non-improving rounds, allow one bounded exploratory probe by comparing a local exploit candidate, a wider surrogate candidate, and a second-basin candidate when one exists
- `recovery`: if that exploratory probe also fails, reset to the best known basin and stop making broader jumps

That rule set improved the development COCO/BBOB benchmark from a `66.7%` win rate against random continuation to `75.0%`, and it still achieved a `72.9%` holdout win rate on unseen instances. That is not proof that the policy is optimal, but it is a useful signal that the added decision rules improved robustness rather than merely overfitting the first benchmark run.

For Week 7 review, I added a true historical backtest of the state-policy generator. The backtest replays each week boundary using only information available at that time, then compares the generated candidate with the actual next submission. Because the portal never evaluates the counterfactual candidate, the backtest uses proxy checks rather than pretending to know the missing output. The key learning was that the state labels are directionally useful, but the raw generator is usually wider than the hand-blended submissions that worked best. Across 48 historical replays, the policy candidate was more local than the actual submission only `14.58%` of the time, with a mean nearest-neighbour support delta of `-0.049`. For Week 8, this means the generator should remain a signal source, not an automatic submitter. The final submission should continue to apply micro-local clipping around proven basins unless the diagnostics provide a strong reason to widen the search.

I also explored a ranking-based policy variant that selects between multiple candidate types rather than accepting the base state-policy recommendation. This was a useful engineering experiment because it made the selection criteria explicit, but the COCO/BBOB results did not justify adopting it. On the development benchmark, the ranked variant lost to the simpler state policy on `44` of `72` comparable problems and won only `24`. The decision for now is to keep the ranked policy available in the script for future experimentation, but not use it for live capstone submissions.

The Week 8 candidate submission applies that backtest lesson directly. Raw candidates were generated with the state-policy script, but the final submitted points were manually clipped into tighter trust regions around the best observed basins. Functions 1, 4, 5, 6, and 7 are treated as momentum cases. Functions 2 and 3 are refine cases anchored on their Week 6 bests. Function 8 is a recovery case anchored tightly on its Week 2 best basin. The final Week 8 rationale is documented in [week8/approach.md](week8/approach.md), with exact reproduction steps in [week8/reproduction.md](week8/reproduction.md).

Week 8 results validated the micro-local approach for several functions, producing new bests for Functions 1, 4, 5, and 7. It did not improve Functions 2, 3, 6, or 8. The Week 8 diagnostics now classify Functions 1, 4, 5, and 7 as momentum cases; Functions 2 and 3 as stagnant cases where one bounded alternative can be compared against a local point; Function 6 as a refine case returning toward its Week 7 best; and Function 8 as a recovery case anchored tightly on the Week 2 best basin. The updated backtest through Week 8 still shows the raw state-policy generator is usually wider than the successful hand-blended submissions, with the policy more local than the actual submission only `12.50%` of the time. For Week 9, the rule remains: use the generator for state and direction, but keep final choices basin-aware and conservative unless stagnation clearly justifies one bounded alternative.

Week 9 was one of the strongest rounds so far, producing new bests for Functions 1, 3, 4, 5, 6, and 7. The return-to-basin move for Function 6 worked particularly well, and the micro-local continuation strategy remained strong for Functions 1, 4, 5, and 7. Function 3 also improved after staying close to the Week 6/Week 8 basin rather than taking the wider raw candidate. Function 2's bounded alternative failed, so it should now be treated as a recovery case anchored back on the Week 6 best. Function 8 remains very close to its Week 2 best but still has not improved, so broad moves remain hard to justify. The Week 9 diagnostics classify Functions 1, 3, 4, 5, 6, and 7 as momentum cases, and Functions 2 and 8 as recovery cases.

After Week 9, I explicitly decided not to rerun COCO/BBOB as a routine pre-submission step. The capstone now has enough internal evidence that the most useful weekly checks are the function-specific diagnostics and leakage-safe historical backtest. COCO/BBOB remains valuable when testing a new policy idea, such as the ranked selector, but rerunning it every week risks optimizing against the benchmark rather than the eight course functions. The current operating rule is: benchmark externally only when the policy changes; otherwise, use internal diagnostics and manual basin-aware blending.

Week 10 produced new bests for Functions 1, 4, 5, 7, and 8. The most important change was Function 8, where the tightly anchored recovery probe finally improved beyond the long-standing Week 2 best, moving it into momentum for Week 11. Functions 3 and 6 missed after Week 9 bests, so they should be treated as refine cases returning to their Week 9 best basins. Function 2 remains the main recovery problem after another miss. The updated Week 10 backtest still shows that raw state-policy candidates tend to be wider than the successful hand-blended submissions, so the Week 11 process should continue to use internal diagnostics and manual basin-aware blending rather than broad raw model jumps.

Week 11 again supported the micro-local approach for the strongest momentum functions. Functions 1, 4, 5, and 7 all produced new bests, with Function 5 continuing its very strong boundary-adjacent trend. Function 3 was a near miss against the Week 9 best, which suggests the basin is real but narrow. Function 8 missed by only a very small amount after the Week 10 improvement, so the next round should return to the Week 10 best basin rather than widen the search. Function 2 remains the clearest recovery problem, and Function 6 is now a stagnant case after two misses. The Week 11 diagnostics classify Functions 1, 4, 5, and 7 as momentum, Function 8 as refine, Functions 3 and 6 as stagnant, and Function 2 as recovery.

For Week 12, the strategy changes into an endgame policy because only two submissions remain. The default is no longer to test interesting raw-surrogate candidates. Instead, the default is to preserve known winning basins. Functions 1, 4, 5, and 7 receive tiny local continuation moves because they are still improving. Functions 3 and 8 remain close to their best basins after near misses. Functions 2 and 6 are the only controlled alternatives: repeated reset-to-best attempts have not recovered their historical bests, so Week 12 uses one bounded alternative for each before the final Week 13 fallback decision.

Week 12 validated the endgame policy for most functions. Functions 1, 4, 5, 7, and 8 all produced new bests, supporting one final small exploitation move. Function 2's bounded alternative improved substantially over Week 11 but did not beat the Week 6 best. Function 6's alternative came within `0.000827` of its Week 9 best, indicating useful directional information even without a new record. Function 3 was the clearest failure and should return to the Week 9 best basin for the final round. The final Week 13 decision should therefore be highly exploitative, with only very small corrections and no broad search.

The Week 13 submission applies that final-round rule. Functions 1, 4, 5, and 7 continue their repeatedly successful step patterns, while Function 8 receives a tiny move from its Week 12 best. Function 2 uses a local quadratic estimate around the Week 6 peak. Function 3 moves just beyond the latest strong point in its alternating micro-local sequence, and Function 6 tests the midpoint between its Week 9 best and Week 12 near-best alternative. All final points pass trust-region and classifier checks. The raw surrogate candidates were rejected because they remained substantially wider than the observed successful paths.

The final Week 13 results strongly validated the endgame strategy. Functions 1, 4, 5, and 7 improved again by continuing their observed trajectories, and Function 8 improved through a tiny sensitivity-guided step. Function 6 was the most valuable final insight: the midpoint between two near-equal strong regions outperformed both and created a new best. Functions 2 and 3 remained below their historical bests, demonstrating that some response surfaces stayed narrow or unstable despite extensive local sampling. Overall, six of the eight functions ended with new bests in the final round, and six functions achieved their best observed value in Week 13.

## Final Outcome
The completed challenge demonstrates a progression from broad visual and surrogate-guided exploration to a transparent state-policy trust-region workflow. The strongest general lesson is that raw surrogate recommendations were most useful as decision support, while basin-aware manual blending and small evidence-led moves produced the most consistent results under a limited evaluation budget.
