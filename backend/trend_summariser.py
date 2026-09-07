import pandas as pd

# Load patient data
data = pd.read_csv("../data/synthetic_patient_data.csv")

def summarise_trend(patient_data):

    baseline = patient_data["baseline_weight"].iloc[0]

    # Recent weight readings
    weights = patient_data["weight"].tolist()

    current_weight = weights[-1]

    # Change from baseline
    weight_change = current_weight - baseline

    # Check whether weight is continuously increasing
    increasing_days = 0

    for i in range(1, len(weights)):
        if weights[i] > weights[i - 1]:
            increasing_days += 1

    # Check symptoms
    latest = patient_data.iloc[-1]

    symptom_count = 0

    if latest["breathlessness"] != "No":
        symptom_count += 1

    if latest["swelling"] != "No":
        symptom_count += 1

    if latest["fatigue"] != "No":
        symptom_count += 1

    # Priority calculation
    score = 0

    if weight_change > 0.5:
        score += 2

    if weight_change > 1.0:
        score += 1

    if increasing_days >= 2:
        score += 2

    if symptom_count > 0:
        score += 2

    if symptom_count >= 2:
        score += 1

    # Priority
    if score >= 5:
        priority = "HIGH"
    elif score >= 3:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    # Summary
    if increasing_days >= 2 and weight_change > 0.5:
        trend = "Persistent increasing weight trend"
    elif weight_change > 0.5:
        trend = "Weight increased from baseline"
    else:
        trend = "No meaningful weight trend"

    return priority, trend, weight_change, score


print("TREND SUMMARISER RESULTS")
print("------------------------")

# Process each patient
for patient_id, patient_data in data.groupby("patient_id"):

    priority, trend, change, score = summarise_trend(patient_data)

    print(f"\nPatient: {patient_id}")
    print(f"Priority: {priority}")
    print(f"Trend: {trend}")
    print(f"Weight change: {change:.1f} kg")
    print(f"Score: {score}")

    if priority == "HIGH":
        print("Action: Human clinical review recommended.")
    else:
        print("Action: Continue human monitoring.")