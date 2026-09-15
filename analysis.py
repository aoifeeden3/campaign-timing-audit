"""
The Frequency Ceiling — marketing A/B test analysis
=====================================================

Does a paid ad campaign beat doing nothing, how much exposure is enough
before returns flatten, and when should delivery be scheduled?

Dataset: "Marketing A/B Testing" (Faviovaz, via Kaggle)
https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing

Download the CSV from the link above and place it at data/marketing_AB.csv
before running this script. Not included in this repo — see Kaggle's
terms of use for the dataset.

Usage:
    pip install -r requirements.txt
    python analysis.py
"""

import numpy as np
import pandas as pd
from scipy import stats

DATA_PATH = "data/marketing_AB.csv"


def load_data(path=DATA_PATH):
    df = pd.read_csv(path, index_col=0)
    df.columns = [c.strip() for c in df.columns]
    df["converted"] = df["converted"].astype(bool)
    return df


def ab_test(df):
    """Two-proportion z-test comparing conversion rate: ad group vs. psa control."""
    ad = df.loc[df["test group"] == "ad", "converted"]
    psa = df.loc[df["test group"] == "psa", "converted"]

    n_ad, n_psa = len(ad), len(psa)
    x_ad, x_psa = int(ad.sum()), int(psa.sum())
    p_ad, p_psa = x_ad / n_ad, x_psa / n_psa

    # pooled z-test for significance
    p_pool = (x_ad + x_psa) / (n_ad + n_psa)
    se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / n_ad + 1 / n_psa))
    z = (p_ad - p_psa) / se_pool
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    # unpooled SE for the confidence interval on the difference
    se_diff = np.sqrt(p_ad * (1 - p_ad) / n_ad + p_psa * (1 - p_psa) / n_psa)
    diff = p_ad - p_psa
    ci = (diff - 1.96 * se_diff, diff + 1.96 * se_diff)

    incremental_conversions = diff * n_ad

    print("=" * 60)
    print("1. DOES THE AD WORK AT ALL?")
    print("=" * 60)
    print(f"  n (ad)          = {n_ad:,}")
    print(f"  n (psa control) = {n_psa:,}")
    print(f"  conversion (ad)  = {p_ad:.4%}")
    print(f"  conversion (psa) = {p_psa:.4%}")
    print(f"  absolute lift    = {diff * 100:.2f} points")
    print(f"  relative lift    = {(p_ad / p_psa - 1) * 100:.1f}%")
    print(f"  z-statistic      = {z:.2f}")
    print(f"  p-value          = {p_value:.2e}")
    print(f"  95% CI on lift   = [{ci[0]*100:.2f}, {ci[1]*100:.2f}] points")
    print(f"  incremental conversions ≈ {incremental_conversions:,.0f}")
    print()


def dose_response(df):
    """Conversion rate by total ad exposures received (ad group only)."""
    ad = df[df["test group"] == "ad"].copy()

    bins = [0, 5, 10, 20, 50, 100, 200, 500, ad["total ads"].max() + 1]
    labels = ["1-5", "6-10", "11-20", "21-50", "51-100", "101-200", "201-500", "501+"]
    ad["bucket"] = pd.cut(ad["total ads"], bins=bins, labels=labels, include_lowest=True)

    summary = ad.groupby("bucket", observed=True).agg(
        n=("converted", "size"), conversion_rate=("converted", "mean")
    )

    print("=" * 60)
    print("2. HOW MUCH EXPOSURE IS ENOUGH?")
    print("=" * 60)
    print(summary.assign(conversion_rate=lambda d: (d["conversion_rate"] * 100).round(2)))

    heavy = ad[ad["total ads"] > 100]
    print(f"\n  share of ad group seeing >100 ads = {len(heavy) / len(ad):.1%}")
    print(f"  their conversion rate             = {heavy['converted'].mean():.2%}")
    print(f"  (overall ad group rate            = {ad['converted'].mean():.2%})")
    print()


def timing(df):
    """Conversion rate by day and hour of peak ad delivery (ad group, 8am-11pm only)."""
    ad = df[(df["test group"] == "ad") & (df["most ads hour"] >= 8)].copy()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    pivot_rate = ad.pivot_table(
        index="most ads day", columns="most ads hour", values="converted", aggfunc="mean"
    ).reindex(day_order)
    pivot_n = ad.pivot_table(
        index="most ads day", columns="most ads hour", values="converted", aggfunc="size"
    ).reindex(day_order)

    flat = pivot_rate.stack().rename("rate").reset_index()
    flat["n"] = pivot_n.stack().values
    flat = flat.rename(columns={"most ads day": "day", "most ads hour": "hour"})

    print("=" * 60)
    print("3. WHEN SHOULD IT RUN?")
    print("=" * 60)
    print("  restricted to 8am-11pm cells (n >= ~1,800) to avoid noisy overnight hours\n")
    print("  Top 5 windows:")
    print(flat.sort_values("rate", ascending=False).head(5).to_string(index=False,
          formatters={"rate": "{:.2%}".format}))
    print("\n  Bottom 5 windows:")
    print(flat.sort_values("rate").head(5).to_string(index=False,
          formatters={"rate": "{:.2%}".format}))
    print()


def main():
    df = load_data()
    print(f"\nLoaded {len(df):,} rows from {DATA_PATH}\n")
    ab_test(df)
    dose_response(df)
    timing(df)


if __name__ == "__main__":
    main()
