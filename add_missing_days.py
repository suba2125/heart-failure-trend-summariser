import pandas as pd

input_file = "data/synthetic_patient_data.csv"

# Read existing dataset
data = pd.read_csv(input_file)

# Remove selected reporting days to simulate missed reporting.
# We remove complete days, not individual sensor values.
missing_days = {
    "P028": [3],
    "P029": [5],
    "P030": [2]
}

original_rows = len(data)

for patient_id, days in missing_days.items():
    data = data[
        ~(
            (data["patient_id"] == patient_id)
            & (data["day"].isin(days))
        )
    ]

data = data.sort_values(
    ["patient_id", "day"]
).reset_index(drop=True)

# Save the updated dataset
data.to_csv(input_file, index=False)

print("MISSING REPORTING DAY UPDATE")
print("============================")

print(f"Original rows: {original_rows}")
print(f"Updated rows: {len(data)}")
print(f"Rows removed: {original_rows - len(data)}")

print("\nMissing reporting days:")

for patient_id, days in missing_days.items():
    print(f"{patient_id}: Day {days}")

print("\nDataset updated successfully.")