# Manganese Recovery Observatory

Research materials for **What Counts as Recovery? Manganese, Market Switching and Uneven Adjustment in Georgia, 2015–2025**, by Shivam Gupta (2026).

This is an exploratory empirical research manuscript, not an accepted publication. The repository distinguishes export weight, gross nominal receipts and destination concentration. It contains actual public data, a reproducible analysis and a small offline observatory. It makes no claim of a new concentration index, a causal effect of labour conflict or trade policy, or an estimate of local welfare.

## Main findings

- In 2024, Georgia exported 20.61% more silicomanganese by weight than in 2022, but received 31.22% fewer nominal dollars. Against 2019, weight and receipts were 0.66% and 3.02% higher; the boom benchmark matters.
- The 2023–2024 rebound increased both value and weight concentration as Türkiye became the largest destination.
- In 2025, value HHI fell 65.41% while export weight fell 25.24% and receipts fell 28.79%.
- A two-group Shapley accounting decomposition assigns 65.85% of the concentration decline to changes in Türkiye and US sales. Expansion elsewhere partly offset their receipts losses.
- Aggregate and common-route unit-receipts components can have opposite signs. Neither is a quality-adjusted transaction-price index.

## Reproduce the snapshot

Tested with Python 3.9.6, NumPy 1.26.4, pandas 2.2.2 and Matplotlib 3.9.4. Use Python 3.9–3.12 with these pins.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 src/analyze.py
python3 src/reference.py
python3 src/verify_independently.py
python3 -m unittest discover -s tests -v
python3 src/figures.py
python3 src/dashboard.py
```

The archived data allow reproduction without network access after installing dependencies. Open `observatory.html` in a browser to explore the derived results. It has no tracking, external library or data request.

Build the paper with Tectonic:

```sh
cd paper
tectonic manuscript.tex
```

To retrieve a new snapshot, run `python3 src/fetch.py`, then `python3 src/fetch_reference.py`. This uses the official public preview API, with one period per query, bounded retries, a local cache and a guard against the 500-record ceiling. The second script appends comparator queries to the main manifest. Remove only the specific cache files you intend to refresh; upstream revisions can change results. Preserve the archived snapshot and manifest if you need the published numbers.

An external check against South Africa, India, Malaysia and Norway shows lower unit receipts in each after 2022. Georgia's decline is larger, but grade, contract and destination differences prevent interpreting this as a quality-adjusted price penalty. Missing and estimated comparator weights are preserved; the displayed endpoint comparison uses only non-estimated positive weights.

## Files

- `paper/manuscript.pdf`, `.tex`, `references.bib`: paper and editable source.
- `data/raw/`: archived UN Comtrade JSON; each query is below the preview record ceiling.
- `data/manifest.json`: full URLs, hashes, counts and retrieval-session date.
- `data/derived/`: annual series, all baseline comparisons, route decompositions, concentration attribution, source discrepancies and independent verification.
- `src/`: retrieval, analysis, verification, plots and offline viewer.
- `tests/`: accounting invariants and snapshot validation.
- `figures/`: vector PDF and PNG versions of the paper figures.
- `PROTOCOL.md`: exploratory scope, comparisons and identification limits.
- `LITERATURE_REVIEW.md`: closest antecedents and bounded novelty assessment.
- `APPLICATIONS.md`: practical uses and evidence limits.

## Data qualifications

Primary conclusions use **Georgia-reported exports of HS 720230**, net weight and primaryValue, not mine-level production. World rows validate totals and are excluded from partner sums. The historical 2015 quantity field differs from net weight in two destinations and the World aggregate; net weight is used consistently. Summed 2022 monthly net weight exceeds the annual declaration by 171.5 kg; the discrepancy is retained. US mirror records are diagnostic and are never averaged or spliced into the Georgian series. See the manuscript for full limitations.

No p-values or confidence intervals are manufactured from administrative totals. The ±5% error screens are deterministic sensitivity bounds, not statistical uncertainty intervals.

## Licence and citation

Code: MIT (`LICENSE`). Manuscript and original figures: CC BY 4.0. Raw UN Comtrade records remain United Nations data, with source terms at [UN Comtrade re-dissemination policy](https://uncomtrade.org/docs/re-dissemination-of-data/). This small, free research archive is below the stated 100,000-record threshold; the code licence does not relicense the underlying data.

Please cite the manuscript and **UN Comtrade** when using the findings. `CITATION.cff` provides manuscript metadata. Conference selection and journal peer review are separate from this repository's computational checks.
