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
  - Main model (v1.5): OLS of log(amount) on group, log team size, log grant length (years), start year, funder (funders with fewer than 10 grants pooled) and topic, with HC1 robust errors. The model also reports the amount per year of grant, and the v1.0–v1.4 model (team size, US funder, start year) for comparison (Table S3).
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

## 6. Robustness (notebook 06, v1.5)
- **Screening flow.** Counts for every step are read from the screening columns of the raw Dimensions export (`includes ?`, `funding?`), so the flow diagram is generated, not typed (Figure S12, Table S30). Five records are coded −1 in `includes ?`; they are excluded with the 386 coded 0.
- **Award types.** Each record is classed as a research grant, a training award (studentship, scholarship, fellowship, thesis, graduate-programme record) or capacity funding (USDA formula funds) from its programme name and source link (`src/robustness.py`, `award_type`). 43% of the grants without an amount are training awards, against 8% of grants with one (Table S31).
- **Grants without an amount.** The 272 relevant grants with no amount (start year 1999–2023) enter three checks:
  - count-based shares, each grant counted once and split equally across its recipient countries (Table S32);
  - imputation: each missing amount takes the median (central), 25th percentile (low) or 75th percentile (high) of priced grants from the same funder (at least 3), else the same funder country and award type, else the same award type. Training awards are set to 0 in the low and central scenarios and to the 25th percentile of priced training awards in the high scenario (Table S33);
  - recovery: a private worksheet lists each grant with its funder page; amounts entered by hand in `data/raw/recovered_amounts.csv` are used when present.

  The recipient countries of these grants come from the Dimensions export, with spelling cleaned. Seven countries not in the reference table were added (World Bank FY2024 income group; Qatar's North/South label differs between sources).
- **Projects.** Records with the same funder and the same English (translated) title whose years follow on are merged into one project, with amounts summed (Table S34). Using the translated title stops grants with non-Latin titles from being merged by mistake.
- **Other definitions.**
  - Amounts spread evenly over grant years.
  - Income group at grant start: China lower-middle income until 2009 and Thailand until 2010. These years were entered by hand and should be checked against the World Bank historical classification (OGHIST).
  - OECD DAC list of ODA recipients (2024–25) as an alternative to Global South.
  - Engagement: the share of researchers with one active year among those first seen 2001–2019, and the share with a single grant.
  - Topic shares from the refitted model's topic probabilities (Table S36).
  - The gender model without funders in Japan and China (name inference is less reliable there) and without training awards (Table S35).
- **Validation and cross-checks (to complete).**
  - The notebook writes private samples for a second screener (15% of 1,521, stratified), hand-coding of topics (100 grants) and checking of inferred gender (100 names, stratified by country), and reports Cohen's kappa once they are filled.
  - Public templates hold yearly NIH totals for comparison with NIH RePORTER and World Bank price level ratios for a PPP check.
- **Summary.** Figure S13 and Table S37 show each headline under each check, with the rule used to judge whether its conclusion holds.
