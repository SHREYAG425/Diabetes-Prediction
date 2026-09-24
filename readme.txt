# Diabetes Risk Prediction

A machine learning web app that predicts diabetes risk from clinical measurements. Built with scikit-learn and Flask, with an interactive frontend using vanilla JavaScript.

## Overview

This project compares two classification models — Logistic Regression and a Decision Tree — trained on 100,000 patient records, and deploys the stronger performer behind a simple, interactive web interface. Users enter health measurements (age, BMI, HbA1c, blood glucose, hypertension, heart disease, smoking history, gender) and get an instant risk prediction with a confidence score.

## Model performance

| Model | Test Accuracy |
|---|---|
| Logistic Regression | 96.2% |
| Decision Tree (selected) | 97.2% |

Both models were evaluated on a stratified 80/20 train-test split, using a confusion matrix to check for class imbalance issues (the dataset is ~91.5% non-diabetic / 8.5% diabetic).

Feature importance (from the trained Decision Tree) shows the model relies almost entirely on two clinically meaningful features:

| Feature | Importance |
|---|---|
| HbA1c level | 65.3% |
| Blood glucose level | 32.1% |
| BMI | 1.3% |
| Age | 1.2% |
| Hypertension | 0.1% |
| Gender, smoking history, heart disease | ~0% |

This lines up with real diagnostic criteria — HbA1c ≥ 6.5% and fasting glucose ≥ 126 mg/dL are the standard clinical thresholds for diabetes — which suggests the model learned medically sound patterns rather than spurious correlations.

## Tech stack

- Machine learning: Python, scikit-learn, pandas
- Backend: Flask (JSON API)
- Frontend: HTML, CSS, vanilla JavaScript (fetch API for async predictions, no page reload)
- Deployment: Render, gunicorn

