from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd

app = FastAPI(
    title="Student Performance Prediction API",
    description="Uses Logistic Regression to predict if a student passes (Performance Index >= 60).",
    version="1.0.0"
)

# 1. Load the model and scaler
try:
    model = joblib.load('model/trained_model.pkl')
    scaler = joblib.load('model/scaler.pkl')
except Exception as e:
    model = None
    scaler = None

# 2. Define Request Schema
FEATURE_COLS = [
    'Hours Studied',
    'Previous Scores',
    'Extracurricular Activities',
    'Sleep Hours',
    'Sample Question Papers Practiced'
]

class StudentFeatures(BaseModel):
    hours_studied: float = Field(..., ge=1, le=9, description="Hours studied between 1 and 9")
    previous_scores: float = Field(..., ge=40, le=100, description="Previous test scores between 40 and 100")
    extracurricular_activities: int = Field(..., ge=0, le=1, description="1 for Yes, 0 for No")
    sleep_hours: float = Field(..., ge=4, le=9, description="Sleep hours between 4 and 9")
    sample_question_papers: int = Field(..., ge=0, le=9, description="Number of papers practiced")

@app.get("/", tags=["Health Check"])
def root():
    return {"message": "Student Performance Predictor API is active."}

@app.post("/predict", tags=["Prediction"])
def predict_performance(data: StudentFeatures):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model is not loaded properly. Train the model first.")
    
    # Extract features in the same format used at training
    features = pd.DataFrame([
        [
            data.hours_studied,
            data.previous_scores,
            data.extracurricular_activities,
            data.sleep_hours,
            data.sample_question_papers,
        ]
    ], columns=FEATURE_COLS)
    
    # Scale features
    scaled_features = scaler.transform(features)
    
    # Predict
    prediction = model.predict(scaled_features)
    probabilities = model.predict_proba(scaled_features)
    
    result = "Pass" if prediction[0] == 1 else "Fail"
    confidence = float(np.max(probabilities))
    
    return {
        "prediction": result,
        "confidence_score": round(confidence, 4),
        "pass_probability": round(probabilities[0][1], 4),
        "fail_probability": round(probabilities[0][0], 4)
    }