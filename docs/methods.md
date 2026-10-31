# Methods

## 1. Search (Dimensions, 13 Feb 2024, no date limit)
```
(title:(Bacteriophage OR Bacteriophages OR phage OR phages OR "phago virus" OR "phagovirus" OR siphophage* OR Microbacteriophage* OR Mycobacteriophage* OR Mycobacteriophage OR Microbacteriophage OR multiphage* OR multiphage OR "multi-phage*" OR "phage-based" OR "bacteriophage-based" OR phageome OR phagotherapy OR "Monophage Therapy" OR "Polyphage" OR Coliphage OR prophage OR staphylophage OR phageome OR PHAGOTHERAPY)) AND ((abstract:(therap* OR Therapy OR THERAPEUTIC OR treat* OR Treatment OR antibacterial OR antibacteria* OR "anti-bacterial" OR antimicrobial OR cocktail* OR cocktail OR prophylax* OR Prophylaxis OR Antifungal OR Antiviral OR PHAGOTHERAPY)) OR (title:(therap* OR Therapy OR THERAPEUTIC OR treat* OR Treatment OR antibacterial OR antibacteria* OR "anti-bacterial" OR antimicrobial OR cocktail* OR cocktail OR prophylax* OR Prophylaxis OR Antifungal OR Antiviral OR PHAGOTHERAPY)))
```

## 2. Enrichment
- **Institutions.** Harmonised with GRID/ROR in Dimensions, then checked by hand. Missing co-recipients were added.
- **Countries.** Each funder and recipient country is tagged with its World Bank income group (2023) and a Global North/South label.
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
- **Fractional counting.**
  - A grant with *k* recipient institutions gives 1/*k* of its amount to each one.
  - That share goes to the institution's country and income group.
  - Each grant has one funder.
- **Gender.**
  - Grants are put into exclusive groups by the genders of their named researchers: male only, female only, mixed, and no named researcher.
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
