# Changelog

## v1.2 (31 Oct 2026)
- **New notebook `04_supplementary_figures`.** It redraws the figures worth keeping from the 2024–25 Colab notebooks (Figures S2–S10, Tables S14–S23).
- **Code ported from the notebooks.**
  - In `src/phagefund.py`: `explode_entities` (was `preprocess_entity_data`), `engagement_by_year` (was `classify_entities_func` + `count_entity_classifications`), `researchers_by_gender_year` (was `count_gender_by_year`), `row_shares` (was `group_and_pivot`), `country_flows`, `aligned_long`, `jaccard_matrix`, `distinctive_words`.
  - New `src/figures.py`: `heatmap` (was `plot_top_50_heatmap`), `engagement_panel` (was `plot_entity_trends`), `topic_dendrogram`, `sankey_html` (was `create_sankey_diagrams_top20`).
- **Fixes over the old code.**
  - Engagement: real years on the x-axis, 0 instead of gaps, the same end year (2023) for every subset, and the female funder plot no longer reuses the male data.
  - Heatmaps show counts or shares, not dollar amounts in every cell, and leave empty cells white.
  - Patent-study labels ("Assignee", "IPCR", "Application Year") are gone.
- **Docs.** New `docs/notebook_inventory.md` maps each old notebook to what was kept, fixed or dropped. `plotly` is added to `environment.yml`.

## v1.1 (31 Oct 2026)
- **Country labels.** Income group and Global North/South for funders and recipients now come from `data/reference/country_classification.csv`.
  - The recipient file had Switzerland, Sweden and Spain as "Global South / Upper middle income".
  - Global South recipients go from 6.7% to 2.1% of funding, and high-income recipients from 93.2% to 97.8%.
- **EU funders.** The European Commission and the European Research Council are coded as funder country "European Union" instead of Belgium.
- **New tables.**
  - S11: Global South recipients by country. China is 73% of the Global South total.
  - S12: domestic vs cross-border funding. 88.7% of funding stays in the funder's country.
  - S13: the largest cross-border funders.
- **Key numbers.** `key_numbers.json` gains the high-income, Global South, China and domestic shares.

## v1.0 (31 Oct 2026)
- **Notebooks.** The 2024–25 Colab notebooks are replaced by three notebooks (preprocessing, topic modelling, main analysis).
- **Fixes.**
  - The growth rate now uses USD amounts.
  - Gender groups no longer overlap.
  - Institution lists keep their order, with fractional counting per institution.
  - Topic coherence uses the correct word order.
  - Grants with duplicate text now take their twin's topic.
