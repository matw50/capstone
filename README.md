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

## Decision Log
| Week | Main Strategy | What Changed | Outcome / Interpretation | Notes |
|---|---|---|---|---|
| 1 | Adaptive hybrid: local visual reasoning for lower-dimensional functions, random-forest surrogate guidance for higher-dimensional functions | Started with broad exploitation plus limited exploration because only the initial observations were available | Functions 5, 6, and 8 responded well; Functions 1, 3, and 7 showed that the initial direction was not yet strong enough | [Week 1 Approach](week1/approach.md) |
| 2 | Trust-region strategy | Shifted to tighter local search: exploit where Week 1 improved, refine cautiously where it was close, and reset toward the best historical basin where Week 1 underperformed | The sanity checks led to a safer manual override for Function 5, which then produced the strongest Week 2 improvement | [Week 2 Approach](week2/approach.md), [Week 2 Notes](week2/notes.md), [Week 2 Post-Results Reflection](week2/post_results_reflection.md) |
| 3 | Manually blended trust-region submission | Kept the trust-region framework but overrode unstable raw model suggestions, especially for lower-dimensional functions, using sanity checks and convergence review | Current Week 3 set is designed to stay local, avoid unjustified basin jumps, and preserve momentum where evidence is strongest | [Week 3 Notes](week3/notes.md), [Week 3 Inputs](week3/inputs.json) |

## Repository Workflow
The repository is organised to support the weekly optimisation cycle:

1. Start from the original arrays stored in `initial_data/`.
2. Record each round of submitted points and returned outputs in a `weekN/` folder.
3. Generate appended `.npy` files for that week so the updated dataset is ready for the next round.
4. Use the helper scripts in `scripts/` to keep the workflow repeatable and organised.

## Repository Layout
- `initial_data/`: original `.npy` arrays for each function
- `week1/`: completed week 1 submission, outputs, and appended arrays
- `week2/` to `week13/`: scaffold folders for future rounds
- `scripts/`: helper scripts for filling week folders and appending results
- `REPO_INVENTORY.md`: notes on the current repository structure and script usage

## Scripts
### `scripts/fill_week_from_text.py`
Populates a week scaffold from a pasted text block containing submitted inputs and returned outputs.

### `scripts/append_week_results.py`
Reads `initial_data` and a `weekN/results.json` file, then writes appended `.npy` arrays to a chosen output directory.

## Approach
The aim of this repository is to support a disciplined experimental workflow rather than a single fixed optimiser. Different optimisation methods may be used over time depending on the dimension and behaviour of each function, including local search, surrogate models, and Bayesian-optimisation-inspired reasoning.

The main objective is to maintain a clear record of:
- what was submitted each week
- what outputs were returned
- how the dataset changed over time
- what optimisation strategy was used and how it evolved
