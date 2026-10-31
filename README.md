# Global phage therapy research funding, 1999–2023

Code for the preprint *Global Trends and Equity in Bacteriophage Therapy Research Funding (1999–2023)*.
It covers 802 grants worth USD 318.6 million, taken from Dimensions (export of 13 Feb 2024).
The method follows the phage therapy patent landscape study by Mbogning Fonkou & Kong,
[*Nat. Biotechnol.* 42, 1781–1791 (2024)](https://www.nature.com/articles/s41587-024-02493-9).

## Main findings
| Finding | Value | Source |
|---|---|---|
| Growth in grants per year, 1999–2022 (log-linear) | +12.2% per year (95% CI 10.0–14.5) | Fig. 1, Table S2 |
| Growth in funding per year, 1999–2022 (nominal USD) | +16.6% per year (95% CI 12.6–20.7) | Fig. 1, Table S2 |
| Funding from high-income countries | 98.3% | Fig. 4, Table 5 |
| Funding received by lower-middle and low-income countries | 0.34% | Fig. 4, Table 5 |
| Share of funding from NIAID | 21.0% | Table 2a |
| Female-only vs male-only grant size (adjusted) | −27% (95% CI −43 to −8) | Fig. 3, Table S3 |

## Repository structure
```
├── notebooks/
│   ├── 01_preprocessing.ipynb     build the analysis table (802 grants)
│   ├── 02_topic_modelling.ipynb   LDA topics, coherence curve, seed stability
│   └── 03_main_analysis.ipynb     every figure and table in the paper
├── src/
│   ├── preprocess.py              joins grants, institution metadata, gender and topics
│   ├── topics.py                  text cleaning, LDA, coherence, stability
│   └── phagefund.py               growth, fractional counting, gender tests, engagement types
├── outputs/
│   ├── figures/                   Fig1–Fig4, FigS1 (PNG 300 dpi and PDF)
│   └── tables/                    Tables 1–5, S1–S10, key_numbers.json
├── data/                          not in the repository; see data/README.md
├── docs/methods.md                search query and methods in full
├── archive/2024_colab/            original 2024 notebooks, kept for the record
├── environment.yml
└── run_all.sh
```

## How to reproduce
```bash
conda env create -f environment.yml
conda activate phagefund
# put the input files in data/raw/ (see data/README.md)
./run_all.sh
```
`run_all.sh` runs the notebooks in this order: 02 (topics), 01 (table), 03 (results).
On a laptop the whole run takes about 10 minutes.

## Figure and table map
| Paper item | Notebook | Output |
|---|---|---|
| Figure 1: grants and funding per year | 03 | `Fig1_trends` |
| Figure 2: topic share by period | 03 | `Fig2_topics` |
| Figure 3: gender | 03 | `Fig3_gender` |
| Figure 4: income groups and countries | 03 | `Fig4_geography` |
| Table 1: grants by period | 03 | `Table1_by_period.csv` |
| Table 2: top funders and recipients | 03 | `Table2a_top_funders.csv`, `Table2b_top_recipients.csv` |
| Table 3: topics | 03 | `Table3_topics.csv` |
| Table 4: gender | 03 | `Table4_gender.csv` |
| Table 5: income groups | 03 | `Table5_income_groups.csv` |
| Figure S1: topic coherence | 02 | `FigS1_topic_coherence` |
| Tables S1–S7: data quality, growth, tests, geography, engagement | 03 | `S1`–`S7_*.csv` |
| Tables S8–S10: coherence, stability, topic words | 02 | `S8`–`S10_*.csv` |

## Corrections compared with the 2024–25 Colab notebooks
1. **Growth rate.** Now computed on USD amounts with a log-linear fit. The old CAGR used original-currency amounts and 25 intervals instead of 24.
2. **Gender.** Groups are now exclusive. The old totals counted mixed teams in both the male and female groups.
3. **Recipient counting.** Lists stay in order, so country and income group line up with each institution. Each institution gets an equal share of a shared grant.
4. **Topic coherence.** Now computed with the correct word order. k = 5 is still the best choice.
5. **Duplicate texts.** 17 grants whose text duplicated another grant had no topic. They now take their twin's topic.
6. **Figures.** All figures are now drawn from the data, with no numbers typed into plotting code.

## Limitations to keep in mind
- **Coverage.** Dimensions covers NIH, European and Japanese funders well but many low- and middle-income country funders poorly.
- **Amounts.** All amounts are nominal USD.
- **Gender.** Inferred from first names, so it is binary.
- **Topics.** About 60% of grants keep the same topic when the LDA random seed changes (Table S9), so read topic results at the aggregate level.

## Licence and citation
Code: MIT (`LICENSE`). Cite with `CITATION.cff`.
Grant-level data are not redistributed (Dimensions terms of use); see `data/README.md`.
