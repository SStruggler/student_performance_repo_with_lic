# Frontend - Streamlit Student Performance UI

## Overview

This is the interactive frontend service that:
- Provides a beautiful web UI for predictions
- Collects student data via sliders and inputs
- Displays prediction results with visualizations
- Communicates with the FastAPI backend

## 🚀 Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start Streamlit app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🎨 Features

- **Student Profile Input**
  - Hours studied (1-9)
  - Previous test scores (40-100)
  - Sleep hours (4-9)
  - Sample papers practiced (0-9)
  - Extracurricular activities (Yes/No)

- **Prediction Display**
  - Pass/Fail verdict with confidence
  - Probability breakdown with visual bars
  - Input summary expandable section

- **Configuration**
  - Sidebar option to set custom API URL
  - Defaults to `http://localhost:8001`

## 🐳 Docker

Build and run:
```bash
docker build -t student-perf-ui .
docker run -p 8000:8000 -e API_URL=http://localhost:8001 student-perf-ui
```

## ⚙️ Configuration

### API URL

Change the default API URL by:
1. Using the sidebar input in the UI, or
2. Setting environment variable: `API_URL=http://your-api:8001`

### Streamlit Config

Settings can be adjusted in `~/.streamlit/config.toml` or via Docker CMD.

## 🔗 Integration with Backend

The frontend makes POST requests to:
- `{API_URL}/predict` - Get predictions

Ensure the backend service is running and accessible.

## 🎯 Error Handling

The app gracefully handles:
- Connection errors (backend offline)
- Timeout errors (slow responses)
- HTTP errors (invalid requests)
- Unexpected errors (logging)

All errors are displayed in red alert boxes.
