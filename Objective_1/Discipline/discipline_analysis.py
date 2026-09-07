import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, t
from pathlib import Path

# Find the main project folder
base_folder = Path(__file__).resolve().parents[2]

# Load the raw data
df = pd.read_excel(base_folder / "fbref_WC2026_Cards.xlsx")

# Remove rows that are not player records
df = df.dropna(subset=["Player"])

# Remove columns that are not needed
df = df.drop(columns=["Rk", -9999])

# Select defenders and midfielders
data = df[df["Pos"].isin(["DF", "MF"])].copy()

# Keep players with at least one full 90-minute equivalent
data = data[data["90s"] >= 1].copy()

# Calculate yellow cards per 90 minutes
data["Yellow_Cards_Per_90"] = data["CrdY"] / data["90s"]

# Save the cleaned dataset
data.to_csv(
    Path(__file__).parent / "discipline_cleaned.csv",
    index=False
)

# Separate the two groups
defenders = data[data["Pos"] == "DF"]["Yellow_Cards_Per_90"]
midfielders = data[data["Pos"] == "MF"]["Yellow_Cards_Per_90"]

# Calculate descriptive statistics and 95% confidence intervals
results = []

for position, group in [
    ("Defenders", defenders),
    ("Midfielders", midfielders)
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

print("\nSample:")
print("Total eligible players:", len(data))
print("Defenders:", len(defenders))
print("Midfielders:", len(midfielders))

print("\nDescriptive Statistics:")
print(results_table.round(3).to_string(index=False))

# Welch two-sample t-test
t_statistic, p_value = ttest_ind(
    defenders,
    midfielders,
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
    Path(__file__).parent / "discipline_results.csv",
    index=False
)

# Create boxplot
plt.figure(figsize=(8, 6))

data.boxplot(
    column="Yellow_Cards_Per_90",
    by="Pos"
)

plt.title("Yellow Cards per 90 Minutes: Defenders vs Midfielders")
plt.suptitle("")
plt.xlabel("Playing Position")
plt.ylabel("Yellow Cards per 90 Minutes")

plt.tight_layout()

plt.savefig(
    Path(__file__).parent / "discipline_boxplot.png",
    dpi=300
)

plt.show()