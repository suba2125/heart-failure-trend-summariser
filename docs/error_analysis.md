# Error Analysis

## Purpose

The Trend Summariser is a prototype decision-support system.
It may produce incorrect or incomplete prioritisation in
some situations.

## Potential Error Cases

### 1. One-Time Weight Spike

A patient may have a temporary increase in weight.

Example:
P003 shows a one-time increase to 77.0 kg,
but the following reading returns close to baseline.

Risk:
A simple threshold-based system may generate an unnecessary alert.

Prototype handling:
The trend summariser checks whether the increase persists
across multiple readings.

---

### 2. Missing Symptoms

A patient may not report symptoms even when weight changes
are observed.

Risk:
The system may underestimate the importance of a change.

Improvement:
Future versions should handle missing data explicitly
and allow human review when data quality is uncertain.

---

### 3. Missing or Incorrect Readings

Home measurements may be missing or entered incorrectly.

Risk:
An incorrect reading could create a false trend.

Improvement:
Future versions should include data-quality checks
before calculating trends.

---

### 4. False Negative

A meaningful change may not be detected if the available
readings are incomplete or the change does not match
the prototype's trend rules.

Risk:
The care team may not receive a prioritised signal.

Mitigation:
The system should remain a support tool and not replace
routine monitoring or professional judgement.

---

## Key Limitation

The current prototype uses synthetic data and simple
rule-based scoring.

Therefore, the measured 75% alert reduction demonstrates
the behaviour of this prototype dataset only.

It should not be interpreted as evidence of clinical
effectiveness.
