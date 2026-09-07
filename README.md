# Heart Failure Trend Summariser

## Project Overview

Heart-failure patients recovering at home after discharge
may generate multiple daily readings and symptom reports.

A simple threshold-based alert system can generate many
low-value alerts and make it harder for care teams to
identify meaningful changes.

This project demonstrates a prototype Trend Summariser that
groups recent readings, identifies persistent patterns,
considers reported symptoms, and prioritises cases for
human review.

---

## Problem Statement

Care teams may receive too many individual home-monitoring
alerts.

The goal is to reduce low-value alerts while highlighting
meaningful changes that may require human review.

---

## Objectives

- Analyse repeated home readings.
- Compare a simple baseline alert method with a trend-based method.
- Identify persistent changes rather than isolated spikes.
- Consider reported symptoms.
- Prioritise patients for human review.
- Reduce unnecessary alert volume.
- Provide a simple care-team dashboard.

---

## Project Structure

```text
heart-failure-trend-summariser/

├── backend/
│   ├── baseline.py
│   ├── trend_summariser.py
│   ├── comparison.py
│   ├── evaluation.py
│   └── edge_cases.py
│
├── data/
│   └── synthetic_patient_data.csv
│
├── docs/
│   ├── patient_journeys.md
│   ├── workflow.md
│   └── error_analysis.md
│
└── frontend/
    └── index.html
```
