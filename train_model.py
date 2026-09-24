"""
train_model.py

Trains on the diabetes_prediction_dataset (100,000 records, both genders).
Everything — encoding categories, scaling numbers, and the classifier itself —
is bundled into ONE scikit-learn Pipeline, so we only need to save ONE file
(model.pkl) for app.py to use.
"""

import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix


# ---- Step 1: Load the data ----
data = pd.read_csv("diabetes.csv")

# Columns that are numbers
numeric_features = ["age", "hypertension", "heart_disease", "bmi", "HbA1c_level", "blood_glucose_level"]

# Columns that are text categories (need to be converted to numbers)
categorical_features = ["gender", "smoking_history"]

target_column = "diabetes"

X = data[numeric_features + categorical_features]
y = data[target_column]


# ---- Step 2: Split into training and testing data ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=43, stratify=y
)


# ---- Step 3: Build a preprocessing + model pipeline ----
# ColumnTransformer applies different preprocessing to different columns:
# - numeric columns get scaled (so all numbers are on a similar range)
# - categorical columns get "one-hot encoded" (turned into 0/1 columns,
#   e.g. gender_Male, gender_Female, gender_Other)
preprocessor = ColumnTransformer(transformers=[
    ("numbers", StandardScaler(), numeric_features),
    ("categories", OneHotEncoder(handle_unknown="ignore"), categorical_features),
])

log_reg_pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("model", LogisticRegression(max_iter=1000, random_state=43)),
])

tree_pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("model", DecisionTreeClassifier(max_depth=6, random_state=43)),
])


# ---- Step 4: Train both models ----
log_reg_pipeline.fit(X_train, y_train)
tree_pipeline.fit(X_train, y_train)


# ---- Step 5: Compare accuracy ----
lr_predictions = log_reg_pipeline.predict(X_test)
tree_predictions = tree_pipeline.predict(X_test)

lr_accuracy = accuracy_score(y_test, lr_predictions)
tree_accuracy = accuracy_score(y_test, tree_predictions)

print(f"Logistic Regression accuracy: {lr_accuracy * 100:.1f}%")
print(f"Decision Tree accuracy:       {tree_accuracy * 100:.1f}%")

print("\nLogistic Regression confusion matrix:")
print(confusion_matrix(y_test, lr_predictions))
print("\nDecision Tree confusion matrix:")
print(confusion_matrix(y_test, tree_predictions))

if lr_accuracy >= tree_accuracy:
    best_pipeline = log_reg_pipeline
    best_name = "Logistic Regression"
else:
    best_pipeline = tree_pipeline
    best_name = "Decision Tree"

print(f"\nBest model: {best_name} — saving it to model.pkl")


# ---- Step 6: Save the whole pipeline (preprocessing + model) as ONE file ----
with open("model.pkl", "wb") as f:
    pickle.dump(best_pipeline, f)

print("Done. Saved model.pkl")