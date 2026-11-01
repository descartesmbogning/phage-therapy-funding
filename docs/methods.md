# Methods

## 1. Search (Dimensions, 13 Feb 2024, no date limit)
```
(title:(Bacteriophage OR Bacteriophages OR phage OR phages OR "phago virus" OR "phagovirus" OR siphophage* OR Microbacteriophage* OR Mycobacteriophage* OR Mycobacteriophage OR Microbacteriophage OR multiphage* OR multiphage OR "multi-phage*" OR "phage-based" OR "bacteriophage-based" OR phageome OR phagotherapy OR "Monophage Therapy" OR "Polyphage" OR Coliphage OR prophage OR staphylophage OR phageome OR PHAGOTHERAPY)) AND ((abstract:(therap* OR Therapy OR THERAPEUTIC OR treat* OR Treatment OR antibacterial OR antibacteria* OR "anti-bacterial" OR antimicrobial OR cocktail* OR cocktail OR prophylax* OR Prophylaxis OR Antifungal OR Antiviral OR PHAGOTHERAPY)) OR (title:(therap* OR Therapy OR THERAPEUTIC OR treat* OR Treatment OR antibacterial OR antibacteria* OR "anti-bacterial" OR antimicrobial OR cocktail* OR cocktail OR prophylax* OR Prophylaxis OR Antifungal OR Antiviral OR PHAGOTHERAPY)))
```

## 2. Enrichment
- **Institutions.** Harmonised with GRID/ROR in Dimensions, then checked by hand. Missing co-recipients were added.
- **Countries.** Each funder and recipient country is tagged with its World Bank income group (2023) and a Global North/South label (World Population Review 2024).
  - **One table for all labels (since v1.1).** Labels come from one table, `data/reference/country_classification.csv`, used for funders and recipients alike.
  - **Earlier error.** The earlier hand-made recipient file labelled Switzerland, Sweden and Spain as Global South / upper-middle income.
  - **Contested labels.** Georgia, Russia, Ukraine and Singapore are labelled differently in different sources. They keep the source label and are flagged in the table.
  - **EU funders.** The European Commission and the European Research Council are coded as funder country "European Union".
- **Gender.** Researcher gender is inferred from first names with Gender API. Ambiguous names were checked by hand.

## 3. Topics (notebook 02)
1. **Text.** Title, abstract and keywords, using the English translations.
2. **Stopwords.** WordCloud list, NLTK stopwords in all languages, and "amp".
3. **Duplicates.** Exact duplicate texts are dropped.
4. **Lemmas.** Nouns, adjectives and verbs only (spaCy `en_core_web_md`).
5. **Term counts.** Tokens longer than 2 characters, `min_df=50`, `max_df=0.75`.
6. **LDA.** scikit-learn, online learning, `learning_offset=50`, seed 111.
7. **Choice of k.** k was picked by mean c_v coherence over the top 30 words, testing k = 2–12. The 2024 code passed the vocabulary to the coherence measure in the wrong order. The corrected curve also peaks at k = 5 (Figure S1).
8. **Labels.** Topics were labelled from their top words and the abstracts that fit each topic best.
   - 0: Bacterial genetics and mechanisms
   - 1: Antibiotic resistance strategies
   - 2: Immunotherapy and targeted treatments
   - 3: Near-empty, 1 grant, reported as Unclassified
   - 4: Infectious disease control
9. **Stability.** Refitting with five other seeds keeps 51–68% of grants in the same topic (Table S9). Results are reported for topic totals, not single grants.
10. **Duplicates in the results.** Grants whose text duplicated another grant take that grant's topic.

## 4. Analysis (notebook 03)
- **Growth.** A log-linear fit of yearly counts and USD totals over 1999–2022, reported as % per year with a 95% CI. 2023 is excluded from the fit because of indexing lag.
- **Domestic vs cross-border.** A grant is domestic when every recipient institution is in the funder's country (Table S12). By this whole-grant rule, 88.7% of funding is domestic. Splitting multi-country grants fractionally instead (1/*k* per institution) gives 91.4%, because 30 of the 65 cross-border grants also include a recipient in the funder's country.
- **Fractional counting.**
  - A grant with *k* recipient institutions gives 1/*k* of its amount to each one.
  - That share goes to the institution's country and income group.
  - Each grant has one funder.
- **Gender.**
  - Grants are put into exclusive groups by the genders of their named researchers: male only, female only, mixed, and gender unknown. "Gender unknown" covers 59 grants that list no researcher and 1 grant whose researchers' gender could not be inferred (labelled "no named researcher" before v1.4).
  - Groups are compared with Mann-Whitney tests.
  - An OLS model of log(amount) on group, log team size, US funder and start year is also fitted, with HC1 robust errors.
- **Engagement types.** Same rules as the patent study.
  - An entity is labelled in each year it is active:
    - **Newcomer:** not active before, active later, or first seen in 2023.
    - **Continuant:** active before and after.
    - **Terminator:** active before, not after.
    - **Transient:** active in one year only.
  - The summary uses each entity's last label.
  - Results are reported for two activity rules, start year only and the full grant span (Table S7), because the shares depend strongly on the rule.

## 5. Concentration, collaboration and sensitivity (notebook 05, v1.3)
- **Concentration.**
  - Herfindahl-Hirschman index (HHI): the sum of squared percentage shares of funding, on a 0–10,000 scale. It is computed for funders, funder countries, and recipient countries (fractional counting). By the usual convention, above 2,500 is highly concentrated and 1,500–2,500 moderately concentrated.
  - Gini coefficient and the share of funding received by the top 10% of recipient institutions (fractional counting). With 525 institutions, the top 10% is the 52 largest (10% rounded to the nearest whole institution); the 53 largest would receive 54.0%.
  - Shares of funding from US funders and from NIAID, for 1999–2008, 2009–2015 and 2016–2023 (by grant start year).
- **Collaboration.** Counts only, with no names: grants with more than one recipient institution, more than one recipient country, both Global North and Global South recipients; co-investigator pairs and pairs that share two or more grants.
- **Without NIAID.** Growth rates, the US share and the HHIs are re-estimated with NIAID grants removed.
- **Constant dollars.** Amounts are converted to 2023 USD with the annual average CPI-U (all items, U.S. city average, 1982–84 = 100), by grant start year (`data/reference/cpi_u_annual.csv`). 1999–2021 come from the BLS CPI-U historical table; 2022 (292.655) and 2023 (304.702) from BLS data as published by the Idaho Department of Labor. Dimensions had already converted other currencies to USD, so only US inflation is removed.
- **Corrections log.** The values quoted in the July 2025 draft are typed into `data/reference/draft_2025_values.csv` with the cause of each error and its fix; the corrected values are read from the repo outputs (Table S29, Figure S11).
