# Changelog

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
