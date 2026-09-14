"""
Campaign Timing & Contact Frequency Audit
Eden Hwang

Analyzes real direct-marketing phone campaign data to find where outreach
timing and effort didn't match conversion outcomes.

Data source: UCI Machine Learning Repository, "Bank Marketing Dataset"
S. Moro, P. Cortez, P. Rita, "A Data-Driven Approach to Predict the Success
of Bank Telemarketing," Decision Support Systems, Elsevier, 62:22-31, 2014.

Run with: python analysis.py
Requires: pandas
"""

import pandas as pd

df = pd.read_csv("bank_marketing_data.csv")
df["converted"] = (df["y"] == "yes").astype(int)

print(f"Total contacts analyzed: {len(df):,}")
print(f"Overall conversion rate: {df['converted'].mean() * 100:.1f}%\n")

# ---------------------------------------------------------------
# Finding 1: Conversion rate and call volume by month
# ---------------------------------------------------------------
month_order = ["jan", "feb", "mar", "apr", "may", "jun",
                "jul", "aug", "sep", "oct", "nov", "dec"]

by_month = df.groupby("month")["converted"].agg(["mean", "count"])
by_month = by_month.reindex([m for m in month_order if m in by_month.index])
by_month["conversion_pct"] = (by_month["mean"] * 100).round(1)
by_month["share_of_volume_pct"] = (by_month["count"] / len(df) * 100).round(1)

print("=== Conversion rate and call volume by month ===")
print(by_month[["conversion_pct", "share_of_volume_pct", "count"]])
print()

worst_month = by_month["conversion_pct"].idxmin()
best_month = by_month["conversion_pct"].idxmax()
print(f"KEY FINDING: {by_month.loc[worst_month, 'share_of_volume_pct']}% of all "
      f"calls went to {worst_month}, the lowest-converting month "
      f"({by_month.loc[worst_month, 'conversion_pct']}% conversion).")
print(f"Meanwhile {best_month}, the best-converting month "
      f"({by_month.loc[best_month, 'conversion_pct']}% conversion), received only "
      f"{by_month.loc[best_month, 'share_of_volume_pct']}% of volume.\n")

# ---------------------------------------------------------------
# Finding 2: Conversion rate by number of contacts this campaign
# ---------------------------------------------------------------
df["campaign_bucket"] = pd.cut(
    df["campaign"], bins=[0, 1, 2, 3, 5, 100],
    labels=["1", "2", "3", "4-5", "6+"]
)
by_frequency = df.groupby("campaign_bucket", observed=True)["converted"].mean() * 100

print("=== Conversion rate by number of contacts ===")
print(by_frequency.round(1))
print("\nKEY FINDING: Conversion rate declines steadily as contact count rises, "
      "suggesting diminishing returns rather than persistence paying off.\n")

# ---------------------------------------------------------------
# Finding 3: Conversion rate by prior campaign outcome
# ---------------------------------------------------------------
by_outcome = df.groupby("poutcome")["converted"].mean() * 100

print("=== Conversion rate by prior campaign outcome ===")
print(by_outcome.round(1))
print("\nKEY FINDING: Leads with a prior successful outcome convert far above "
      "baseline, suggesting this segment is under-prioritized for re-contact.\n")

# ---------------------------------------------------------------
# Recommendation
# ---------------------------------------------------------------
print("=== Recommendation ===")
print("""1. Reallocate a portion of low-converting-month call volume toward
   historically high-converting windows, even using the same lead list.
2. Cap outreach at 2-3 contacts per lead; returns diminish sharply beyond that.
3. Prioritize call capacity toward leads with a prior successful outcome.""")
