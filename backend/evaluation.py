import pandas as pd

data = pd.read_csv("../data/synthetic_patient_data.csv")

baseline_alerts = 0
trend_alerts = 0

for patient_id, patient_data in data.groupby("patient_id"):

    baseline = patient_data["baseline_weight"].iloc[0]

    # Baseline alerts
    for weight in patient_data["weight"]:
        if weight - baseline > 0.5:
            baseline_alerts += 1

    # Trend summariser
    weights = patient_data["weight"].tolist()

    increasing_days = 0

    for i in range(1, len(weights)):
        if weights[i] > weights[i - 1]:
            increasing_days += 1

    weight_change = weights[-1] - baseline

    latest = patient_data.iloc[-1]

    symptom_count = 0

    if latest["breathlessness"] != "No":
        symptom_count += 1

    if latest["swelling"] != "No":
        symptom_count += 1

    if latest["fatigue"] != "No":
        symptom_count += 1

    if (
        weight_change > 0.5
        and increasing_days >= 2
    ) or symptom_count >= 1:
        trend_alerts += 1


print("EVALUATION RESULTS")
print("==================")

print(f"Baseline alert count: {baseline_alerts}")
print(f"Trend summariser alert count: {trend_alerts}")

if baseline_alerts > 0:
    reduction = (
        (baseline_alerts - trend_alerts)
        / baseline_alerts
    ) * 100

    print(f"Alert reduction: {reduction:.1f}%")
else:
    print("Alert reduction: Not applicable")

print("\nEvaluation completed.")