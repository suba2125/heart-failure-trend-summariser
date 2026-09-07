import pandas as pd

data = pd.read_csv("../data/synthetic_patient_data.csv")

print("EDGE CASE TESTS")
print("================")

# Test 1: One-time weight spike
p003 = data[data["patient_id"] == "P003"]

if p003["weight"].iloc[2] > p003["baseline_weight"].iloc[0] + 0.5:
    print("Test 1 - One-time spike: Detected")
else:
    print("Test 1 - One-time spike: Not detected")

# Test 2: Stable patient
p001 = data[data["patient_id"] == "P001"]

weight_change = p001["weight"].iloc[-1] - p001["baseline_weight"].iloc[0]

if weight_change <= 0.5:
    print("Test 2 - Stable patient: No escalation")
else:
    print("Test 2 - Stable patient: Review needed")

# Test 3: Persistent increase with symptoms
p002 = data[data["patient_id"] == "P002"]

increasing_days = 0

for i in range(1, len(p002["weight"])):
    if p002["weight"].iloc[i] > p002["weight"].iloc[i - 1]:
        increasing_days += 1

symptoms = p002.iloc[-1]

symptom_count = 0

if symptoms["breathlessness"] != "No":
    symptom_count += 1

if symptoms["swelling"] != "No":
    symptom_count += 1

if symptoms["fatigue"] != "No":
    symptom_count += 1

if increasing_days >= 2 and symptom_count >= 1:
    print("Test 3 - Persistent trend + symptoms: Human review recommended")
else:
    print("Test 3 - Persistent trend + symptoms: Not detected")

print("\nEdge case testing completed.")