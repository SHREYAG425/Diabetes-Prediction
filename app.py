"""
app.py

The web app. Loads the saved model pipeline once when the server starts.
The homepage serves the interactive form. When the form is submitted,
JavaScript (see static/script.js) sends the data to /predict using fetch(),
and this route sends back a JSON answer — no page reload needed.
"""

import pickle
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

numeric_features = ["age", "hypertension", "heart_disease", "bmi", "HbA1c_level", "blood_glucose_level"]
categorical_features = ["gender", "smoking_history"]
all_features = numeric_features + categorical_features


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Build a one-row table with the same column names used in training.
    row = {}
    for col in numeric_features:
        row[col] = [float(data[col])]
    for col in categorical_features:
        row[col] = [data[col]]

    input_df = pd.DataFrame(row)[all_features]

    prediction = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])

    return jsonify({
        "prediction": prediction,
        "probability": round(probability * 100, 1),
        "label": "Higher risk of diabetes" if prediction == 1 else "Lower risk of diabetes",
    })


if __name__ == "__main__":
    app.run(debug=True)