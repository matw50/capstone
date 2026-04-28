# Capstone

This repository tracks data, weekly submissions, returned outputs, and helper scripts for the capstone black-box optimisation challenge.

## Environment Setup

Install the Python dependencies with:

```bash
python3 -m pip install -r requirements.txt
```

The repository currently uses:
- `numpy` for array handling and geometric checks
- `scikit-learn` for surrogate models, classifier checks, and the experimental MLP surrogate
- `matplotlib` for convergence and low-dimensional plots

## Current Status
| Item | Status |
|---|---|
| Latest completed round | Week 7 results recorded |
| Next submission prepared | Week 8 candidate submission prepared |
| Current optimisation phase | Awaiting Week 8 portal submission/results |
| Main operating pattern | Local trust-region search plus manual sanity checks |
| Extra validation in latest round | Trust-region, nearest-neighbour, logistic regression, RBF SVM, experimental MLP ensemble checks, COCO/BBOB benchmarking, and historical backtesting |

## Best Results So Far
| Function | Best Output So Far | Source | Current Read |
|---|---|---|---|
| 1 | `4.250433342725532e-15` | Week 7 | Sparse narrow peak, improved again by ultra-local probing |
| 2 | `0.7729097325485852` | Week 6 | Local momentum after historical-best anchoring |
| 3 | `-0.03140224643128403` | Week 6 | Recovery basin now improved beyond the initial best |
| 4 | `-3.962742151304709` | Week 7 | Reset-to-best-basin refinement continues to pay off |
| 5 | `3273.8921448849183` | Week 7 | Strongest momentum function, still improving |
| 6 | `-0.4993080476858224` | Week 7 | Recovery reset worked and created a new best |
| 7 | `1.7491755214029385` | Week 7 | Strong momentum after recovery |
| 8 | `9.7841491208186` | Week 2 | Week 7 remained essentially flat against the validated local basin |

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
| 8 | Prepared | [week8](week8/) | [notes](week8/notes.md) | [reproduction](week8/reproduction.md) | [results](week8/results.json) |
| 9 | Scaffold | [week9](week9/) | [notes](week9/notes.md) | [reproduction](week9/reproduction.md) | [results](week9/results.json) |
| 10 | Scaffold | [week10](week10/) | [notes](week10/notes.md) | [reproduction](week10/reproduction.md) | [results](week10/results.json) |
| 11 | Scaffold | [week11](week11/) | [notes](week11/notes.md) | [reproduction](week11/reproduction.md) | [results](week11/results.json) |
| 12 | Scaffold | [week12](week12/) | [notes](week12/notes.md) | [reproduction](week12/reproduction.md) | [results](week12/results.json) |
| 13 | Scaffold | [week13](week13/) | [notes](week13/notes.md) | [reproduction](week13/reproduction.md) | [results](week13/results.json) |

## Reproduce Latest Round
To reproduce the prepared Week 8 submission from the recorded Week 7 data:

1. Generate raw candidates:
```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week7 \
  --output-file week8/candidates.json \
  --seed 42 \
  --policy-variant state
```
2. Run the true historical backtest:
```bash
/opt/anaconda3/bin/python scripts/backtest_state_policy.py \
  --repo-root . \
  --from-week week1 \
  --through-week week7 \
  --output-dir reports/week7_backtest
```
3. Run geometric sanity checks:
```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week7 \
  --candidate-file week8/candidates.json
```
4. Run classifier region checks:
```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week7 \
  --candidate-file week8/candidates.json \
  --svm
```
5. Run the experimental neural-net surrogate check:
```bash
/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week7 \
  --candidate-file week8/candidates.json
```
6. Apply the backtest-informed manual blending rules in [week8/reproduction.md](week8/reproduction.md) to produce [week8/inputs.json](week8/inputs.json).
7. Re-run the same sanity, classifier, and neural-network checks on [week8/inputs.json](week8/inputs.json).

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
| 8 | Backtest-informed micro-local trust-region submission | Added a true historical backtest. It showed that the raw state-policy generator is directionally useful but usually wider than the successful manual submissions, so final candidates were clipped tightly around proven basins. | Submission prepared. Momentum: Functions 1, 4, 5, 6, 7. Refine: Functions 2, 3. Recovery: Function 8. | [Week 8 Approach](week8/approach.md), [Week 8 Notes](week8/notes.md), [Week 8 Reproduction](week8/reproduction.md), [Week 8 Inputs](week8/inputs.json) |

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
- `week8/`: prepared candidate submission, raw candidates, approach notes, and reproduction steps
- `week9/` to `week13/`: standardized scaffold folders for future rounds, including placeholder strategy, notes, and reproduction files
- `benchmarks/`: external optimizer checks, including COCO/BBOB runs against baselines
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
