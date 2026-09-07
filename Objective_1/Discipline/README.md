# HIT140 Assessment 2 – Discipline Analysis

## Objective 1 – Discipline

### Research Question

Is there a statistically significant difference in yellow-card rates per 90 minutes between defenders and midfielders in the FIFA World Cup 2026?

### Why we chose this question

For our part of the project, we focused on player discipline. We compared defenders and midfielders to see whether their yellow-card rates differed.

We used yellow cards per 90 minutes rather than total yellow cards because players did not all play the same amount of time. This gives a fairer comparison between the two position groups.

### Data Source

The player-level FIFA World Cup 2026 data was obtained from FBref.

The original Excel dataset contained 1,042 records. After removing three records that were not player records, 1,039 valid player records remained.

### Data Preparation

We focused on two position groups:

- DF – Defenders
- MF – Midfielders

Players who had played less than one 90-minute equivalent were excluded. This was done because a yellow-card rate based on very little playing time can be unusually high and unstable.

After this filtering, the eligible population contained:

- 253 defenders
- 254 midfielders
- 507 players in total

Yellow cards per 90 minutes were calculated using:

**Yellow cards per 90 = Yellow cards / 90s played**

### Sampling

The eligible players were divided into two strata based on playing position: defenders and midfielders.

We then used stratified random sampling to select:

- 100 defenders
- 100 midfielders

This produced a balanced sample of 200 players. A random seed of 42 was used so that the same sample can be reproduced when the analysis is run again.

### Hypotheses

**H0:** There is no difference in the average yellow-card rate per 90 minutes between defenders and midfielders.

**H1:** There is a difference in the average yellow-card rate per 90 minutes between defenders and midfielders.

### Descriptive Statistics

| Position | Players | Mean YC/90 | Median | Standard Deviation |
|---|---:|---:|---:|---:|
| Defenders | 100 | 0.106 | 0.000 | 0.208 |
| Midfielders | 100 | 0.180 | 0.000 | 0.274 |

The sample shows that midfielders had a higher average yellow-card rate than defenders.

### 95% Confidence Intervals

| Position | 95% Confidence Interval |
|---|---:|
| Defenders | 0.065 – 0.148 |
| Midfielders | 0.126 – 0.234 |

### Two-Sample t-Test

A Welch two-sample t-test was used to compare the average yellow-card rates of the two groups.

- Significance level: **0.05**
- t-statistic: **-2.142**
- p-value: **0.0335**

Because the p-value is less than 0.05, we rejected the null hypothesis.

### Conclusion

Midfielders had a higher average yellow-card rate than defenders (0.180 compared with 0.106 cards per 90 minutes).

The p-value of 0.0335 is below the 0.05 significance level. Therefore, the sample provides statistically significant evidence of a difference in yellow-card rates per 90 minutes between defenders and midfielders.

### Limitation

Yellow cards are relatively uncommon, so many players had zero yellow cards. This results in a skewed distribution of yellow-card rates.

We reduced the effect of very small playing-time values by excluding players with less than one 90-minute equivalent. The analysis also uses a sample rather than all 507 eligible players, so the sample results may not exactly represent the full eligible population.

The analysis identifies a difference between the two groups but does not prove that playing position causes differences in disciplinary behaviour.

### Files

- `discipline_analysis.py` – Python code used for data preparation, analysis and visualisation
- `discipline_cleaned.csv` – final sampled dataset used for the analysis
- `discipline_results.csv` – descriptive statistics and confidence intervals
- `discipline_boxplot.png` – visualisation comparing the two groups
- `README.md` – description of the analysis

### How to Run

The raw FBref Excel dataset should be placed in the main project folder, two levels above the Discipline folder.

Run the analysis from the main project folder using:

```bash
python Objective_1\Discipline\discipline_analysis.py