# Datasheet: BBO Capstone Dataset

## Motivation
This dataset supports the Black-Box Optimisation (BBO) capstone challenge. The task is to propose query points for eight unknown maximisation functions and use the returned outputs to improve future submissions. The dataset was created to document the iterative search process, preserve evidence behind each query, and make the optimisation strategy reproducible.

The data was developed as part of the Imperial Professional Certificate in Machine Learning and Artificial Intelligence capstone project. The functions are synthetic black-box functions provided through the course portal. The repository records my submitted queries, returned outputs, derived candidates, diagnostic reports, and notes.

The dataset helps answer:
- which query points were submitted for each function
- what output each query returned
- how the best observed value changed over time
- how the optimisation strategy evolved as more evidence became available

## Composition
The dataset contains eight separate black-box optimisation histories. Each function accepts a numeric input vector and returns one scalar output.

Function dimensions:
- Function 1: 2D
- Function 2: 2D
- Function 3: 3D
- Function 4: 4D
- Function 5: 4D
- Function 6: 5D
- Function 7: 6D
- Function 8: 8D

Data formats:
- initial inputs and outputs are stored as `.npy` arrays under `initial_data/function_<n>/`
- weekly submissions are stored as JSON in `week<n>/inputs.json`
- weekly returned outputs are stored as JSON in `week<n>/outputs.json`
- combined input/output records are stored in `week<n>/results.json`
- appended arrays are stored in `week<n>/function_<n>/inputs.npy` and `outputs.npy` once each week is recorded
- raw candidates, notes, reproduction steps, diagnostics, and backtests are stored as JSON or Markdown

The initial dataset contains known starting observations for each function. Each weekly round adds one new observed query/output pair per function. The completed dataset contains the initial data plus all returned observations from Week 1 through Week 13.

The dataset is not a random or complete sample of the full input space. It is an adaptive optimisation trace, biased toward regions that appeared promising in previous rounds. This is intentional, but it means the dataset should not be treated as representative of the full function domains.

No personal, demographic, sensitive, or human-subject data is present. The data consists of synthetic numeric inputs, synthetic scalar outputs, and project metadata.

## Collection Process
The initial data was provided by the capstone project. Weekly observations were collected by submitting one query per function through the capstone portal and recording the returned output values.

Queries were generated iteratively using:
- visual and local reasoning for lower-dimensional functions
- Gaussian-process-style candidate generation for lower-dimensional trust-region search
- random-forest surrogate guidance for higher-dimensional functions
- sanity checks based on distance to best points, nearest-neighbour support, boundary flags, and trust-region adherence
- logistic regression, RBF SVM, and small MLP surrogate checks as secondary evidence
- historical backtests to understand whether generated candidates were too broad
- manual basin-aware blending before final submission

The collection process was adaptive rather than random. Later queries depended on prior observations, returned outputs, diagnostic reports, and reflection notes. Broad exploration was used more early on, then the strategy shifted toward local exploitation and recovery around best observed basins as the remaining query budget became more valuable.

No human subjects or consent process applies because the observations are synthetic black-box function evaluations supplied by the course challenge.

## Preprocessing, Cleaning, And Labelling
The raw numeric values from the portal were preserved in JSON files. Appended `.npy` arrays were generated from the initial arrays and weekly results to support modelling and plotting.

Preprocessing steps include:
- converting submitted and returned values into structured JSON
- appending weekly observations to function-level `.npy` arrays
- generating candidate JSON files from accumulated data
- producing diagnostic and backtest reports from historical observations
- formatting portal submissions as six-decimal hyphen-separated strings in `submission.txt`

No supervised labels are provided by the original challenge. Some helper scripts temporarily create derived labels such as high-performing versus lower-performing regions for classifier checks, but these are diagnostic constructs rather than canonical dataset labels.

The challenge dataset is complete through Week 13. No weekly portal outputs are missing from the recorded challenge history.

## Uses
Intended uses:
- reproduce the capstone optimisation history
- analyse how query strategy evolved over time
- train or evaluate surrogate models for the eight capstone functions
- replay or study historical candidate-generation decisions
- support portfolio documentation and reflections
- demonstrate responsible documentation of an iterative ML workflow

Inappropriate uses:
- treating the dataset as representative samples of the full function domains
- using the synthetic outputs as real-world measurements
- drawing claims about real physical, medical, financial, or business systems
- using the data to benchmark general-purpose optimisers without noting the adaptive sampling bias

Known risks and limitations:
- the dataset is small relative to the dimensionality of several functions
- query locations are heavily biased toward successful regions
- the true functions are hidden, so uncertainty about global optima remains
- model-based conclusions may overfit the limited observations
- many apparently strong patterns may reflect local behaviour rather than global structure

## Distribution
The dataset is stored in this GitHub repository for capstone documentation and reproducibility. It includes synthetic challenge data, submitted queries, returned outputs, scripts, notes, and generated reports.

Distribution is through the repository itself. Any use should respect the course context and any applicable programme or portal terms. The repository should be treated as educational project documentation rather than a general public benchmark.

## Maintenance
The completed dataset is maintained by the repository owner as a versioned portfolio and reproducibility artefact.

Maintenance process:
- preserve the final weekly inputs, outputs, and results without rewriting history
- keep scripts and dependency documentation reproducible
- update final analysis, visualisations, or presentation artefacts when needed
- use Git commits to retain an auditable record of any post-project changes

The dataset is version controlled with Git. Weekly folders provide an audit trail of inputs, outputs, rationale, candidates, and follow-up analysis. Future updates should preserve prior results rather than overwrite historical decisions.
