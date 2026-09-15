# The Frequency Ceiling

A marketing analytics case study: does a paid ad campaign actually beat doing nothing, how much ad exposure is enough before returns flatten, and when should delivery be scheduled?

**[Read the full write-up →](https://claude.ai/code/artifact/d50af0fb-918c-493b-9904-6b412f6c5d73)**

## About

This is a self-directed practice project, not client or employer work. I built it to practice the kind of question a paid-media or lifecycle marketing team asks about a campaign — is it working, how much exposure is enough, when should it run — using Python instead of a BI tool.

## Dataset

[Marketing A/B Testing](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing) (Faviovaz, via Kaggle) — 588,101 users, logging test group (ad/psa), whether they converted, total ad impressions received, and the day/hour each user got the most of them.

The CSV isn't included in this repo (see Kaggle's terms). Download it from the link above and save it as `data/marketing_AB.csv` before running the script.

## Key findings

- Ad-exposed users converted at 2.55% vs. 1.79% for the PSA control — a 43% relative lift (two-proportion z-test, p < 0.001, 95% CI on the lift: 0.60–0.94 points)
- Conversion climbs sharply with exposure up to roughly 150–200 ad views per user, then flattens — only 3.9% of the ad group saw more than 100 ads, but they convert at 17.1%
- Conversion rate by day/hour of peak delivery ranges from 1.5% to 4.6%; weekday early-to-mid afternoon and Sunday evening are strongest, weekend late morning is weakest

## Running it

```bash
pip install -r requirements.txt
python analysis.py
```

Prints every statistic used in the write-up: group sizes, the lift with its confidence interval and p-value, conversion rate by exposure bucket, and the top/bottom day-hour windows.

## Tools

Python, pandas, SciPy — matches my actual toolkit (Google Analytics, Python, and R from coursework). No Tableau or Power BI used or claimed here.

## Limitations

The ad/psa split is the one randomized comparison, so it supports a causal read. Total ad exposure and delivery timing were not randomly assigned, so the frequency and timing findings are observational — they could partly reflect who those users already were rather than a pure effect of the ads. A randomized frequency-cap test and a scheduling test would be the next step to isolate that. Full discussion in the write-up.

---
Eden Hwang · aoifeeden3@gmail.com · [LinkedIn](https://linkedin.com/in/edenjhwang)
