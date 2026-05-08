# ── Base Image ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── Environment ───────────────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ── System Dependencies ───────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ── Working Directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Python Dependencies ───────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy Project Files ────────────────────────────────────────────────────────
COPY . .

# ── Train the Model at Build Time ─────────────────────────────────────────────
RUN python train.py

# ── Expose Port ────────────────────────────────────────────────────────────────
# Railway will inject PORT at runtime; 8001 remains the local default.
EXPOSE 8001

# ── Start FastAPI ───────────────────────────────────────────────────────────────
# Use shell form to allow $PORT expansion when Railway runs the container.
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
