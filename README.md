# HIT140 Assessment 2 – Assists Analysis

## Objective 1 – Assists

### Research Question

Is there a statistically significant difference in assist rates per 90 minutes between midfielders and forwards in the FIFA World Cup 2026?

### Why we chose this question

For our part of the project, we focused on creative output — specifically, assists. Assists are often associated with attacking players, but midfielders are frequently the primary creative outlet in modern tactical systems. We compared midfielders and forwards to see whether their assist rates actually differed.

We used assists per 90 minutes rather than total assists because players did not all play the same amount of time. This gives a fairer comparison between the two position groups.

### Data Source

The player-level FIFA World Cup 2026 assist data was obtained from FBref.

The original CSV export contained 499 records (including a two-row header and one blank footer row). After removing the footer row, 498 valid player records remained.

### Data Preparation

We focused on two position groups:

- MF – Midfielders
- FW – Forwards

Players with mixed position tags (e.g., FW,MF or MF,DF) were excluded so that each player represents a single, unambiguous position category.

Players who had played less than one 90-minute equivalent were excluded. This was done because an assist rate based on very little playing time can be unusually high and unstable.

After this filtering, the eligible population contained:

- 122 midfielders
- 48 forwards
- 170 players in total

Assists per 90 minutes were calculated using:

**Assists per 90 = Assists / 90s played**

### Sampling

The eligible players were divided into two strata based on playing position: midfielders and forwards.

We then used stratified random sampling to select:

- 40 midfielders
- 40 forwards

This produced a balanced sample of 80 players. A random seed of 42 was used so that the same sample can be reproduced when the analysis is run again.

### Hypotheses

**H0:** There is no difference in the average assist rate per 90 minutes between midfielders and forwards.

**H1:** There is a difference in the average assist rate per 90 minutes between midfielders and forwards.

### Descriptive Statistics

| Position | Players | Mean Ast/90 | Median | Standard Deviation |
|---|---:|---:|---:|---:|
| Midfielders | 40 | 0.133 | 0.000 | 0.246 |
| Forwards | 40 | 0.088 | 0.000 | 0.185 |

The sample shows that midfielders had a higher average assist rate than forwards.

### 95% Confidence Intervals

| Position | 95% Confidence Interval |
|---|---:|
| Midfielders | 0.054 – 0.212 |
| Forwards | 0.029 – 0.147 |

### Two-Sample t-Test

A Welch two-sample t-test was used to compare the average assist rates of the two groups.

- Significance level: **0.05**
- t-statistic: **0.925**
- p-value: **0.3581**

Because the p-value is greater than 0.05, we failed to reject the null hypothesis.

### Conclusion

Midfielders had a numerically higher average assist rate than forwards in the sample (0.133 compared with 0.088 assists per 90 minutes), but this difference was not statistically significant.

The p-value of 0.3581 is above the 0.05 significance level. Therefore, the sample does not provide statistically significant evidence of a difference in assist rates per 90 minutes between midfielders and forwards.

### Limitation

Assists are relatively uncommon, so many players had zero assists. This results in a skewed distribution of assist rates (both group medians are 0).

We reduced the effect of very small playing-time values by excluding players with less than one 90-minute equivalent, and by excluding players with ambiguous, mixed position tags. The analysis also uses a sample rather than all 170 eligible players, so the sample results may not exactly represent the full eligible population.

The analysis does not find a difference between the two groups in this sample, but this does not prove that playing position has no relationship with creative output; a larger sample or a different metric (e.g., key passes, expected assists) might reveal a different picture.

### Files

- `assists_analysis.py` – Python code used for data preparation, analysis and visualisation
- `assists_cleaned.csv` – final sampled dataset used for the analysis
- `assists_results.csv` – descriptive statistics and confidence intervals
- `assists_boxplot.png` – visualisation comparing the two groups
- `README.md` – description of the analysis

### How to Run

The raw FBref CSV dataset (`fbref_WC2026_Assists.csv`) should be placed in the main project folder, two levels above the Assists folder.

Run the analysis from the main project folder using:

```bash
python Objective_1\Assists\assists_analysis.py
```
