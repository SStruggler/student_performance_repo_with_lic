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
EXPOSE 8000

# ── Start Streamlit ───────────────────────────────────────────────────────────
CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0", "--server.headless=true"]
