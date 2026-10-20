# MarketMind Phase 2 — AI Governance Audit Report

**Prepared by:** Aldric Pinto  
**Date:** October 2026  
**Scope:** MarketMind Phase 2 — University Marketing Intelligence Platform  
**Audience:** Capstone Supervisor  

---

## Purpose

This document summarizes a code-level governance audit of the MarketMind Phase 2 platform. The goal was to identify AI-specific risks present in the system and recommend concrete, actionable improvements. Each item below is tied directly to specific components in the codebase.

---

## Audit Summary

| Area | Finding | Priority |
|---|---|---|
| Demographic bias in lead scoring | High risk | 🔴 High |
| No model drift monitoring | Gap | 🔴 High |
| PII in training data | High risk | 🔴 High |
| Pickle-based model serialization | Security risk | 🟡 Medium |
| Hardcoded fusion weights | Accuracy risk | 🟡 Medium |
| No model performance logging | Observability gap | 🟡 Medium |
| Transparent audit trail | Already addressed | 🟢 Remediated |
| Human override controls | Already addressed | 🟢 Remediated |
| Explainable step-by-step output | Already addressed | 🟢 Remediated |

---

## Improvement 1 — Remove Protected Attributes from Lead Scoring

**File:** `MarketMindServer/app/models/crm/crm_funnel_model.py` (line 70)

**What the model does:**  
The `CRMFunnelModel` predicts the probability of a lead applying or enrolling. One of its input features is `Person Citizenship (Primary)`.

**The problem:**  
Using national origin or citizenship to score leads is a form of demographic bias. If, historically, students from a certain country applied at lower rates, the model will continue predicting lower scores for those students — not because they are less likely to enroll, but because of historical patterns in the data. This creates a feedback loop that disadvantages specific groups and may constitute a disparate impact violation.

**Recommended improvement:**  
Remove `Person Citizenship (Primary)` from `self.feature_cols`. If geographic insight is needed, replace it with a broader regional grouping (e.g., region: North America, South Asia, Europe) rather than individual country/citizenship labels.

```python
# Current (risky)
self.feature_cols = ["Platform", "term_index", "Inquiry Major of Interest", "Person Citizenship (Primary)"]

# Recommended
self.feature_cols = ["Platform", "term_index", "Inquiry Major of Interest", "Applicant Region"]
```

---

## Improvement 2 — Add Model Drift Monitoring

**File:** `MarketMindServer/app/model_registry.py`

**What the system does:**  
Models are trained once from historical data and cached as `.pkl` files. They are reloaded on startup and used indefinitely until manually deleted.

**The problem:**  
The university's marketing behavior, platform costs, and applicant demographics change over time. A model trained on 2022–2024 data will produce increasingly inaccurate predictions by 2026 with no warning. There is currently no mechanism to detect this.

**Recommended improvement:**  
Log a prediction confidence score or an internal validation metric each time a model is loaded or used. Set a threshold — if the model's internal AUC or accuracy falls below a set baseline, automatically flag it for retraining. A simple implementation would log the stored AUC (already saved in `crm_summary.json`) and compare it against a defined minimum at startup.

```python
# In model_registry.py — on model load
if stored_auc < MINIMUM_ACCEPTABLE_AUC:
    logger.warning("Model AUC below threshold — retraining recommended.")
```

---

## Improvement 3 — Anonymize PII Before Training

**File:** `MarketMindServer/app/processors/` (CRM processing pipeline)

**What the system does:**  
Raw CRM exports containing student names, citizenship, and inquiry timelines are loaded directly into pandas DataFrames and used as training data without any anonymization step.

**The problem:**  
FERPA (the U.S. federal law governing student privacy) requires that individual student records be protected. If the server or training artifacts are ever exposed, raw identifiable student data could be leaked. The model also memorizes patterns from individual records, which is a known privacy attack surface (model inversion attacks).

**Recommended improvement:**  
Add a data anonymization step in the CRM processor before data reaches any model. At minimum:
- Drop all name/ID columns before training.
- Hash or generalize citizenship to a region.
- Apply k-anonymity checks (ensure no demographic sub-group has fewer than k=5 records).

```python
# In CRM processor, before model training
COLUMNS_TO_DROP = ["Student Name", "Email", "Phone", "Student ID"]
df = df.drop(columns=[c for c in COLUMNS_TO_DROP if c in df.columns])
```

---

## Improvement 4 — Replace Pickle with a Safer Serialization Format

**File:** `MarketMindServer/app/models/crm/crm_funnel_model.py` (lines 139, 153)

**What the system does:**  
All trained models are saved using `joblib.dump()`, which uses Python's `pickle` protocol internally.

**The problem:**  
Pickle files execute arbitrary Python code on load. If a `.pkl` file in `saved_models/` is ever replaced by a malicious file (e.g., via a compromised S3 bucket or a supply chain attack), loading it via `joblib.load()` will run that code with full server privileges.

**Recommended improvement:**  
- Add a SHA-256 checksum file alongside every `.pkl` at save time.
- Verify the checksum before loading any `.pkl`.
- For Phase 3, migrate to ONNX or `skops` (a scikit-learn safe serialization library designed to replace pickle).

```python
import hashlib, json

def save_model_with_checksum(model, path):
    joblib.dump(model, path)
    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
    with open(path + ".sha256", "w") as f:
        json.dump({"sha256": digest}, f)

def load_model_with_checksum(path):
    stored = json.load(open(path + ".sha256"))["sha256"]
    actual = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if stored != actual:
        raise SecurityError("Model file checksum mismatch — refusing to load.")
    return joblib.load(path)
```

---

## Improvement 5 — Replace Hardcoded Fusion Weights with Auto-Calibration

**File:** `MarketMindServer/app/predictors/platform_predictor.py` (lines 20–22)

**What the system does:**  
The `FusionPredictor` blends the Platform model's prediction with the Content model's prediction using weights of `0.7` (platform) and `0.3` (content). These values are hardcoded.

**The problem:**  
There is an open `TODO` comment in the code confirming these values were never validated. Using arbitrary weights without calibration means the final prediction quality is unknown and cannot be trusted in a production context.

**Recommended improvement:**  
Use the held-out test set from training to find the optimal weight ratio by minimizing prediction error. This can be done once at training time and the optimal weights stored alongside the `.pkl` files.

```python
# Replace hardcoded default
w_platform = 0.7  # TODO: replace with true variance analysis

# With a calibrated value loaded from training logs
w_platform = load_calibrated_weight("platform_content_weight.json")
```

---

## What Is Already Done Well

### ✅ Human Override Controls
The `/predict` endpoint accepts `platform_weight` and `content_weight` as optional user inputs. Marketing managers can manually override the model's weighting when they have contextual knowledge the model lacks (e.g., a new ad format not present in training data). This is a strong human-in-the-loop design.

### ✅ Explainable, Step-by-Step Output
Instead of returning a single "ROI score," the system returns each stage of the prediction funnel — allocated budget, CPC, estimated clicks, inquiries, enrollments, and final net ROI — as separate values. Users can audit each step independently and catch where projections look unreasonable.

### ✅ Honest Scope Documentation
The Phase 2 README explicitly documents all known model limitations — including the 9-row test sample, distribution shift, and missing ad copy data. This type of honest scope disclosure directly reduces the risk of over-reliance on model output.

---

## Summary

MarketMind Phase 2 has a functional and well-documented ML system with genuine human oversight built in. The most important improvements are:

1. **Remove citizenship as a model feature** — prevents demographic bias in lead scoring.
2. **Anonymize CRM data before training** — required for FERPA compliance.
3. **Add drift detection** — prevents silent model degradation over time.
4. **Checksum-verify model files** — closes a real serialization security hole.
5. **Calibrate the fusion weights** — makes prediction quality verifiable, not assumed.

Items 1, 2, and 3 should be prioritized before any production or multi-institution deployment.

---

*Audit conducted via manual code review of the MarketMind Phase 2 repository — October 2026.*
