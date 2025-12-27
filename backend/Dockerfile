FROM python:3.11-slim

# 1. Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# 2. System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos '' appuser

# 3. Copy requirements and install
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 4. Copy the whole project
COPY --chown=appuser:appuser . .

# 5. FIX: Ensure app is a package so relative imports work
RUN touch /app/app/__init__.py

USER appuser

EXPOSE 8000

# 6. FIX: Run from the root using the module path
# This allows 'from .chat' inside main.py to work correctly
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]