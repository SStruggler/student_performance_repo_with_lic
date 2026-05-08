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

# ── Expose Port ────────────────────────────────────────────────────────────────
# Railway will inject the runtime PORT value, so 8001 is only a default for local builds.
EXPOSE 8001

# ── Start Streamlit ───────────────────────────────────────────────────────────────
# Use shell form so the $PORT environment variable expands at runtime.
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
