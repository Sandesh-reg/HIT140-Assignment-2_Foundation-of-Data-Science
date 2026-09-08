"""
Analytic Question: Do defenders record a higher rate of yellow cards 
per 90 minutes than midfielders in the 2026 FIFA World Cup?
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, t
from pathlib import Path

# Find the main project folder
base_folder = Path(__file__).resolve().parents[2]
output_folder = Path(__file__).parent

# Load the raw data
df = pd.read_excel(base_folder / "fbref_WC2026_Cards.xlsx")

# Remove rows that are not player records
df = df.dropna(subset=["Player"])

# Remove columns that are not needed
df = df.drop(columns=["Rk", -9999])

# Select defenders and midfielders
# Players with mixed position tags (e.g., DFMF, MFDF) are excluded so that
# each player represents a single, unambiguous position category.
data = df[df["Pos"].isin(["DF", "MF"])].copy()

# Keep players with at least one full 90-minute equivalent
data = data[data["90s"] >= 1].copy()

# Calculate yellow cards per 90 minutes
data["Yellow_Cards_Per_90"] = data["CrdY"] / data["90s"]

# Stratified random sampling
# Position is used as the stratification variable.
defenders = data[data["Pos"] == "DF"].sample(
    n=100,
    random_state=42
)

midfielders = data[data["Pos"] == "MF"].sample(
    n=100,
    random_state=42
)

# Combine both groups into the final sample
sample = pd.concat([defenders, midfielders])

# Save the final sample
sample.to_csv(
    output_folder / "discipline_cleaned.csv",
    index=False
)

# Get yellow-card rates for each group
defender_rates = sample[
    sample["Pos"] == "DF"
]["Yellow_Cards_Per_90"]

midfielder_rates = sample[
    sample["Pos"] == "MF"
]["Yellow_Cards_Per_90"]

# Calculate descriptive statistics and 95% confidence intervals
results = []

for position, group in [
    ("Defenders", defender_rates),
    ("Midfielders", midfielder_rates)
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
        "Mean YC/90": mean,
        "Median YC/90": median,
        "Standard Deviation": standard_deviation,
        "95% CI Lower": confidence_interval[0],
        "95% CI Upper": confidence_interval[1]
    })

results_table = pd.DataFrame(results)

print("\nDISCIPLINE ANALYSIS")
print("===================")

print("\nPopulation after eligibility filtering:")
print("Defenders:", len(data[data["Pos"] == "DF"]))
print("Midfielders:", len(data[data["Pos"] == "MF"]))

print("\nStratified Random Sample:")
print("Defenders:", len(defenders))
print("Midfielders:", len(midfielders))
print("Total sample:", len(sample))

print("\nDescriptive Statistics:")
print(results_table.round(3).to_string(index=False))

# Welch two-sample t-test
t_statistic, p_value = ttest_ind(
    defender_rates,
    midfielder_rates,
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
    output_folder / "discipline_results.csv",
    index=False
)

# Create boxplot and grab the axis directly to prevent blank figures
ax = sample.boxplot(
    column="Yellow_Cards_Per_90",
    by="Pos",
    figsize=(8, 6)
)

# Apply formatting directly to the active plot axis
ax.set_title("Yellow Cards per 90 Minutes: Defenders vs Midfielders")
plt.suptitle("")
ax.set_xlabel("Playing Position")
ax.set_ylabel("Yellow Cards per 90 Minutes")

plt.tight_layout()

plt.savefig(
    output_folder / "discipline_boxplot.png",
    dpi=300
)

plt.show()
