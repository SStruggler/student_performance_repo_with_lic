# Backend - FastAPI Student Performance API

## Overview

This is the ML backend service that:
- Trains a Logistic Regression model on student performance data
- Serves predictions via REST API
- Manages model persistence and preprocessing

## 🚀 Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Train model (run once)
python train.py

# Start API server
uvicorn main:app --reload --port 8001
```

API documentation: `http://localhost:8001/docs`

## 📚 API Endpoints

### `GET /`
Health check / status message

**Response:**
```json
{
  "message": "Student Performance Predictor API is active."
}
```

### `GET /health`
Detailed health status

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### `POST /predict`
Make a prediction for a student

**Request:**
```json
{
  "hours_studied": 5.5,
  "previous_scores": 75.0,
  "extracurricular_activities": 1,
  "sleep_hours": 7.0,
  "sample_question_papers": 3
}
```

**Response:**
```json
{
  "prediction": "Pass",
  "confidence_score": 0.9234,
  "pass_probability": 0.9234,
  "fail_probability": 0.0766
}
```

## 🐳 Docker

Build and run:
```bash
docker build -t student-perf-api .
docker run -p 8001:8001 student-perf-api
```

## 📊 Model Details

- **Algorithm:** Logistic Regression
- **Target:** Pass (1) / Fail (0) based on Performance Index >= 60
- **Features:** 5 input features
- **Train/Test Split:** 80% / 20%
- **Saved Artifacts:** `model/` directory

## 🔄 Retraining

To retrain the model with new data:

```bash
python train.py
```

This will:
1. Load data from `Student_Performance.csv`
2. Preprocess and scale features
3. Train Logistic Regression
4. Save model to `model/trained_model.pkl`
5. Save scaler to `model/scaler.pkl`
