# Discipline Analysis

This analysis investigates whether yellow-card rates differ between defenders and midfielders in the FIFA World Cup 2026.
# Data Preparation

The original FBref dataset was cleaned by removing non-player records and irrelevant columns. Players who participated in less than one full 90-minute equivalent were excluded to reduce the effect of unstable yellow-card rates from very limited playing time.

The final analysis contains 507 players:

- 253 defenders
- 254 midfielders
## Analysis

Yellow cards were standardised as yellow cards per 90 minutes.

The analysis includes:

- Descriptive statistics
- 95% confidence intervals
- Welch two-sample t-test
- Boxplot visualisation

# Result

Defenders had a mean rate of 0.115 yellow cards per 90 minutes, compared with 0.154 for midfielders.

The Welch two-sample t-test produced:

- t = -1.814
- p = 0.0703

At the 0.05 significance level, the difference was not statistically significant.

# Conclusion

Although midfielders had a higher observed yellow-card rate, there was insufficient statistical evidence to conclude that yellow-card rates differed significantly between defenders and midfielders.   