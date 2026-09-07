import pandas as pd

# Load synthetic patient data
data = pd.read_csv("../data/synthetic_patient_data.csv")

# Alert threshold
threshold = 0.5

# Calculate difference from baseline
data["weight_change"] = data["weight"] - data["baseline_weight"]

# Simple baseline alert
data["baseline_alert"] = data["weight_change"] > threshold

# Display results
print("BASELINE ALERT RESULTS")
print("----------------------")

for index, row in data.iterrows():

    if row["baseline_alert"]:
        print(
            f'{row["patient_id"]} - Day {row["day"]}: '
            f'ALERT | Weight = {row["weight"]} kg | '
            f'Change = +{row["weight_change"]:.1f} kg'
        )