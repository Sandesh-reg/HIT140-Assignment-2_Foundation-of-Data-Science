"""
Analytic Question: Do midfielders record a higher rate of assists
per 90 minutes than forwards in the 2026 FIFA World Cup?
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, t
from pathlib import Path

# Find the main project folder
base_folder = Path(__file__).resolve().parents[2]
output_folder = Path(__file__).parent

# Load the raw data
# (FBref's CSV export has a 2-row header: a blank grouping row, then the
# real column names, so we skip the first row.)
df = pd.read_csv(
    base_folder / "fbref_WC2026_Assists.csv",
    skiprows=1,
    encoding="latin1"
)

# Remove rows that are not player records
df = df.dropna(subset=["Player"])

# Remove columns that are not needed
df = df.drop(columns=["Rk"])

# Select midfielders and forwards
# Players with mixed position tags (e.g., FW,MF or MF,FW) are excluded so that
# each player represents a single, unambiguous position category.
data = df[df["Pos"].isin(["MF", "FW"])].copy()

# Keep players with at least one full 90-minute equivalent
data = data[data["90s"] >= 1].copy()

# Calculate assists per 90 minutes
data["Assists_Per_90"] = data["Ast"] / data["90s"]

# Stratified random sampling
# Position is used as the stratification variable.
midfielders = data[data["Pos"] == "MF"].sample(
    n=40,
    random_state=42
)

forwards = data[data["Pos"] == "FW"].sample(
    n=40,
    random_state=42
)

# Combine both groups into the final sample
sample = pd.concat([midfielders, forwards])

# Save the final sample
sample.to_csv(
    output_folder / "assists_cleaned.csv",
    index=False
)

# Get assists rates for each group
midfielder_rates = sample[
    sample["Pos"] == "MF"
]["Assists_Per_90"]

forward_rates = sample[
    sample["Pos"] == "FW"
]["Assists_Per_90"]

# Calculate descriptive statistics and 95% confidence intervals
results = []

for position, group in [
    ("Midfielders", midfielder_rates),
    ("Forwards", forward_rates)
]:
    mean = group.mean()
    median = group.median()
    standard_deviation = group.std()
    sample_size = len(group)

    standard_error = standard_deviation / (sample_size ** 0.5)

    confidence_interval = t.interval(
        0.95,
        sample_size - 1,
        loc=mean,
        scale=standard_error
    )

    results.append({
        "Position": position,
        "Players": sample_size,
        "Mean Ast/90": mean,
        "Median Ast/90": median,
        "Standard Deviation": standard_deviation,
        "95% CI Lower": confidence_interval[0],
        "95% CI Upper": confidence_interval[1]
    })

results_table = pd.DataFrame(results)

print("\nASSISTS ANALYSIS")
print("================")

print("\nPopulation after eligibility filtering:")
print("Midfielders:", len(data[data["Pos"] == "MF"]))
print("Forwards:", len(data[data["Pos"] == "FW"]))

print("\nStratified Random Sample:")
print("Midfielders:", len(midfielders))
print("Forwards:", len(forwards))
print("Total sample:", len(sample))

print("\nDescriptive Statistics:")
print(results_table.round(3).to_string(index=False))

# Welch two-sample t-test
t_statistic, p_value = ttest_ind(
    midfielder_rates,
    forward_rates,
    equal_var=False
)

print("\nWelch Two-Sample t-Test:")
print("t-statistic:", round(t_statistic, 3))
print("p-value:", round(p_value, 4))

if p_value < 0.05:
    print("Result: Statistically significant difference.")
else:
    print("Result: No statistically significant difference.")

# Save statistical results
results_table.to_csv(
    output_folder / "assists_results.csv",
    index=False
)

# Create boxplot and grab the axis directly to prevent blank figures
ax = sample.boxplot(
    column="Assists_Per_90",
    by="Pos",
    figsize=(8, 6)
)

# Apply formatting directly to the active plot axis
ax.set_title("Assists per 90 Minutes: Midfielders vs Forwards")
plt.suptitle("")
ax.set_xlabel("Playing Position")
ax.set_ylabel("Assists per 90 Minutes")

plt.tight_layout()

plt.savefig(
    output_folder / "assists_boxplot.png",
    dpi=300
)

plt.show()
