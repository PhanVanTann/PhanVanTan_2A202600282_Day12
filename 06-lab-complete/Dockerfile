# ─────────────────────────────
# STAGE 1: Builder
# ─────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt


# ─────────────────────────────
# STAGE 2: Runtime
# ─────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# create non-root user (bonus but recommended)
RUN useradd -m appuser
USER appuser

# copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# copy source code
COPY --chown=appuser:appuser . .

# env path for pip packages
ENV PATH="/home/appuser/.local/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
CMD curl -f http://localhost:8000/health || exit 1