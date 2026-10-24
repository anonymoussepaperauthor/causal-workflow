# Does Causality Pay Off? Evaluating a Causal-Inspired Workflow in Software Optimization

> **Anonymous submission for SANER 2027 RENE** — Author information withheld for double-anonymous review.

## Overview

Reproduction repository for a study of causal-inspired filtering and tree construction in label-efficient optimization. It includes the experiment code, 127 MOOT datasets, and saved results for labeling budgets of **50, 100, 150, and 200**.

## Treatments

| Output identifier | Tree construction | Confounder filtering |
|---|---|---|
| `ezr` | Original EZR | No |
| `ezr-cf` | Original EZR with filtering preprocessing | Yes |
| `cs` | Causal-inspired | No |
| `cs-cf` | Causal-inspired | Yes |

CF uses conditional-dependence screening. CS combines discretization, one-value-versus-rest partitions, normalized impurity reduction, and alternative stopping rules. The workflow is causal-inspired; it does not establish causal effects. The split score is not conventional gain ratio.

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── LICENSE
├── data/
│   ├── dataset_summary.csv         # Dataset characteristics
│   └── optimize/                   # 127 benchmark inputs
│       ├── behavior_data/
│       ├── binary_config/
│       ├── config/
│       ├── financial_data/
│       ├── health_data/
│       ├── hpo/
│       ├── misc/
│       ├── process/
│       ├── rl/
│       ├── sales_data/
│       ├── systems/
│       └── test/
├── experiment/
│   ├── main.py                     # Four-treatment experiment driver
│   ├── example.py                  # Recommendation example
│   ├── try.py                      # Exploratory filtering script
│   ├── 50/                         # Saved results: labeling budget 50
│   ├── 100/                        # Saved results: labeling budget 100
│   ├── 150/                        # Saved results: labeling budget 150
│   └── 200/                        # Saved results: labeling budget 200
├── tools/
│   ├── ezr.py                      # Baseline sampling, trees, and scoring
│   ├── causal_tools.py             # Filtering and alternative tree construction
│   ├── stats.py                    # Statistical comparisons
│   └── aggregate_results.py        # Dataset-by-treatment result tables
├── runners/
│   └── runner.sh                   # Batch execution with GNU Parallel
├── docs/
│   └── example.txt                 # Example output
└── new-paper.md                    # Earlier planning notes
```

Each budget directory contains one summary CSV per dataset and an `aggregates/` subdirectory with dataset-by-treatment tables for each metric. The saved results are available at [50](experiment/50/), [100](experiment/100/), [150](experiment/150/), and [200](experiment/200/).

## Datasets

The experiments use **127 datasets** from [MOOT](https://github.com/timm/moot), covering software optimization and other application domains, with both single-objective and multi-objective tasks. The table follows the actual folders under [data/optimize/](data/optimize/).

| Dataset group | Directory | Count | Examples |
|---|---|---:|---|
| Behavioral data | `behavior_data/` | 4 | Employee attrition, player statistics, student dropout |
| Binary configurations and feature models | `binary_config/` | 12 | FFM, FM, Scrum, billing10k |
| Software configurations | `config/` | 35 | SS-A–SS-X, Apache, SQL, X264 |
| Financial data | `financial_data/` | 4 | BankChurners, Loan, Telco churn |
| Health data | `health_data/` | 3 | COVID-19, life expectancy, hospital readmissions |
| Software project health | `hpo/` | 35 | Closed issues, closed pull requests, commits |
| Miscellaneous | `misc/` | 3 | auto93, car prices, wine quality |
| Software process models | `process/` | 10 | coc1000, nasa93dem, POM3, XOMO |
| Reinforcement learning | `rl/` | 2 | A2C Acrobot, A2C CartPole |
| Sales data | `sales_data/` | 5 | Marketing analytics, accessories, wallpaper |
| Software systems | `systems/` | 12 | PostgreSQL, LLVM, Redis, x264 |
| Test datasets | `test/` | 2 | dataset120, dataset600 |
| **Total** | | **127** | |

See [data/dataset_summary.csv](data/dataset_summary.csv) for dataset characteristics and the README files within the dataset folders for source descriptions.

## Research Questions

| RQ | Question |
|---|---|
| **RQ1 — Effectiveness** | Does the combined causal-inspired workflow improve optimization quality and recommendation stability over EZR? |
| **RQ2 — Components** | What do confounder filtering and alternative tree construction contribute individually and together? |
| **RQ3 — Variation and cost** | How do outcomes vary across datasets and labeling budgets, and what computational overhead do the treatments introduce? |

The four treatments in [experiment/main.py](experiment/main.py) support these comparisons; the budget-specific result folders contain the quality, stability, and runtime outputs.

## Key Findings

1. **Mixed quality gains:** Across budgets, CS–CF improves RMSE over EZR on 56–63 of 127 datasets and worsens it on 57–67.
2. **Limited filtering benefit:** Adding CF leaves rounded RMSE unchanged on 103–107 datasets for EZR and 95–102 for CS, depending on budget.
3. **Substantial filtering cost:** CF increases total measured construction-and-ranking time by 6.88–10.36× for EZR and 4.56–4.96× for CS across budgets.

These are descriptive comparisons of the archived results at budgets 50, 100, 150, and 200; RMSE equality is assessed at the exported two-decimal precision. They concern this implemented workflow and do not establish conclusions about causal methods in general.

## Setup

Use **Python 3.10 or newer**. Run the following commands from the repository root:

```bash
python -m pip install -r requirements.txt
```

Install **GNU Parallel** separately if using the batch runner.

## Run a single dataset

```bash
python experiment/main.py data/optimize/misc/auto93.csv
```

For the PostgreSQL example:

```bash
python experiment/main.py data/optimize/systems/PostgreSQL.csv
```

The driver prints one CSV row per treatment after 20 repetitions. The current code fixes `the.Budget = 200` inside `run()`; it does not accept a command-line budget option. To rerun another archived budget, set that assignment to 50, 100, or 150 in your local copy before running.

## Run all datasets

```bash
mkdir -p experiment/results
bash runners/runner.sh
```

The runner writes to `experiment/results/`, regardless of the budget selected in the driver. It overwrites same-named files there, so preserve any previous run before starting another. The saved budget directories listed above are separate from this output path.

Aggregate the new results with:

```bash
mkdir -p experiment/results/aggregates
python tools/aggregate_results.py
```

The aggregation script reads `experiment/results/` and writes to `experiment/results/aggregates/`. Its default paths do not select an archived budget folder.

## Experimental settings

- **Repetitions:** 20, with seeds 0–19 reset before each treatment's repetition.
- **Split:** 50% training and 50% holdout, paired across treatments.
- **Label selection:** `likely()` with acquisition `near`.
- **Tree settings:** Gini impurity and minimum leaf size three.
- **Checking budget:** five candidates, inherited from `tools/ezr.py`.
- **Recommendation:** the best of the checked, highest-ranked holdout candidates.
- **Reference optimum:** the best configuration in the holdout pool.

Training configurations are not included as final recommendations or in the reference optimum. Actual labels and checks can be fewer than the nominal budgets when there are insufficient candidates.

## Reading the results

Objective values are normalized and combined into distance-to-heaven (`d2h`), then converted to integer win scores using the full dataset's minimum and mean `d2h`. Higher win scores are better. A run's error is the holdout reference win score minus the recommendation win score.

| CSV field | Meaning |
|---|---|
| `trt` | Treatment identifier |
| `perf-rmse` | Root mean square of the 20 run-level errors; lower is better |
| `stab-std` | Sample standard deviation of recommendation win scores; lower means more consistent recommendation quality |
| `best_perf` | Membership in the quality top set |
| `best_stab` | Legacy stability ranking flag; interpret stability descriptively |
| `runtimes` | Total filtering, tree-construction, and holdout-ranking time in seconds across 20 runs |

Quality top-set membership is computed from run-level errors using `top()` with `Ks=0.9`, `Delta="smed"`, and minimum mean separation of 0.35 times the pooled error standard deviation. Ties are possible; top-set membership does not establish equivalence.

The stability flag compares one standard deviation per treatment and should not be treated as statistical evidence of a stability difference. Runtime excludes active-learning sampling and final objective-score calculations and varies with hardware and system load.

The driver exports rounded summary metrics and ranking flags, not the underlying per-seed observations. Consult the saved tables for each budget when comparing results.

## Related Resources

The benchmarks come from [MOOT](https://github.com/timm/moot). Individual source descriptions are retained in the dataset directories. The baseline builds on [EZR](https://github.com/timm/ezr).

## Citation

Paper citation and BibTeX entry will be added after double-anonymous review.

<!-- Add the final paper citation and BibTeX entry here after review. -->

## License

The repository code is released under the [MIT License](LICENSE). Dataset source descriptions retain upstream attribution.

<!-- Add any additional dataset-specific license information here, if applicable. -->
