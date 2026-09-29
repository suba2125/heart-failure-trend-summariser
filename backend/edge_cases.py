import pandas as pd

data = pd.read_csv("../data/synthetic_patient_data.csv")


print("EXPANDED EDGE CASE TESTS")
print("========================")


# --------------------------------------------------
# TEST 1: ONE-TIME WEIGHT SPIKE
# --------------------------------------------------

print("\nTest 1 - One-time weight spike")

p009 = data[
    data["patient_id"] == "P009"
].dropna(subset=["weight"])

baseline = p009["baseline_weight"].iloc[0]

spike_detected = False

for weight in p009["weight"]:
    if weight - baseline > 0.5:
        spike_detected = True
        break

if spike_detected:
    print("Result: Spike detected in raw readings.")
    print(
        "Expected behaviour: Trend model should avoid "
        "persistent escalation."
    )
else:
    print("Result: No spike detected.")


# --------------------------------------------------
# TEST 2: STABLE PATIENT
# --------------------------------------------------

print("\nTest 2 - Stable patient")

p001 = data[
    data["patient_id"] == "P001"
].dropna(subset=["weight"])

baseline = p001["baseline_weight"].iloc[0]
latest_weight = p001["weight"].iloc[-1]

weight_change = latest_weight - baseline

if weight_change <= 0.5:
    print(
        "Result: Stable patient correctly remains "
        "below threshold."
    )
else:
    print(
        "Result: Unexpected weight increase detected."
    )


# --------------------------------------------------
# TEST 3: PERSISTENT INCREASING TREND
# --------------------------------------------------

print("\nTest 3 - Persistent increasing trend")

p017 = data[
    data["patient_id"] == "P017"
].dropna(subset=["weight"])

weights = p017["weight"].tolist()

increasing_days = 0

for i in range(1, len(weights)):

    if weights[i] > weights[i - 1]:
        increasing_days += 1

if increasing_days >= 2:

    print(
        "Result: Persistent increasing trend detected."
    )

    print(
        "Expected behaviour: Human clinical review recommended."
    )

else:

    print(
        "Result: Persistent trend not detected."
    )


# --------------------------------------------------
# TEST 4: SYMPTOM-ONLY CASE
# --------------------------------------------------

print("\nTest 4 - Symptoms without major weight increase")

p025 = data[
    data["patient_id"] == "P025"
].dropna(
    subset=[
        "breathlessness",
        "swelling",
        "fatigue"
    ]
)

latest = p025.iloc[-1]

symptom_count = 0

if latest["breathlessness"] != "No":
    symptom_count += 1

if latest["swelling"] != "No":
    symptom_count += 1

if latest["fatigue"] != "No":
    symptom_count += 1

baseline = p025["baseline_weight"].iloc[0]
latest_weight = p025["weight"].iloc[-1]

weight_change = latest_weight - baseline

if symptom_count > 0 and weight_change <= 0.5:

    print(
        "Result: Symptoms detected despite small "
        "weight change."
    )

    print(
        "Expected behaviour: Human review can still "
        "be prioritised."
    )

else:

    print(
        "Result: Symptom-only scenario not detected."
    )


# --------------------------------------------------
# TEST 5: MISSING REPORTING DAYS
# --------------------------------------------------

print("\nTest 5 - Missing reporting days")

missing_day_patients = [
    "P028",
    "P029",
    "P030"
]

missing_days_found = []

for patient_id in missing_day_patients:

    patient_data = data[
        data["patient_id"] == patient_id
    ].sort_values("day")

    recorded_days = patient_data["day"].tolist()

    if len(recorded_days) > 0:

        expected_days = list(
            range(
                min(recorded_days),
                max(recorded_days) + 1
            )
        )

        for day in expected_days:

            if day not in recorded_days:

                missing_days_found.append(
                    (patient_id, day)
                )


if len(missing_days_found) > 0:

    print(
        f"Result: {len(missing_days_found)} "
        "missing reporting day(s) detected."
    )

    for patient_id, day in missing_days_found:

        print(
            f"{patient_id}: Day {day} missing"
        )

else:

    print(
        "Result: No missing reporting days found."
    )


# --------------------------------------------------
# TEST 6: NOISY SENSOR READINGS
# --------------------------------------------------

print("\nTest 6 - Noisy sensor readings")

noisy_patients = [
    "P028",
    "P029",
    "P030"
]

noisy_data = data[
    data["patient_id"].isin(noisy_patients)
].dropna(subset=["weight"])


if len(noisy_data) > 0:

    for patient_id in noisy_patients:

        patient_data = noisy_data[
            noisy_data["patient_id"] == patient_id
        ]

        if len(patient_data) > 1:

            weights = patient_data["weight"].tolist()

            variation = max(weights) - min(weights)

            print(
                f"{patient_id}: Weight variation = "
                f"{variation:.2f} kg"
            )

    print(
        "Result: Noisy patient profiles processed successfully."
    )

else:

    print(
        "Result: No noisy patient data found."
    )


# --------------------------------------------------
# TEST 7: DATASET SCALE CHECK
# --------------------------------------------------

print("\nTest 7 - Dataset scale")

patient_count = data[
    "patient_id"
].nunique()

if patient_count >= 25:

    print(
        f"Result: Dataset contains "
        f"{patient_count} patient profiles."
    )

    print(
        "Requirement satisfied: More than 25 "
        "simulated patients."
    )

else:

    print(
        f"Result: Dataset contains only "
        f"{patient_count} patients."
    )


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print("\nEDGE CASE TESTING SUMMARY")
print("=========================")

print("✓ One-time spike scenario tested")
print("✓ Stable patient scenario tested")
print("✓ Persistent trend scenario tested")
print("✓ Symptom-only scenario tested")
print("✓ Missing reporting days scenario tested")
print("✓ Noisy sensor scenario tested")
print("✓ Dataset scale checked")

print("\nEdge case testing completed.")