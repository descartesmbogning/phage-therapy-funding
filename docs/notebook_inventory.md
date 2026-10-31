# The 2024–25 Colab notebooks: what was kept

The first version of this analysis lived in about twenty Colab notebooks. This page explains what each one did and what happened to its code in this repository. Two of them are kept unchanged in `archive/2024_colab/`; they were written for Colab and do not run as they are. The others stay in the authors' Google Drive, because their saved outputs contain grant-level data, and are listed here for the record. Cell numbers refer to each notebook as it was in October 2026.

## What each notebook did

| Notebook | Role | Now |
|---|---|---|
| Key_Players_phage_therapy_funding | Built the analysis table: joined grants, LDA topics, gender and institution metadata, then saved `phage_funding_preprocesse` and VOSviewer files | `src/preprocess.py`, `01_preprocessing` |
| Patent_TopicModeling_phage_funding | LDA: choice of k, word clouds, topic similarity, topic trends | `src/topics.py`, `02_topic_modelling`; similarity redrawn as Figure S5 |
| all_stats_phage_therapy_funding | The analysis template: trends, topics, gender, funders, recipients, collaborations, flows, heatmaps | `03_main_analysis`, `04_supplementary_figures` |
| ARTS / BGM / BTIDC / ITT_all_stats | The same template run on one topic each | Replaced by functions called per subset |
| all_female_stats / male_stats | The same template on grants with at least one woman (297) or at least one man (542). The 95 mixed teams appear in both | Replaced by exclusive gender groups (Table 4) |
| data_analysis_phage_therapy_funding | all_stats plus engagement (overall, by gender, by topic). The latest and most complete version | Reference for Figures S2–S4 and S6–S9 |
| trend_entities / trend_topics_and_gender_based_engagement | Earlier drafts of the engagement analysis | Superseded; see the bugs below |
| evolving, prep, collab_network, extract_biomedical, grant_extract_diseases | Early trend figures, cleaning, collaboration networks, disease and organism extraction | Trends and cleaning replaced. Network and text-mining code kept for later work, not used in the preprint |

## Code: kept, fixed or dropped

| Old function | Decision | New home |
|---|---|---|
| `preprocess_entity_data` | Kept | `phagefund.explode_entities` |
| `classify_entities_func`, `count_entity_classifications` | Fixed | `phagefund.engagement_by_year`, `phagefund.classify_engagement` |
| `plot_entity_trends` | Fixed: years on the x-axis, 0 instead of gaps, correct labels | `figures.engagement_panel` |
| `count_gender_by_year` | Kept | `phagefund.researchers_by_gender_year` |
| `group_and_pivot_Assignee`, `plot_top_50_heatmap` | Fixed: counts or shares instead of dollar amounts; patent labels removed | `phagefund.row_shares`, `figures.heatmap` |
| `create_sankey_diagrams_top20` | Kept | `phagefund.country_flows`, `figures.sankey_html` |
| `jaccard_similarity` | Kept | `phagefund.jaccard_matrix`, `figures.topic_dendrogram` |
| `calculate_cagr`, `calculate_agr` | Dropped: wrong number of intervals and original currency | `phagefund.loglinear_growth` |
| `clean_entities` | Dropped: `set()` changed the order of names | `phagefund.explode_entities` |
| `extract_first_last_years` | Dropped: covered by the engagement labels | |
| `analyze_collaborations`, `calculate_centrality_measures`, `visualize_graph_pyvis`, `draw_chord_diagram` | Kept for a later network paper | not in v1 |
| `extract_biomedical_data`, `extract_diseases`, `extract_taxons` | Kept for later text mining; needs checking against hand-labelled grants | not in v1 |

## Bugs found in the old notebooks

1. **Female funder plot = male funder plot.** In trend_entities (cell 314) and trend_topics, the "Fund to female" section used the male data, because a variable was not reset. It was fixed in data_analysis (cell 397).
2. **Topic × gender sections read every grant.** In trend_topics_and_gender_based_engagement, six sections per topic (receiver countries, funders and funder countries, each for men and for women) started from the full dataset. The four topics therefore show the same numbers. These 24 plots are not redrawn.
3. **Every topic section read one topic.** In an older copy of trend_topics, each per-topic section used the infectious-disease subset. This was fixed in later versions.
4. **Axes and labels.** The engagement plots used the row index as the x-axis in one version. Zero counts showed as gaps. Funder plots were labelled "Researchers".
5. **No figure was saved by code.** All `savefig` lines were commented out, and the target folder was the patent paper's. In this repository every figure is written to `outputs/figures` by the notebooks.

## A note on the engagement labels

The old plots counted each entity once, by its label in its *last* active year. This makes "Newcomer" almost disappear: for example, 0 newcomer recipient countries. Figures S8 and S9 instead show labels year by year. Table S7 compares the start-year and full-grant-span definitions. Everyone active in 2023 is labelled Continuant or Newcomer, because later years are not observed.
