# HIT140 Assessment 2 – Discipline Analysis

# Objective 1 – Discipline

# Research Question

Is there a statistically significant difference in yellow-card rates per 90 minutes between defenders and midfielders in the FIFA World Cup 2026?

# Why we chose this question

For this part of the project, we wanted to look at player discipline. We compared defenders and midfielders because these players have different roles on the field, and this may be reflected in the number of yellow cards they receive.

Instead of comparing the total number of yellow cards, we used yellow cards per 90 minutes. This gives a fairer comparison because players did not all play the same amount of time.

# Data Source

The player data was obtained from FBref's FIFA World Cup 2026 statistics.

The original Excel file contained 1,042 records. After checking the data, three rows were found to be non-player records and were removed. This left 1,039 player records for analysis.

The original Excel file is kept locally and is not uploaded to GitHub because it is listed in `.gitignore`.

# Data Preparation

We focused on two position groups:

- DF – Defenders
- MF – Midfielders

We removed players who had played less than one 90-minute equivalent. This was done because a player who only played a few minutes could have an unusually high yellow-card rate even from receiving only one card.

For example, one yellow card in a very small amount of playing time can produce a misleading per-90 rate.

After this filtering, we had 507 players:

- 253 defenders
- 254 midfielders

We calculated yellow cards per 90 minutes using:

**Yellow cards per 90 = Yellow cards / 90s played**

# Sampling

Our analysis population was the defenders and midfielders in the cleaned FIFA World Cup 2026 player dataset.

Rather than taking a smaller random sample, we used all players who met our eligibility rule of at least one 90-minute equivalent. This gave us 507 observations and allowed us to keep as much of the available relevant data as possible.

# Hypotheses

H0: There is no difference in the average yellow-card rate per 90 minutes between defenders and midfielders.

H1: There is a difference in the average yellow-card rate per 90 minutes between defenders and midfielders.

# Descriptive Statistics

| Position | Players | Mean YC/90 | Median | Standard Deviation |
|---|---:|---:|---:|---:|
| Defenders | 253 | 0.115 | 0.000 | 0.208 |
| Midfielders | 254 | 0.154 | 0.000 | 0.272 |

The results show that midfielders had a higher average yellow-card rate than defenders.

# 95% Confidence Intervals

| Position | 95% Confidence Interval |
|---|---:|
| Defenders | 0.089 – 0.140 |
| Midfielders | 0.120 – 0.187 |

These intervals show the range of values around each group's estimated mean.

# Two-Sample t-Test

We used a Welch two-sample t-test to compare the average yellow-card rates of the two groups.

- Significance level: 0.05
- t-statistic: -1.814
- p-value: 0.0703

Because the p-value is greater than 0.05, we failed to reject the null hypothesis.

# Conclusion

Midfielders had a higher observed yellow-card rate than defenders (0.154 compared with 0.115 cards per 90 minutes). However, the difference was not statistically significant at the 5% level.

Therefore, based on this dataset, we do not have enough statistical evidence to say that defenders and midfielders had different yellow-card rates per 90 minutes.

# Limitation

Yellow cards are relatively uncommon, so many players had zero yellow cards. This makes the data uneven and somewhat skewed.

We reduced the effect of very small playing-time values by only including players who had played at least one 90-minute equivalent. However, the results should still be interpreted carefully.

Also, this analysis shows an association between playing position and yellow-card rate. It does not prove that a player's position causes them to receive more or fewer yellow cards.

# Files

- `discipline_analysis.py` – Python code used for the analysis
- `discipline_cleaned.csv` – cleaned data used in the analysis
- `discipline_results.csv` – calculated statistical results
- `discipline_boxplot.png` – visualisation of yellow-card rates
- `.gitignore` – keeps the raw Excel file out of the GitHub repository

# How to Run

Make sure the raw Excel dataset is in the same folder as the Python file, then run:

bash
python discipline_analysis.py