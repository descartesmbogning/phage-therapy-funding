"""Shared functions for the phage therapy funding analysis (1999-2023).

Every figure and table in the preprint is produced from one table:
data/processed/phage_funding_analysis.csv (802 grants, Dimensions export of
13 Feb 2024, screened and enriched), built by notebooks/01_preprocessing.ipynb.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# Column names used throughout
USD = "Funding amount in USD"
YEAR = "Start Year"
ORG = "Research Organization - standardized"
FUNDER = "Funder"
TOPIC = "Topic N°"
GENDER = "Gender"

PARTIAL_YEAR = 2023          # Dimensions indexes grants with a lag
TREND_YEARS = (1999, 2022)   # complete years used for growth estimates

TOPIC_LABELS = {
    "Bacteriophage Therapy and Infectious Disease Control": "Infectious disease control",
    "Bacterial Genetics and Mechanisms": "Bacterial genetics and mechanisms",
    "Antibiotic Resistance and Therapeutic Strategies": "Antibiotic resistance strategies",
    "Immunotherapy and Targeted Treatments": "Immunotherapy and targeted treatments",
    "Not Class.": "Unclassified",  # 1 grant after duplicates inherit their twin's topic
}
GENDER_LABELS = {"Male": "Male only", "Female": "Female only",
                 "Female;Male": "Mixed", "Male;Female": "Mixed"}

# Validated categorical palette (fixed order; dataviz reference palette, light mode)
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
NEUTRAL = "#9a9890"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def load(path: str | Path) -> pd.DataFrame:
    """Load the analysis table and add clean helper columns."""
    d = pd.read_csv(path)
    d = d[(d[YEAR] >= 1999) & (d[YEAR] <= 2023)].copy()
    d["topic"] = d[TOPIC].map(TOPIC_LABELS).fillna("Unclassified")
    d["team_gender"] = d[GENDER].map(GENDER_LABELS).fillna("No named researcher")
    if "n_researchers" not in d:
        d["n_researchers"] = d["Researchers"].apply(_count_people)
    return d


def _count_people(s) -> int:
    if pd.isna(s):
        return 0
    return len([p for p in str(s).split(",") if p.strip() and p.strip().lower() != "nan"])


def split_list(value, sep: str = ";") -> list[str]:
    if pd.isna(value):
        return []
    return [v.strip() for v in str(value).split(sep) if v.strip() and v.strip().lower() != "nan"]


# ---------------------------------------------------------------- trends
def yearly(d: pd.DataFrame) -> pd.DataFrame:
    y = d.groupby(YEAR).agg(grants=("Grant ID", "count"), usd=(USD, "sum"))
    return y.reindex(range(1999, 2024), fill_value=0)


def loglinear_growth(series: pd.Series, years=TREND_YEARS) -> dict:
    """Annual growth from a log-linear fit, with a 95% CI (replaces endpoint CAGR)."""
    s = series.loc[years[0]:years[1]]
    t = np.asarray(s.index) - years[0]
    coef, cov = np.polyfit(t, np.log(s.values), 1, cov=True)
    b, se = coef[0], np.sqrt(cov[0, 0])
    pct = lambda x: round((np.exp(x) - 1) * 100, 1)
    return {"annual_growth_pct": pct(b), "ci_low": pct(b - 1.96 * se), "ci_high": pct(b + 1.96 * se),
            "years": f"{years[0]}-{years[1]}"}


def endpoint_cagr(series: pd.Series, first: int, last: int) -> float:
    """Classic CAGR with the correct number of intervals (last - first)."""
    return round(((series[last] / series[first]) ** (1 / (last - first)) - 1) * 100, 1)


def by_period(d: pd.DataFrame) -> pd.DataFrame:
    p = pd.cut(d[YEAR], [1998, 2008, 2015, 2023], labels=["1999-2008", "2009-2015", "2016-2023"])
    g = d.groupby(p, observed=True)[USD]
    out = pd.DataFrame({
        "Grants": g.count(),
        "Total (USD M)": (g.sum() / 1e6).round(1),
        "Median (USD)": g.median().round(0),
        "Q1 (USD)": g.quantile(0.25).round(0),
        "Q3 (USD)": g.quantile(0.75).round(0),
    })
    out.loc["All years"] = [len(d), round(d[USD].sum() / 1e6, 1), d[USD].median(),
                            d[USD].quantile(.25), d[USD].quantile(.75)]
    out.index.name = "Period"
    return out


# ---------------------------------------------------------------- fractional counting
def fractional(d: pd.DataFrame, col: str, sep: str = ";") -> pd.DataFrame:
    """Split each grant's amount equally across the listed entities so totals add up."""
    rows = []
    for gid, amt, val in zip(d["Grant ID"], d[USD], d[col]):
        items = split_list(val, sep)
        for it in items:
            rows.append((gid, it, amt / len(items), 1 / len(items)))
    f = pd.DataFrame(rows, columns=["Grant ID", col, "usd_frac", "grant_frac"])
    out = f.groupby(col).agg(grants_full=("Grant ID", "nunique"), grants_frac=("grant_frac", "sum"),
                             usd_frac=("usd_frac", "sum"))
    out["share_usd"] = out["usd_frac"] / d[USD].sum()
    return out.sort_values("usd_frac", ascending=False)


def top_funders(d: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    g = d.groupby(FUNDER).agg(**{"Country": ("Funder Country", "first"), "Grants": ("Grant ID", "count"),
                                 "Total (USD M)": (USD, "sum")})
    g["Share (%)"] = (g["Total (USD M)"] / d[USD].sum() * 100).round(1)
    g["Total (USD M)"] = (g["Total (USD M)"] / 1e6).round(1)
    return g.sort_values("Total (USD M)", ascending=False).head(n)


def fractional_aligned(d: pd.DataFrame, list_col: str, org_col: str = "receiver_org_list") -> pd.DataFrame:
    """Fractional counting per recipient institution.

    `list_col` holds one value per institution, in the same order as `org_col`
    (built by src/preprocess.py). A grant with k institutions gives 1/k of its amount
    to each institution, and that share goes to the institution's category.
    """
    rows = []
    for gid, amt, orgs, vals in zip(d["Grant ID"], d[USD], d[org_col], d[list_col]):
        o = split_list(orgs)
        v = str(vals).split(";") if isinstance(vals, str) else []
        if not o:
            continue
        for i in range(len(o)):
            val = v[i].strip() if i < len(v) and v[i].strip() not in ("", "nan") else "Not classified"
            rows.append((gid, val, amt / len(o), 1 / len(o)))
    f = pd.DataFrame(rows, columns=["Grant ID", list_col, "usd_frac", "grant_frac"])
    out = f.groupby(list_col).agg(grants_full=("Grant ID", "nunique"), grants_frac=("grant_frac", "sum"),
                                  usd_frac=("usd_frac", "sum"))
    out["share_usd"] = out["usd_frac"] / d[USD].sum()
    return out.sort_values("usd_frac", ascending=False)


def top_recipients(d: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    f = fractional(d, "receiver_org_list")
    f["Total (USD M, fractional)"] = (f["usd_frac"] / 1e6).round(2)
    f = f.rename(columns={"grants_full": "Grants"})
    return f[["Grants", "Total (USD M, fractional)"]].head(n)


# ---------------------------------------------------------------- gender
def gender_table(d: pd.DataFrame) -> pd.DataFrame:
    order = ["Male only", "Female only", "Mixed", "No named researcher"]
    g = d.groupby("team_gender")
    out = pd.DataFrame({
        "Grants": g.size(),
        "Total (USD M)": (g[USD].sum() / 1e6).round(1),
        "Share of funding (%)": (g[USD].sum() / d[USD].sum() * 100).round(1),
        "Mean (USD)": g[USD].mean().round(0),
        "Median (USD)": g[USD].median().round(0),
        "Median team size": g["n_researchers"].median(),
    }).reindex(order)
    out.index.name = "Team composition"
    return out


def gender_tests(d: pd.DataFrame) -> pd.DataFrame:
    """Mann-Whitney tests and a log-amount regression with controls."""
    from scipy import stats
    import statsmodels.formula.api as smf

    e = d[d["team_gender"].isin(["Male only", "Female only", "Mixed"])].copy()
    e["log_usd"] = np.log(e[USD])
    e["us_funder"] = e["Funder Country"].astype(str).str.contains("United States").astype(int)
    e["log_team"] = np.log(e["n_researchers"].clip(lower=1))
    e["g"] = pd.Categorical(e["team_gender"], ["Male only", "Female only", "Mixed"])
    m = smf.ols("log_usd ~ C(g) + log_team + us_funder + Q('Start Year')", data=e).fit(cov_type="HC1")
    male = e.loc[e.team_gender == "Male only", USD]
    rows = []
    for grp in ["Female only", "Mixed"]:
        key = f"C(g)[T.{grp}]"
        rows.append({
            "Comparison": f"{grp} vs Male only",
            "Mann-Whitney p": stats.mannwhitneyu(e.loc[e.team_gender == grp, USD], male).pvalue,
            "Adjusted difference (%)": (np.exp(m.params[key]) - 1) * 100,
            "95% CI low (%)": (np.exp(m.conf_int().loc[key, 0]) - 1) * 100,
            "95% CI high (%)": (np.exp(m.conf_int().loc[key, 1]) - 1) * 100,
            "Regression p": m.pvalues[key],
        })
    out = pd.DataFrame(rows).set_index("Comparison").round(3)
    out.attrs["n"] = int(m.nobs)
    out.attrs["controls"] = "log team size, US funder, start year; robust (HC1) errors"
    return out


# ---------------------------------------------------------------- engagement
def classify_engagement(d: pd.DataFrame, col: str = "Researchers", sep: str = ",",
                        span: bool = False) -> pd.Series:
    """Last-period label per entity, same rules as the patent-study function.

    span=False: an entity is active only in a grant's start year (original rule).
    span=True:  active in every year from start to end year (sensitivity check).
    """
    active: dict[str, set[int]] = {}
    for _, r in d.iterrows():
        s = int(r[YEAR])
        e = int(r["End Year"]) if span and pd.notna(r["End Year"]) else s
        years = range(s, min(max(e, s), PARTIAL_YEAR) + 1)
        for ent in split_list(r[col], sep):
            active.setdefault(ent, set()).update(years)
    last_period = PARTIAL_YEAR
    labels = {}
    for ent, ys in active.items():
        first, last = min(ys), max(ys)
        before = first < last
        if last == last_period:
            labels[ent] = "Continuant" if before else "Newcomer"
        else:
            labels[ent] = "Terminator" if before else "Transient"
    return pd.Series(labels, name="label")


def engagement_summary(d: pd.DataFrame) -> pd.DataFrame:
    a = classify_engagement(d, span=False).value_counts()
    b = classify_engagement(d, span=True).value_counts()
    out = pd.DataFrame({"Start year only (n)": a, "Full grant span (n)": b}).fillna(0).astype(int)
    for c in list(out.columns):
        out[c.replace("(n)", "(%)")] = (out[c] / out[c].sum() * 100).round(1)
    grants_per_person = d["Researchers"].apply(split_list, sep=",").explode().dropna().value_counts()
    out.attrs["single_grant_share"] = round((grants_per_person == 1).mean() * 100, 1)
    out.attrs["n_researchers"] = int(len(grants_per_person))
    return out


# ---------------------------------------------------------------- data quality
def missingness(d: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    m = d[cols].isna().sum()
    return pd.DataFrame({"Present": len(d) - m, "Missing": m, "Missing (%)": (m / len(d) * 100).round(1)})
