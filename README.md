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

## Decision Log
| Week | Main Strategy | What Changed | Outcome / Interpretation | Notes And Reproduction |
|---|---|---|---|---|
| 1 | Adaptive hybrid: local visual reasoning for lower-dimensional functions, random-forest surrogate guidance for higher-dimensional functions | Started with broad exploitation plus limited exploration because only the initial observations were available | Functions 5, 6, and 8 responded well; Functions 1, 3, and 7 showed that the initial direction was not yet strong enough | [Week 1 Approach](week1/approach.md), [Week 1 Reproduction](week1/reproduction.md), [Week 1 Inputs](week1/inputs.json) |
| 2 | Trust-region strategy | Shifted to tighter local search: exploit where Week 1 improved, refine cautiously where it was close, and reset toward the best historical basin where Week 1 underperformed | The sanity checks led to a safer manual override for Function 5, which then produced the strongest Week 2 improvement | [Week 2 Approach](week2/approach.md), [Week 2 Notes](week2/notes.md), [Week 2 Reproduction](week2/reproduction.md), [Week 2 Inputs](week2/inputs.json) |
| 3 | Manually blended trust-region submission | Kept the trust-region framework but overrode unstable raw model suggestions, especially for lower-dimensional functions, using sanity checks and convergence review | Current Week 3 set is designed to stay local, avoid unjustified basin jumps, and preserve momentum where evidence is strongest | [Week 3 Notes](week3/notes.md), [Week 3 Reproduction](week3/reproduction.md), [Week 3 Inputs](week3/inputs.json) |
| 4 | Late-stage trust-region with classifier-assisted review | Added logistic-regression and SVM region checks as secondary evidence, but kept trust-region, neighbour, and boundary checks as the primary filters before blending the final submission | The new classifier checks were useful for Functions 5 to 8, but they did not justify changing the core late-stage logic. The final Week 4 set stays local and basin-aware. | [Week 4 Approach](week4/approach.md), [Week 4 Notes](week4/notes.md), [Week 4 Reproduction](week4/reproduction.md), [Week 4 Inputs](week4/inputs.json) |

## Repository Workflow
The repository is organised to support the weekly optimisation cycle:

1. Start from the original arrays stored in `initial_data/`.
2. Record each round of submitted points and returned outputs in a `weekN/` folder.
3. Generate appended `.npy` files for that week so the updated dataset is ready for the next round.
4. Use the helper scripts in `scripts/` to keep the workflow repeatable and organised.

## Repository Layout
- `initial_data/`: original `.npy` arrays for each function
- `week1/`: Week 1 submission, outputs, appended datasets, lower-dimensional plots, approach notes, and reproduction notes
- `week2/`: Week 2 submission, outputs, appended datasets, raw candidates, lower-dimensional plots, notes, reflections, and reproduction notes
- `week3/`: Week 3 submission, outputs, appended datasets, raw candidates, lower-dimensional plots, convergence plots, notes, and reproduction notes
- `week4/`: Week 4 submission, raw candidates, approach notes, reproduction notes, and placeholder output files ready for returned results
- `week5/` to `week13/`: scaffold folders for future rounds
- `scripts/`: helper scripts for filling week folders, generating candidates, running checks, plotting views, and appending results
- `REPO_INVENTORY.md`: notes on the current repository structure and script usage

## Scripts
### [`scripts/fill_week_from_text.py`](scripts/fill_week_from_text.py)
Populates a `weekN/` scaffold from a pasted text block containing submitted inputs and returned outputs. This is the quickest way to turn portal feedback into structured repo files.

### [`scripts/append_week_results.py`](scripts/append_week_results.py)
Reads `initial_data` and a `weekN/results.json` file, then writes appended `.npy` arrays to a chosen output directory. This keeps the weekly accumulated datasets ready for the next round of analysis.

### [`scripts/generate_candidate_queries.py`](scripts/generate_candidate_queries.py)
Generates raw next-round candidate queries from the accumulated data. It uses a trust-region strategy, with Gaussian-process-style search for lower-dimensional functions and random-forest-guided search for higher-dimensional ones.

### [`scripts/sanity_check_candidates.py`](scripts/sanity_check_candidates.py)
Runs lightweight checks on proposed submissions before they are locked. It reports distance from the best-known point, trust-region adherence, nearby observed outcomes, and boundary behaviour.

### [`scripts/classifier_region_check.py`](scripts/classifier_region_check.py)
Adds a secondary region-classification check for proposed candidates. It converts each function into a temporary high-performing versus not high-performing classification problem, then scores candidates using logistic regression and, optionally, an RBF-kernel SVM.

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
Across the first four rounds, the strategy evolved from a broader adaptive search toward a more disciplined trust-region workflow.

Methods considered or used:
- local visual reasoning for lower-dimensional functions
- surrogate modelling with random forests for higher-dimensional functions
- Gaussian-process-style reasoning for lower-dimensional trust-region search
- manual sanity checks on distance from the best known basin, nearby outcomes, and boundary behaviour
- explicit trust-region adherence checks on every proposed candidate
- nearest-neighbour outcome checks to verify whether a candidate still sits inside a strong local basin
- classifier-based region checks using logistic regression and an RBF SVM as secondary evidence in later rounds
- a rule that classifier outputs must not override the geometric and basin-aware checks when they conflict
- Bayesian-optimisation-inspired thinking about exploration versus exploitation, even when not using a full formal acquisition loop

I have also treated this section as a living record of the decision process. The emphasis is not on committing early to one perfect optimiser, but on updating the method as more observations arrive. In practice, that has meant using more exploration at the beginning, then gradually shifting toward tighter local refinement as the query budget becomes more valuable.

Other model families, including regression-style approximations, SVM-style region classification, and more formal Bayesian optimisation methods, are relevant as supporting tools. By Week 4, the most effective pattern had become a layered decision process: generate raw candidates from the trust-region model, run geometric sanity checks first, add classifier-style region checks second, and only then produce a manually blended final submission. In practice, that combination of surrogate guidance, visual inspection for low-dimensional cases, and explicit rules against unstable basin jumps has worked better than trusting any single model output on its own.
