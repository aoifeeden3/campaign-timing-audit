# Campaign Timing & Contact Frequency Audit

Self-directed analytics project by **Eden Hwang**. Not affiliated with any employer — built using a public academic dataset to practice marketing analytics skills.

**Live interactive dashboard (Tableau Public):** https://public.tableau.com/app/profile/eden.hwang/viz/CampaignTimingContactFrequencyAudit/CampaignTimingContactFrequencyAudit

## The finding

Auditing 4,521 real direct-marketing phone contacts, I found that **31% of all outreach happened in the single worst-converting month (May, 6.7% conversion)**, while the best-converting month (October, 46.2% conversion) received under 2% of call volume. That's a budget-allocation mismatch a standard planning brief wouldn't catch.

Two supporting patterns:
- Conversion rate declines steadily as contact frequency increases (13.8% at 1 contact → 7.2% at 6+), suggesting audience fatigue rather than persistence paying off.
- Leads with a prior successful campaign outcome convert at 64.3%, over 5x the baseline — a clear signal this segment is under-prioritized for re-contact.

## Recommendation

1. Reallocate call volume from low-converting months toward historically strong windows (Sept/Oct/Dec), even using the same lead list.
2. Cap outreach at 2-3 contacts per lead — returns diminish sharply beyond that point.
3. Prioritize call capacity toward leads with a prior successful outcome.

## Data source

UCI Machine Learning Repository, *Bank Marketing Dataset*
S. Moro, P. Cortez, P. Rita, "A Data-Driven Approach to Predict the Success of Bank Telemarketing," *Decision Support Systems*, Elsevier, 62:22-31, June 2014.

Public dataset used for skill-building only — not real campaign data from any employer. All analysis, findings, and the dashboard design are original.

## Files

- `analysis.py` — Python script (pandas) that reproduces every finding above
- `bank_marketing_data.csv` — the dataset
- Dashboard built in Tableau Public (linked above)

## Run it yourself

```
pip install pandas
python analysis.py
```
