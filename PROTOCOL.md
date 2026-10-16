# Analysis protocol and scope

Exploratory, retrospective study, prepared 16 October 2026. This is not a preregistration. Initial annual data were inspected before the analysis plan was finalized.

Unit: Georgia-reported annual and monthly exports of HS 720230, not mine-level output. Primary window: 2015-2025 annual; 2021-2025 monthly. No endpoint selected from an estimated treatment effect. Full available complete calendar years are retained.

Primary comparisons: 2022-2024 (boom benchmark to rebound), 2023-2024 (rebound), 2024-2025 (persistence). Also report 2022-2023, 2022-2025 and 2019-2024. Display every earlier annual benchmark for the 2024 and 2025 endpoints.

Primary variables: nominal USD receipts, net export weight in kg, USD/kg unit receipts, value and weight HHI, count of positive destinations and inverse HHI. World records are excluded when summing partners. No partner quantities are set to zero unless an otherwise complete reporter-period query has no record for that route. Wholly missing periods are never interpreted as zero exports.

Methods: aggregate midpoint value/quantity/unit-receipts identity, common-route midpoint decomposition plus explicit entry/exit receipts, two-group Shapley decomposition of HHI. For the last comparison, groups are the two largest 2024 destinations (Türkiye, United States) and all other destinations. This group choice was made after inspection and is descriptive, not confirmatory.

Validation: source file checksums; response count and truncation guard; unique keys; partner totals against World; quantity units and estimation flags; all 60 monthly World records; monthly totals against annual totals; independently recompute primary results from raw JSON with standard-library decimal arithmetic; algebraic and randomized decomposition invariants.

Sensitivity: benchmark changes; value versus weight HHI; aggregate versus common-route unit receipts; deterministic +/-5% proportional measurement-error screens. No confidence intervals or p-values: administrative totals are not an independent sample, and measurement uncertainty has no calibrated sampling law here.

Identification limits: no exogenous treatment, no causal effect of protests, tariffs, sanctions or ownership; no firm or mine attribution; no inference that reduced exports improve ecology or that higher gross receipts improve wages. U.S. annual data are retained as a separate diagnostic, not reconciled with Georgian flows. No use of the anomalous USGS 2024 manganese concentrate production entry for trend estimation.

## External comparator extension

After primary results and the first manuscript draft, a further descriptive check was specified before retrieving the comparator series. South Africa, India, Malaysia and Norway were chosen as established suppliers identified in the reviewed USITC industry report. World export records for 2019-2025 are archived, with the displayed 2022/2024/2025 comparison restricted to positive, non-estimated net weights. Missing and estimated source records in other years are preserved rather than imputed. This is a purposive external check, not a causal control group or global price index.
