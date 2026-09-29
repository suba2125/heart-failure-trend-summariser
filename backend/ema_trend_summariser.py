import pandas as pd

data = pd.read_csv("../data/synthetic_patient_data.csv")


def calculate_ema(values, alpha=0.4):
    """
    Calculate Exponential Moving Average (EMA).

    EMA gives more importance to recent readings while
    still considering previous readings.
    """
    ema_values = [values[0]]

    for value in values[1:]:
        ema = (alpha * value) + ((1 - alpha) * ema_values[-1])
        ema_values.append(ema)

    return ema_values


def summarise_with_ema(patient_data):
    baseline = patient_data["baseline_weight"].iloc[0]

    weights = patient_data["weight"].tolist()

    # Calculate EMA for weight readings
    ema_values = calculate_ema(weights)

    current_weight = weights[-1]
    current_ema = ema_values[-1]

    weight_change = current_weight - baseline
    ema_change = current_ema - baseline

    # Detect whether EMA shows a persistent upward pattern
    ema_increasing_steps = 0

    for i in range(1, len(ema_values)):
        if ema_values[i] > ema_values[i - 1]:
            ema_increasing_steps += 1

    # Count symptoms from latest available reading
    latest = patient_data.iloc[-1]

    symptom_count = 0

    if latest["breathlessness"] != "No":
        symptom_count += 1

    if latest["swelling"] != "No":
        symptom_count += 1

    if latest["fatigue"] != "No":
        symptom_count += 1

    # EMA-based priority score
    score = 0

    if ema_change > 0.5:
        score += 2

    if ema_change > 1.0:
        score += 1

    if ema_increasing_steps >= 2:
        score += 2

    if symptom_count > 0:
        score += 2

    if symptom_count >= 2:
        score += 1

    if score >= 5:
        priority = "HIGH"
    elif score >= 3:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    # Describe the detected pattern
    if ema_increasing_steps >= 2 and ema_change > 0.5:
        trend = "Persistent increasing EMA trend"
    elif ema_change > 0.5:
        trend = "EMA weight increase from baseline"
    else:
        trend = "No meaningful EMA trend"

    return {
        "priority": priority,
        "trend": trend,
        "weight_change": weight_change,
        "ema_change": ema_change,
        "ema_increasing_steps": ema_increasing_steps,
        "score": score
    }


print("EMA TREND SUMMARISER RESULTS")
print("============================")

for patient_id, patient_data in data.groupby("patient_id"):

    result = summarise_with_ema(patient_data)

    print(f"\nPatient: {patient_id}")
    print(f"Priority: {result['priority']}")
    print(f"Trend: {result['trend']}")
    print(f"Weight change: {result['weight_change']:.1f} kg")
    print(f"EMA change: {result['ema_change']:.2f} kg")
    print(f"EMA increasing steps: {result['ema_increasing_steps']}")
    print(f"Score: {result['score']}")

    if result["priority"] == "HIGH":
        print("Action: Human clinical review recommended.")
    else:
        print("Action: Continue human monitoring.")