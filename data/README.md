# Data

None of the files below are in the repository. Dimensions terms of use do not allow the raw export to be redistributed without written approval from Digital Science. The researcher file also contains personal names with inferred gender.

| File | Rows | Content | How to obtain |
|---|---|---|---|
| `raw/dimensions_export_2024-02-13.xlsx` | 1,521 | The original Dimensions export with the screening columns `includes ?` (1 relevant, 0 or −1 not) and `funding?` ("no fund" = no amount). Used by notebook 06 | Run the query in `docs/methods.md`, or ask the authors |
| `raw/grants_screened.xlsx` | 818 | Dimensions grants after screening and hand enrichment (funder income group and North/South added) | Run the query in `docs/methods.md` (Dimensions subscription), or ask the authors |
| `raw/grants_screened_v1_topics.xlsx` | 818 | Earlier version of the same table, used for the 2024 LDA run | As above |
| `raw/receiver_metadata.xlsx` | 535 | One row per recipient institution: country, region, type, World Bank income group (2023), Global North/South | Authors (it contains no personal data and can be shared on request) |
| `raw/gender_lookup.xlsx` | ~1,150 | Researcher name and inferred gender (Gender API plus manual checks) | Authors only |
| `raw/topic_probability_2024.pkl` | 799 | Frozen 2024 LDA output (k = 5) used in the paper | Authors |
| `reference/country_classification.csv` | 40 | Country → World Bank income group and Global North/South, with notes on corrections. **Public, in the repository** | Included |
| `reference/cpi_u_annual.csv` | 25 | Annual average CPI-U 1999–2023 (BLS), used for constant-dollar growth. **Public** | Included |
| `reference/draft_2025_values.csv` | 10 | Values quoted in the July 2025 manuscript draft, with cause and fix, for the corrections log. **Public** | Included |
| `interim/topic_assignments.csv` | 818 | Grant ID and topic. Written by `02_topic_modelling.ipynb` | Generated |
| `processed/phage_funding_analysis.csv` | 802 | Analysis table. Written by `01_preprocessing.ipynb` | Generated |

## Screening (1,521 → 802)
| Step | Removed | Left |
|---|---|---|
| Dimensions search, 13 Feb 2024 | | 1,521 |
| Not about therapeutic use of phages | 391 | 1,130 |
| No funding amount | 312 | 818 |
| Start year outside 1999–2023 | 16 | 802 |

The counts above are regenerated from the export's screening columns by `06_robustness.ipynb` (Table S30, Figure S12). The record-level screening decisions stay in the private export.

## Private worksheets written by notebook 06 (`data/interim/`, never committed)
| File | Purpose | When filled, save as |
|---|---|---|
| `amount_recovery_worksheet.xlsx` | 272 grants without an amount, research grants first, with the funder's page | `raw/recovered_amounts.csv` (columns `Grant ID`, `recovered_usd`) |
| `validation_screening_sample.xlsx` | Stratified 15% of the 1,521 records for a second screener | `raw/validation_screening.xlsx` |
| `validation_topics_sample.xlsx` | 100 grants (25 per topic) to hand-code | `raw/validation_topics.xlsx` |
| `validation_gender_sample.xlsx` | 100 researcher names stratified by country to check | `raw/validation_gender.xlsx` |
| `topic_probabilities_rerun.csv` | Topic probabilities from the refitted LDA (notebook 02) | (generated) |

