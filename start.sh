#!/bin/bash
set -e

echo "🚀 Starting FastAPI backend on port ${API_PORT:-8001}..."
uvicorn main:app --host 0.0.0.0 --port ${API_PORT:-8001} &

echo "🎓 Starting Streamlit frontend on port ${PORT:-8000}..."
streamlit run app.py \
  --server.port ${PORT:-8000} \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false &

# Keep container alive; exit if either process dies
wait -n
echo "❌ A process exited. Shutting down..."
exit 1
