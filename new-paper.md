# Paper Direction and Decisions

## Working Title

**Does Causality Pay Off? Evaluating a Causal-Inspired Workflow in Software Optimization**

The latest title discussed; final wording remains open.

## Agreed Direction

- **Venue:** SANER 2027 RENE.
- **Format:** A standalone paper, building on EZR and the original model-instability paper's RQ3 experiments.
- **Focus:** The incremental value of causal-inspired filtering and tree construction, rather than instability as the central problem.
- **Motivation:** Can screening potentially misleading associations improve software optimization under a small labeling budget?
- **Framing:** Keep causality in the title and motivation, but make narrow claims about the implemented workflow.
- **Contribution:** Explain when the workflow helps, when it does not, and whether benefits justify added cost.
- **Negative results:** An intended line of investigation, not a conclusion to assume before validation.

## Method and Terminology

- Call the workflow **causal-inspired**; it does not establish causal effects or perform validated causal discovery.
- Separate filtering, preprocessing, and tree splitting in the explanation and evaluation.
- Earlier discussion called the split rule “gain ratio.” Code inspection showed **normalized impurity reduction**, which is different from conventional gain ratio.
- Treat conventional gain ratio as a separate new treatment if added.

## Research Questions

1. **Effectiveness:** Does the combined workflow improve optimization quality and prediction stability over EZR?
2. **Components:** What does filtering add when preprocessing and splitting are held fixed? What explains the remaining baseline difference?
3. **Cost and robustness:** What overhead does filtering add, and how sensitive are benefits to datasets, budgets, and settings?

## Experimental Choices

- Use the original causal code and archived results as the starting point; preserve their provenance.
- Prioritize three treatments: EZR, the alternative tree without filtering, and the same tree with filtering.
- Report quality, stability, runtime.
- Audit implementation defects before interpreting poor results as evidence against the method.
- Do not infer that all causal methods fail, that nonsignificance proves equivalence, or that residual instability must be inherent to the data.

## Still Open

- Final dataset scope: SE-focused primary analysis versus the full benchmark. An SE primary subset with other domains reported separately is proposed, not finalized.
- Final title and whether validated findings justify “negative results” in the title.
- Exact robustness grid, practical-effect thresholds, and statistical protocol.
- Whether to add conventional gain ratio or additional baselines; clustering is not currently a core comparison.
- Final conclusions: limited or inconsistent benefits remain a hypothesis to check against audited reruns.
