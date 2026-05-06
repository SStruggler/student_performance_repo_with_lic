#!/bin/bash
set -e

echo "🚀 Starting FastAPI backend on port ${PORT:-8000}..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} &

echo "🎓 Starting Streamlit frontend on port ${STREAMLIT_PORT:-8501}..."
streamlit run app.py \
  --server.port ${STREAMLIT_PORT:-8501} \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false &

# Keep container alive; exit if either process dies
wait -n
echo "❌ A process exited. Shutting down..."
exit 1
