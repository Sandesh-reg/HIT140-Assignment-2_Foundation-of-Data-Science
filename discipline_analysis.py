import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, t

# Load the discipline data
df = pd.read_excel("fbref_WC2026_Cards.xlsx")

# Remove rows that are not player records
df = df.dropna(subset=["Player"])

# Remove unnecessary columns
df = df.drop(columns=["Rk", -9999])

# Select defenders and midfielders
data = df[df["Pos"].isin(["DF", "MF"])].copy()

# Only include players who played at least 90 minutes
data = data[data["90s"] >= 1].copy()

# Calculate yellow cards per 90 minutes
data["Yellow_Cards_Per_90"] = data["CrdY"] / data["90s"]

# Separate the two groups
defenders = data[data["Pos"] == "DF"]["Yellow_Cards_Per_90"]
midfielders = data[data["Pos"] == "MF"]["Yellow_Cards_Per_90"]

# Descriptive statistics
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

print("\nDISCIPLINE RESULTS")
print(results_table.round(3).to_string(index=False))

# Welch two-sample t-test
t_statistic, p_value = ttest_ind(
    defenders,
    midfielders,
    equal_var=False
)

print("\nWELCH TWO-SAMPLE T-TEST")
print("t-statistic:", round(t_statistic, 3))
print("p-value:", round(p_value, 4))

if p_value < 0.05:
    print("There is a statistically significant difference.")
else:
    print("There is no statistically significant difference.")

# Save results
results_table.to_csv("discipline_results.csv", index=False)

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
plt.savefig("discipline_boxplot.png", dpi=300)
plt.show()