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
| Funding received by high-income countries | 97.8% | Fig. 4, Table 5 |
| Funding received by the Global South (73% of it by China) | 2.1% | Tables S4, S11 |
| Funding received by lower-middle and low-income countries | 0.33% | Fig. 4, Table 5 |
| Funding in grants whose recipients are all in the funder's country | 88.7% | Table S12 |
| Share of funding from NIAID | 21.0% | Table 2a |
| Female-only vs male-only grant size (adjusted for team size, grant length, year, funder and topic) | −19% (95% CI −32 to −2) | Fig. 3, Tables S3, S35 |
| Researchers who held only one grant | 83.9% | Tables S7, S37 |
| Global South share if grants without an amount are imputed (low–high) | 2.6–5.5% of funding | Table S33 |
| Global South share counting grants, all 1,074 relevant grants | 17.5% of grants | Table S32 |
| Share of funding from US funders (NIAID: 14% → 17% → 23% across three periods) | 47.7% | Fig. 5, Tables S24–S25 |
| Concentration across funder countries (HHI, 0–10,000) | 2,501 (highly concentrated) | Table S24 |
| Funding received by the top 10% of recipient institutions | 53.4% (Gini 0.68) | Fig. 5, Table S24 |
| Grants linking Global North and Global South recipients | 7 of 802 | Table S26 |
| Growth in funding per year, constant 2023 USD (CPI-U) | +14.1% per year (95% CI 10.2–18.2) | Table S28 |
| Growth without NIAID (grants / funding) | +11.7% / +16.2% per year | Table S27 |

## Repository structure
```
├── notebooks/
│   ├── 01_preprocessing.ipynb     build the analysis table (802 grants)
│   ├── 02_topic_modelling.ipynb   LDA topics, coherence curve, seed stability
│   ├── 03_main_analysis.ipynb     every figure and table in the paper
│   ├── 04_supplementary_figures.ipynb   Figures S2–S10 from the 2024–25 notebooks, redrawn
│   ├── 05_concentration_and_sensitivity.ipynb   Figure 5, Figure S11, Tables S24–S29
│   └── 06_robustness.ipynb        missing amounts, projects, alternative definitions: Figures S12–S13, Tables S30–S37
├── src/
│   ├── preprocess.py              joins grants, institution metadata, gender and topics
│   ├── topics.py                  text cleaning, LDA, coherence, stability
│   ├── phagefund.py               growth, fractional counting, gender tests, engagement types
│   ├── robustness.py              award types, grants without an amount, imputation, projects (v1.5)
│   └── figures.py                 reusable plotting blocks (heatmap, engagement lines, dendrogram, Sankey)
├── outputs/
│   ├── figures/                   Fig1–Fig5, FigS1–S9, FigS11–S13 (PNG 300 dpi and PDF), FigS10 (HTML)
│   └── tables/                    Tables 1–5, S1–S37, key_numbers.json
├── data/
│   ├── reference/country_classification.csv   public: country income group and North/South
│   ├── reference/cpi_u_annual.csv             public: CPI-U annual averages 1999–2023
│   ├── reference/draft_2025_values.csv        public: values quoted in the July 2025 draft
│   ├── reference/nih_reporter_crosscheck.csv  public: yearly NIH totals, column to fill from NIH RePORTER
│   ├── reference/ppp_price_level_2023.csv     public: column to fill with World Bank price level ratios
│   └── raw/, interim/, processed/             private, not in the repository (data/README.md)
├── docs/methods.md                search query and methods in full
├── docs/notebook_inventory.md     what each 2024–25 Colab notebook did, and what was kept
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
`run_all.sh` runs the notebooks in this order: 02 (topics), 01 (table), 03 (results), 04 (supplementary figures), 05 (concentration and sensitivity), 06 (robustness).
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
| Tables S11–S13: Global South by country, domestic vs cross-border, cross-border funders | 03 | `S11`–`S13_*.csv` |
| Figure S2: grants per year, top 15 funders | 04 | `FigS2_funders_by_year`, `S14` |
| Figure S3: each funder's grants by topic | 04 | `FigS3_topic_by_funder`, `S15` |
| Figure S4: topics by recipient country and Global North/South | 04 | `FigS4_topic_by_recipient`, `S16` |
| Figure S5: topic similarity (word overlap, clustering) | 04 | `FigS5_topic_similarity`, `S17`, `S18` |
| Figure S6: named researchers by gender per year | 04 | `FigS6_researchers_by_gender`, `S19` |
| Figure S7: team gender by topic | 04 | `FigS7_team_gender_by_topic`, `S20` |
| Figure S8: researcher engagement over time, overall and by team gender | 04 | `FigS8_researcher_engagement`, `S21` |
| Figure S9: institution engagement over time, by topic | 04 | `FigS9_institution_engagement_by_topic`, `S22` |
| Figure S10: funder country → recipient country flows (interactive) | 04 | `FigS10_country_flows.html`, `S23` |
| Figure 5: concentration (US and NIAID shares, Lorenz curve, top 10 funders by topic) | 05 | `Fig5_concentration`, `S24`, `S25` |
| Table S26: collaboration counts | 05 | `S26_collaboration.csv` |
| Table S27: growth and concentration without NIAID | 05 | `S27_without_niaid.csv` |
| Table S28: growth in constant 2023 USD | 05 | `S28_real_growth.csv` |
| Figure S11, Table S29: draft vs corrected values | 05 | `FigS11_corrections`, `S29_corrections_log.csv` |
| Figure S12, Table S30: screening flow | 06 | `FigS12_screening_flow`, `S30_screening_flow.csv` |
| Table S31: award types, grants with and without an amount | 06 | `S31_award_types.csv` |
| Table S32: count-based shares including grants without an amount | 06 | `S32_count_based_shares.csv` |
| Table S33: dollar shares with imputed or recovered amounts | 06 | `S33_imputed_amount_scenarios.csv` |
| Table S34: yearly records merged into projects | 06 | `S34_projects.csv` |
| Table S35: gender gap in subsets | 06 | `S35_gender_subsets.csv` |
| Table S36: topic shares from topic probabilities | 06 | `S36_topic_probability_shares.csv` |
| Figure S13, Table S37: robustness summary | 06 | `FigS13_robustness`, `S37_robustness_summary.csv` |

## Corrections compared with the 2024–25 Colab notebooks
1. **Growth rate.** Now computed on USD amounts with a log-linear fit. The old CAGR used original-currency amounts and 25 intervals instead of 24.
2. **Gender.** Groups are now exclusive. The old totals counted mixed teams in both the male and female groups.
3. **Recipient counting.** Lists stay in order, so country and income group line up with each institution. Each institution gets an equal share of a shared grant.
4. **Topic coherence.** Now computed with the correct word order. k = 5 is still the best choice.
5. **Duplicate texts.** 17 grants whose text duplicated another grant had no topic. They now take their twin's topic.
6. **Figures.** All figures are now drawn from the data, with no numbers typed into plotting code.
7. **Country labels (v1.1).** The hand-made recipient file labelled Switzerland, Sweden and Spain as "Global South / Upper middle income". Labels now come from one reference table for funders and recipients. Global South recipients: 6.7% → 2.1% of funding.
8. **EU funders (v1.1).** The European Commission and the ERC (23 grants) were coded as funder country Belgium. They are now "European Union".
9. **Engagement plots (v1.2).** In the old notebooks the "Fund to female" plot reused the male data, several topic × gender sections read the full dataset, and plots used the row index for years with gaps for zero counts. Figures S8–S9 fix all three. Details in `docs/notebook_inventory.md`.
10. **Gender model (v1.5).** The main model now controls for funder, grant length and topic. The female-only gap is −19% (was −27%). The mixed-team advantage (+58%) disappears (−7%, not significant): it reflected which funders fund mixed teams and for how long.
11. **Grants without an amount (v1.5).** 272 relevant grants (1999–2023) have no amount in Dimensions; 43% are training awards (studentships, scholarships, theses). They are now used in count-based checks and imputation scenarios (Tables S31–S33).

## Figure style
Figures use the CognosX palette and type ([github.com/cognosx/brand](https://github.com/cognosx/brand)), set in `src/phagefund.py` (`PALETTE`, `INK`, `GRID`, fonts) and `src/figures.py` (`STYLE`, `SEQ`). Change them there to restyle every figure. Figures have no logo, for journal use.

## Limitations to keep in mind
- **Coverage.** Dimensions covers NIH, European and Japanese funders well but many low- and middle-income country funders poorly.
- **Missing amounts.** 272 relevant grants have no amount, mostly from Brazil (FAPESP, CAPES), Russia (RFBR, RSF) and Belgium (BELSPO, FWO). Dollar shares are shares of *recorded* funding; counting grants, the Global South receives 17.5% (Tables S32–S33).
- **Amounts.** Amounts are nominal USD; constant-dollar growth is in Table S28. Purchasing-power adjustment needs `data/reference/ppp_price_level_2023.csv` filled in.
- **Engagement.** "Transient" depends on the activity rule (82% with the start-year rule, 3.5% with the full-span rule). The share of researchers with a single grant (84%) does not.
- **Gender.** Inferred from first names, so it is binary.
- **Topics.** About 60% of grants keep the same topic when the LDA random seed changes (Table S9), and the refitted model agrees with the 2024 assignment for 59% of grants. The rise of antibiotic-resistance research holds under every topic method, but its level does not (26% to 44% of 2016–2023 funding, Table S36), so read topic results as trends.

## Licence and citation
Code: MIT (`LICENSE`). Cite with `CITATION.cff`.
Grant-level data are not redistributed (Dimensions terms of use); see `data/README.md`.
