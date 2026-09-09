"""
FIFA World Cup 2026 - Goalkeeper Save Percentage

Analytic question:
On average, what save percentage do goalkeepers achieve at the FIFA
World Cup 2026, and is there a meaningful difference in save percentage
between goalkeepers who kept at least one clean sheet in the tournament
and those who never kept a clean sheet?
                           
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

RANDOM_SEED = 40

# 1. Data Wrangling

raw = pd.read_csv(
    "GoalkeeperRawData.csv",
    header=5,
    skip_blank_lines=False,
)

gk = raw[
    ["Player", "Squad", "Age", "MP", "Starts", "Min",
     "SoTA", "Saves", "Save%", "CS", "CS%"]
].copy()

gk.columns = [
    "player", "team", "age", "matches_played", "starts", "minutes",
    "shots_on_target_faced", "saves", "save_pct", "clean_sheets", "clean_sheet_pct"
]

numeric_cols = [
    "age", "matches_played", "starts", "minutes",
    "shots_on_target_faced", "saves", "save_pct",
    "clean_sheets", "clean_sheet_pct"
]
for col in numeric_cols:
    gk[col] = pd.to_numeric(gk[col], errors="coerce")


before = len(gk)
gk_clean = gk.dropna(subset=["save_pct"]).reset_index(drop=True)
removed = before - len(gk_clean)
print(f"Removed {removed} goalkeeper(s) with undefined Save% (0 shots faced).")
print(f"Clean dataset: {len(gk_clean)} goalkeepers.\n")

# 2. Data Preparation and sampling data

population = gk_clean.copy()
POP_N = len(population)
POP_MEAN = population["save_pct"].mean()
POP_STD = population["save_pct"].std(ddof=0)
print(f"Population size (goalkeepers with a defined Save%): {POP_N}")
print(f"Population mean Save%: {POP_MEAN:.2f}")
print(f"Population std dev Save%: {POP_STD:.2f}\n")

SAMPLE_SIZE = 32
sample = population.sample(
    n=SAMPLE_SIZE, random_state=RANDOM_SEED).reset_index(drop=True)
print(
    f"Random sample drawn: {len(sample)} goalkeepers (seed={RANDOM_SEED}).\n")
print(sample[["player", "team", "matches_played",
      "save_pct", "clean_sheets"]].to_string(index=False))
print()


# 3. Descriptive Statistics

desc = sample["save_pct"].describe()
sample_mean = sample["save_pct"].mean()
sample_std = sample["save_pct"].std(ddof=1)
sample_median = sample["save_pct"].median()
sample_min = sample["save_pct"].min()
sample_max = sample["save_pct"].max()
iqr = sample["save_pct"].quantile(0.75) - sample["save_pct"].quantile(0.25)

print("Descriptive statistics: sample Save% ")
print(f"n            : {len(sample)}")
print(f"Mean         : {sample_mean:.2f}%")
print(f"Median       : {sample_median:.2f}%")
print(f"Std dev      : {sample_std:.2f}")
print(f"Min / Max    : {sample_min:.1f}% / {sample_max:.1f}%")
print(f"IQR          : {iqr:.2f}\n")


# 4. Confidence Interval for the population mean

confidence = 0.95
df_ci = len(sample) - 1
t_crit = stats.t.ppf((1 + confidence) / 2, df_ci)
standard_error = sample_std / np.sqrt(len(sample))
margin_of_error = t_crit * standard_error
ci_lower = sample_mean - margin_of_error
ci_upper = sample_mean + margin_of_error

print(" 95% Confidence interval for population mean Save% ")
print(f"t-critical (df={df_ci}): {t_crit:.3f}")
print(f"Standard error: {standard_error:.3f}")
print(f"95% CI: ({ci_lower:.2f}%, {ci_upper:.2f}%)")
print(f"(For reference, the true population mean computed from all "
      f"{POP_N} goalkeepers is {POP_MEAN:.2f}%, which falls inside this interval.)\n")


# 5. TWO-SAMPLE T-TEST

group_clean_sheet = sample.loc[sample["clean_sheets"] >= 1, "save_pct"]
group_no_clean_sheet = sample.loc[sample["clean_sheets"] == 0, "save_pct"]

print("Two-sample t-test: Save% by clean-sheet status ")
print(f"Clean-sheet group    : n={len(group_clean_sheet)}, "
      f"mean={group_clean_sheet.mean():.2f}%, std={group_clean_sheet.std(ddof=1):.2f}")
print(f"No-clean-sheet group : n={len(group_no_clean_sheet)}, "
      f"mean={group_no_clean_sheet.mean():.2f}%, std={group_no_clean_sheet.std(ddof=1):.2f}")


t_stat, p_value = stats.ttest_ind(
    group_clean_sheet, group_no_clean_sheet, equal_var=False
)
alpha = 0.05
print(f"t-statistic: {t_stat:.3f}")
print(f"p-value    : {p_value:.4f}")
if p_value < alpha:
    print(f"Result: p < {alpha} -> reject H0. There IS a statistically "
          f"significant difference in Save% between the two groups.\n")
else:
    print(f"Result: p >= {alpha} -> fail to reject H0. No statistically "
          f"significant difference in Save% was found between the two groups.\n")

# Visualisation

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left panel: distribution of Save% in the sample, with the CI marked
axes[0].hist(sample["save_pct"], bins=8, color="#4C72B0", edgecolor="white")
axes[0].axvline(sample_mean, color="black", linestyle="--",
                linewidth=1.5, label=f"Sample mean ({sample_mean:.1f}%)")
axes[0].axvspan(ci_lower, ci_upper, color="orange", alpha=0.2, label="95% CI")
axes[0].set_title("Distribution of Save% (sample, n=32)")
axes[0].set_xlabel("Save percentage (%)")
axes[0].set_ylabel("Number of goalkeepers")
axes[0].legend()

# Right panel: boxplot comparing the two clean-sheet groups
axes[1].boxplot(
    [group_no_clean_sheet, group_clean_sheet],
    tick_labels=["No clean sheet", "At least 1 clean sheet"],
    patch_artist=True,
    boxprops=dict(facecolor="#DD8452"),
)
axes[1].set_title("Save% by clean-sheet status")
axes[1].set_ylabel("Save percentage (%)")

plt.tight_layout()
output_path = "./goalkeeper_save_percentage_analysis.png"
plt.savefig(output_path, dpi=150)
print(f"Chart saved to: {output_path}")
