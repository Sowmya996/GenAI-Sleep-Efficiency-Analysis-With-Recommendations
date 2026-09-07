
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
data = pd.read_csv("sleep_data.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)


# Remove Person ID because it is not useful for prediction
if "Person ID" in data.columns:
    data = data.drop(columns=["Person ID"])


# Separate input features and target
X = data.drop(columns=["Sleep Disorder"])
y = data["Sleep Disorder"]


# Categorical columns
categorical_columns = [
    "Gender",
    "Occupation",
    "BMI Category",
    "Blood Pressure"
]


# Numerical columns
numerical_columns = [
    "Age",
    "Sleep Duration",
    "Quality of Sleep",
    "Physical Activity Level",
    "Stress Level",
    "Heart Rate",
    "Daily Steps"
]


# Convert categorical values into numbers
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        ),
        (
            "numerical",
            "passthrough",
            numerical_columns
        )
    ]
)


# Random Forest model
classifier = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# Combine preprocessing + model
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ]
)


# Split dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Train model
print("\nTraining model...")

model.fit(X_train, y_train)

print("Training completed!")


# Test model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:")
print(round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# Save trained model
joblib.dump(model, "sleep_model.pkl")

print("\nSUCCESS!")
print("Model saved as sleep_model.pkl")
