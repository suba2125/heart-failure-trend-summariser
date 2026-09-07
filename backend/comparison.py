import pandas as pd

data = pd.read_csv("../data/synthetic_patient_data.csv")

threshold = 0.5

print("BASELINE VS TREND SUMMARISER")
print("============================")

for patient_id, patient_data in data.groupby("patient_id"):

    baseline = patient_data["baseline_weight"].iloc[0]
    current_weight = patient_data["weight"].iloc[-1]

    # BASELINE METHOD
    baseline_alerts = 0

    for weight in patient_data["weight"]:
        if weight - baseline > threshold:
            baseline_alerts += 1

    # TREND METHOD
    weights = patient_data["weight"].tolist()

    increasing_days = 0

    for i in range(1, len(weights)):
        if weights[i] > weights[i - 1]:
            increasing_days += 1

    weight_change = current_weight - baseline

    symptom_count = 0
    latest = patient_data.iloc[-1]

    if latest["breathlessness"] != "No":
        symptom_count += 1

    if latest["swelling"] != "No":
        symptom_count += 1

    if latest["fatigue"] != "No":
        symptom_count += 1

    trend_alert = (
        weight_change > 0.5
        and increasing_days >= 2
    ) or symptom_count >= 1

    print(f"\nPatient: {patient_id}")
    print(f"Baseline alerts: {baseline_alerts}")
    print(f"Trend summariser alert: {trend_alert}")

print("\nComparison completed.")