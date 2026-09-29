# Heart-Failure Trend Summariser

## Trend Summariser Prioritises Meaningful Change for Heart-Failure Patients Recovering At Home After Discharge

---

## 1. Project Overview

Heart-failure patients recovering at home may record daily measurements such as weight, blood pressure, heart rate, and symptoms.

A simple alert system may generate alerts whenever an individual reading crosses a fixed threshold. This can create unnecessary low-value alerts and make it harder for care teams to identify meaningful changes over several days.

This project develops a **trend summariser** that focuses on meaningful patterns across multiple home-monitoring readings instead of reacting only to individual abnormal readings.

The project is designed as a **decision-support prototype**. It does not diagnose patients, prescribe treatment, or make autonomous clinical decisions.

---

## 2. Problem Statement

The main problem is alert overload caused by treating every abnormal individual reading as equally important.

For example, a patient may have one temporary weight increase because of measurement noise or a short-term fluctuation. A simple threshold model may generate an alert for this single reading.

In contrast, a trend-based system can examine multiple days of data and symptoms to identify whether the change appears persistent.

The goal is therefore to:

- Reduce unnecessary low-value alerts.
- Identify persistent changes over multiple days.
- Consider symptoms together with weight trends.
- Compare a simple threshold baseline with a trend-based approach.
- Measure the performance of both approaches.
- Keep human review in the decision-making process.

---

## 3. Project Objectives

The project aims to:

1. Build a baseline threshold-based alert system.
2. Build a multi-factor trend summariser.
3. Improve trend detection using Exponential Moving Average (EMA).
4. Test the system using a larger synthetic dataset.
5. Include missing reporting days and noisy sensor readings.
6. Compare baseline and trend-based alerts.
7. Calculate Precision, Recall, Specificity, and F1 Score.
8. Test realistic edge cases.
9. Maintain a human-in-the-loop safety boundary.

---

## 4. System Approach

The project contains two main approaches.

### 4.1 Baseline Model

The baseline generates an alert when:

```text
Current Weight - Baseline Weight > 0.5 kg
```
