import pandas as pd

data = pd.read_csv("../data/synthetic_patient_data.csv")


# --------------------------------------------------
# EMA CALCULATION
# --------------------------------------------------

def calculate_ema(values, alpha=0.4):
    ema_values = [values[0]]

    for value in values[1:]:
        ema = (alpha * value) + ((1 - alpha) * ema_values[-1])
        ema_values.append(ema)

    return ema_values


# --------------------------------------------------
# EMA PATIENT-LEVEL PREDICTION
# --------------------------------------------------

def ema_predict(patient_data):
    baseline = patient_data["baseline_weight"].iloc[0]
    weights = patient_data["weight"].tolist()

    ema_values = calculate_ema(weights)

    current_ema = ema_values[-1]
    ema_change = current_ema - baseline

    increasing_steps = 0

    for i in range(1, len(ema_values)):
        if ema_values[i] > ema_values[i - 1]:
            increasing_steps += 1

    latest = patient_data.iloc[-1]

    symptom_count = 0

    if latest["breathlessness"] != "No":
        symptom_count += 1

    if latest["swelling"] != "No":
        symptom_count += 1

    if latest["fatigue"] != "No":
        symptom_count += 1

    score = 0

    if ema_change > 0.5:
        score += 2

    if ema_change > 1.0:
        score += 1

    if increasing_steps >= 2:
        score += 2

    if symptom_count > 0:
        score += 2

    if symptom_count >= 2:
        score += 1

    return score >= 5


# --------------------------------------------------
# BASELINE PATIENT-LEVEL PREDICTION
# --------------------------------------------------

def baseline_predict(patient_data):

    baseline = patient_data["baseline_weight"].iloc[0]

    for weight in patient_data["weight"]:
        if weight - baseline > 0.5:
            return True

    return False


# --------------------------------------------------
# METRICS
# --------------------------------------------------

def calculate_metrics(predictions, ground_truth):

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for predicted, actual in zip(predictions, ground_truth):

        if predicted and actual:
            tp += 1

        elif not predicted and not actual:
            tn += 1

        elif predicted and not actual:
            fp += 1

        elif not predicted and actual:
            fn += 1

    precision = (
        tp / (tp + fp)
        if (tp + fp) > 0
        else 0
    )

    recall = (
        tp / (tp + fn)
        if (tp + fn) > 0
        else 0
    )

    specificity = (
        tn / (tn + fp)
        if (tn + fp) > 0
        else 0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    return tp, tn, fp, fn, precision, recall, specificity, f1


# --------------------------------------------------
# BUILD PATIENT-LEVEL RESULTS
# --------------------------------------------------

patient_ids = []
baseline_predictions = []
ema_predictions = []
ground_truth = []

for patient_id, patient_data in data.groupby("patient_id"):

    patient_ids.append(patient_id)

    # Baseline prediction
    baseline_result = baseline_predict(patient_data)
    baseline_predictions.append(baseline_result)

    # EMA prediction
    ema_result = ema_predict(patient_data)
    ema_predictions.append(ema_result)

    # Synthetic ground truth:
    # Patient is considered a clinical-review case
    # if any reading has "Clinical review" as outcome.
    clinical_review = (
        patient_data["escalation_outcome"]
        == "Clinical review"
    ).any()

    ground_truth.append(clinical_review)


# --------------------------------------------------
# CALCULATE BASELINE METRICS
# --------------------------------------------------

(
    baseline_tp,
    baseline_tn,
    baseline_fp,
    baseline_fn,
    baseline_precision,
    baseline_recall,
    baseline_specificity,
    baseline_f1
) = calculate_metrics(
    baseline_predictions,
    ground_truth
)


# --------------------------------------------------
# CALCULATE EMA METRICS
# --------------------------------------------------

(
    ema_tp,
    ema_tn,
    ema_fp,
    ema_fn,
    ema_precision,
    ema_recall,
    ema_specificity,
    ema_f1
) = calculate_metrics(
    ema_predictions,
    ground_truth
)


# --------------------------------------------------
# ALERT COUNTS
# --------------------------------------------------

baseline_alert_count = sum(baseline_predictions)
ema_alert_count = sum(ema_predictions)

if baseline_alert_count > 0:

    alert_reduction = (
        (baseline_alert_count - ema_alert_count)
        / baseline_alert_count
    ) * 100

else:

    alert_reduction = 0


# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

print("QUANTITATIVE EVALUATION")
print("=======================")

print(f"Total patients: {len(patient_ids)}")

print("\nGROUND TRUTH")
print("------------")

clinical_cases = sum(ground_truth)

print(f"Clinical review cases: {clinical_cases}")
print(
    f"No clinical review cases: "
    f"{len(patient_ids) - clinical_cases}"
)


print("\nBASELINE RESULTS")
print("----------------")

print(f"Baseline patient alerts: {baseline_alert_count}")
print(f"True Positives: {baseline_tp}")
print(f"True Negatives: {baseline_tn}")
print(f"False Positives: {baseline_fp}")
print(f"False Negatives: {baseline_fn}")

print(f"Precision: {baseline_precision:.2f}")
print(f"Recall / Sensitivity: {baseline_recall:.2f}")
print(f"Specificity: {baseline_specificity:.2f}")
print(f"F1 Score: {baseline_f1:.2f}")


print("\nEMA RESULTS")
print("-----------")

print(f"EMA patient alerts: {ema_alert_count}")
print(f"True Positives: {ema_tp}")
print(f"True Negatives: {ema_tn}")
print(f"False Positives: {ema_fp}")
print(f"False Negatives: {ema_fn}")

print(f"Precision: {ema_precision:.2f}")
print(f"Recall / Sensitivity: {ema_recall:.2f}")
print(f"Specificity: {ema_specificity:.2f}")
print(f"F1 Score: {ema_f1:.2f}")


print("\nALERT REDUCTION")
print("---------------")

print(
    f"Baseline alerts: {baseline_alert_count}"
)

print(
    f"EMA alerts: {ema_alert_count}"
)

print(
    f"Alert reduction: {alert_reduction:.1f}%"
)


print("\nEVALUATION NOTE")
print("---------------")

print(
    "Ground truth is based on synthetic escalation_outcome "
    "labels in the prototype dataset."
)

print(
    "These metrics are synthetic benchmark results and "
    "do not represent clinical validation."
)

print(
    "The system only recommends human review and does not "
    "make autonomous diagnosis or treatment decisions."
)

print("\nEvaluation completed.")