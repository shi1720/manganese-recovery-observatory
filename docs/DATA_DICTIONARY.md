# Data dictionary

## Raw Comtrade JSON

Each response retains original field names and metadata. `data/manifest.json` maps the response filename to its complete query URL, SHA-256 digest, record count and session date. Country code `0` is World, `268` Georgia and `842` the United States. Comparator codes are `710` South Africa, `699` India, `458` Malaysia and `579` Norway, as used by the trade API.

| Field | Meaning and use |
|---|---|
| `freqCode`, `period`, `refYear` | Annual (`A`) or monthly (`M`) reporting period. |
| `reporterCode`, `partnerCode` | Reporting economy and destination/origin partner. |
| `flowCode` | `X` exports or `M` imports. |
| `cmdCode` | HS six-digit `720230`, ferro-silico-manganese. |
| `classificationCode` | Reported HS edition, preserved without forcing a synthetic edition. |
| `partner2Code=0`, `customsCode=C00`, `motCode=0` | Total selected dimensions; avoid summing parallel breakdowns. |
| `primaryValue` | Nominal trade value in current USD used in the primary calculations. |
| `netWgt` | Export net weight in kg used consistently for Georgian annual and monthly quantities. |
| `qty`, `qtyUnitCode` | Supplementary quantity and its unit. Code 8 denotes kg; not assumed equal to net weight. |
| `isNetWgtEstimated`, `isQtyEstimated` | Source estimation flags, not guarantees of original declaration accuracy. |
| `isReported`, `isAggregate` | Source/aggregation metadata. An aggregate flag does not automatically imply estimated weight; retain all metadata. |
| `cifvalue`, `fobvalue` | Alternative valuations retained as diagnostics; no mirror reconciliation is attempted. |

## Derived outputs

- `annual.csv`: Georgian annual receipts, weight, unit receipts, both HHIs, inverse value HHI, positive-destination count and selected shares.
- `baseline_sensitivity.csv`: percentage changes for every earlier year before the 2024/2025 endpoints.
- `decomposition.csv`: common-route quantity and unit-receipts components, route entry/exit, aggregate midpoint components.
- `route_changes.csv`: destination-level endpoint values, weights and accounting contributions. A zero endpoint means no positive route record within an otherwise validated period.
- `hhi_attribution.csv`: exact two-group Shapley components for Türkiye/United States and all others. Fractions may exceed 100% or be negative when components oppose each other.
- `monthly_world.csv`, `monthly_routes.csv`: monthly Georgian series; no interpolation.
- `monthly_annual_check.csv`, `quality.csv`, `quantity_field_discrepancies.csv`: reconciliation and cross-field discrepancies.
- `us_mirror_diagnostic.csv`: separate US-reported imports; never substituted for Georgian exports.
- `reference_exporters.csv`: all comparator records, including missing/estimated quantities; no imputation.
- `reference_comparison.csv`: positive, non-estimated endpoint unit-receipts comparisons for 2022, 2024 and 2025.
- `measurement_sensitivity.csv`: conservative deterministic ±5% bounds, not confidence intervals.
- `independent_verification.json`: independent decimal checks of primary comparisons.
- `validation_summary.json`: counts and maximum residuals.

## Units and precision

Receipts are current USD. Net weight is kg. Dividing either by one million gives million USD or thousand metric tonnes, respectively. HHI is the sum of squared shares, on the unnormalised 0–1 scale. Raw source precision is retained; manuscript tables round only for display.
