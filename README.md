# Student Performance Prediction System

A full-stack ML application for predicting student performance using Logistic Regression, with a FastAPI backend and Streamlit frontend.

## 📁 Project Structure

```
student_performance/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── train.py                # Model training script
│   ├── requirements.txt         # Backend dependencies
│   ├── Dockerfile              # Backend container
│   ├── Student_Performance.csv  # Training dataset
│   └── model/                  # Saved model artifacts
│       ├── trained_model.pkl
│       └── scaler.pkl
│
├── frontend/
│   ├── app.py                  # Streamlit application
│   ├── requirements.txt         # Frontend dependencies
│   └── Dockerfile              # Frontend container
│
├── docker-compose.yml          # Orchestrate both services
└── .gitattributes              # Line ending configuration
```

## 🚀 Quick Start

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python train.py              # Train model (first time only)
uvicorn main:app --reload --port 8001
```

**Frontend (in new terminal):**
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501` and set API URL to `http://localhost:8001`.

### Docker Compose (Recommended)

```bash
docker-compose up -d
```

Access the app at `http://localhost:8000`.

## 📊 Features

- **Backend (FastAPI on port 8001)**
  - `/predict` - Single prediction endpoint
  - `/health` - Health check
  - Model training with scikit-learn
  - CORS enabled for frontend communication

- **Frontend (Streamlit on port 8000)**
  - Interactive student profile input
  - Real-time predictions
  - Probability visualization
  - Beautiful UI with custom CSS

## 🔧 Configuration

### Environment Variables

For production deployment (e.g., Railway):
- `PORT=8000` (exposed port for Streamlit)
- `API_PORT=8001` (internal FastAPI port)

### API URL

Frontend defaults to `http://localhost:8001` locally. 
In Docker/Production, services communicate via `http://backend:8001`.

## 📦 Dependencies

**Backend:**
- FastAPI, Uvicorn
- scikit-learn, pandas, numpy
- joblib (model persistence)

**Frontend:**
- Streamlit
- requests, pandas, numpy

## 🚢 Deployment

For Railway:
1. Set port to `8000` (Streamlit)
2. Both services run in one container via docker-compose
3. Frontend proxies to backend internally

## 📝 License

[Your License Here]
