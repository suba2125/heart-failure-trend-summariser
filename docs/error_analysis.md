# Error Analysis

## Overview

Error analysis is used to identify situations where the Trend Summariser may produce an incorrect or incomplete priority.

The Review 2 prototype was tested using 30 synthetic patient profiles and 196 observations.

The dataset includes stable patients, one-time spikes, persistent increasing trends, symptom-only cases, noisy readings, and missing reporting days.

---

## 1. One-Time Weight Spike

### Scenario

A patient has one temporary increase in weight that crosses the baseline threshold.

### Potential Error

The simple baseline model may generate an alert from the individual reading even when there is no persistent trend.

### Trend Summariser Behaviour

The EMA-based approach considers multiple observations and can reduce the influence of a single temporary spike.

### Limitation

A short dataset or insufficient follow-up readings may make it difficult to distinguish a temporary spike from an emerging trend.

---

## 2. Stable Patient

### Scenario

The patient's measurements remain close to the baseline.

### Potential Error

Small sensor variations could be incorrectly interpreted as meaningful changes.

### Trend Summariser Behaviour

EMA smoothing reduces the effect of small individual fluctuations.

### Result

Stable patient profiles remained below the high-priority threshold during testing.

---

## 3. Persistent Increasing Trend

### Scenario

Weight increases gradually across multiple reporting days.

### Potential Error

A simple threshold model may generate repeated alerts without summarising the overall pattern.

### Trend Summariser Behaviour

The EMA-based model identifies persistent increasing movement across multiple observations.

### Result

Persistent increasing profiles were prioritised for human clinical review.

---

## 4. Symptoms Without Major Weight Increase

### Scenario

A patient reports symptoms even though weight has not increased significantly.

### Potential Error

A weight-only system may fail to prioritise the case.

### Trend Summariser Behaviour

The prototype includes:

- Breathlessness
- Swelling
- Fatigue

These symptoms contribute to the priority score.

### Result

Symptom-only synthetic cases were prioritised for human review.

---

## 5. Missing Reporting Days

### Scenario

Some patients do not provide readings on every expected day.

### Tested Cases

The dataset contains six missing reporting days:

- P028: Day 3
- P028: Day 5
- P029: Day 4
- P029: Day 5
- P030: Day 2
- P030: Day 5

### Potential Error

Missing observations may make a trend appear shorter or less reliable than it actually is.

### System Behaviour

The missing reporting patterns are detected during edge-case testing.

### Limitation

The prototype does not estimate missing measurements or automatically determine why a reading is missing.

Human review is required when incomplete data affects interpretation.

---

## 6. Noisy Sensor Readings

### Scenario

Home monitoring devices may produce small variations between readings.

### Tested Profiles

- P028: 0.30 kg variation
- P029: 0.90 kg variation
- P030: 0.40 kg variation

### Potential Error

Sensor noise may create false changes.

### Trend Summariser Behaviour

EMA smoothing reduces the influence of individual fluctuations.

### Limitation

The prototype does not model real-world device calibration errors or all possible sensor failure modes.

---

## 7. False Positives

A false positive occurs when the system prioritises a patient for clinical review even though the synthetic ground-truth label does not indicate a clinical escalation.

The quantitative evaluation compares the baseline model and EMA model using the synthetic `escalation_outcome` labels.

The results should be interpreted only as prototype benchmark results.

---

## 8. False Negatives

A false negative occurs when a clinically escalated synthetic case is not identified by the model.

False negatives are important because reducing alerts should not hide meaningful cases.

The evaluation therefore includes Recall / Sensitivity alongside alert reduction.

The current synthetic benchmark produced:

- Baseline false negatives: 3
- EMA false negatives: 0

These results are based on synthetic labels and are not evidence of clinical performance.

---

## 9. Quantitative Error Analysis

### Baseline Model

- True Positives: 8
- True Negatives: 15
- False Positives: 4
- False Negatives: 3
- Precision: 0.67
- Recall / Sensitivity: 0.73
- Specificity: 0.79
- F1 Score: 0.70

### EMA Trend Summariser

- True Positives: 11
- True Negatives: 19
- False Positives: 0
- False Negatives: 0
- Precision: 1.00
- Recall / Sensitivity: 1.00
- Specificity: 1.00
- F1 Score: 1.00

---

## 10. Important Evaluation Limitation

The evaluation uses synthetic `escalation_outcome` labels created for this prototype.

The simulated labels are based on the designed patient scenarios and therefore may align closely with the patterns used by the trend summariser.

As a result, the perfect EMA benchmark metrics should not be interpreted as real-world clinical accuracy.

Real clinical validation would require representative patient data, clinically established labels, appropriate study design, and qualified clinical oversight.

---

## 11. Review 2 Improvements

The following improvements were implemented based on Review 1 feedback:

### Larger Synthetic Dataset

The dataset was expanded from 4 to 30 simulated patient profiles.

### More Realistic Failure Cases

Testing now includes:

- One-time weight spikes
- Stable patients
- Persistent increasing trends
- Symptoms without major weight increase
- Missing reporting days
- Noisy sensor readings

### EMA-Based Trend Detection

The trend summariser was improved from fixed raw-reading trend checks to an Exponential Moving Average approach.

### Quantitative Metrics

The evaluation now includes:

- Precision
- Recall / Sensitivity
- Specificity
- F1 Score
- True Positives
- True Negatives
- False Positives
- False Negatives
- Alert reduction

---

## 12. Safety Boundary

The Trend Summariser is a decision-support prototype.

It does not:

- Diagnose patients
- Prescribe medication
- Change treatment
- Make autonomous clinical decisions

All potentially meaningful cases remain subject to human clinical review.
