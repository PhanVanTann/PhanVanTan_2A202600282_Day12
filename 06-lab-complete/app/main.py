"""
Production AI Agent — Fixed Version (Lab 06)

Features:
  ✔ Config from env
  ✔ JSON logging
  ✔ API Key auth
  ✔ Rate limiting
  ✔ Cost guard
  ✔ Validation
  ✔ Health / Ready
  ✔ Graceful shutdown
  ✔ Security headers
  ✔ CORS
"""

import time
import json
import asyncio
import signal
import logging
from datetime import datetime, timezone
from collections import defaultdict, deque
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Security, Depends, Request, Response
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from app.config import settings
from utils.mock_llm import call_llm as llm_ask   # ✅ FIXED IMPORT

# ─────────────────────────────────────────────
# Logging (JSON structured)
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='{"ts":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}',
)

logger = logging.getLogger("agent")

# ─────────────────────────────────────────────
# Runtime state
# ─────────────────────────────────────────────
START_TIME = time.time()
_is_ready = False

_request_count = 0
_error_count = 0

# ─────────────────────────────────────────────
# Rate Limiter (in-memory)
# ─────────────────────────────────────────────
_rate_windows = defaultdict(deque)

def check_rate_limit(key: str):
    now = time.time()
    window = _rate_windows[key]

    while window and window[0] < now - 60:
        window.popleft()

    if len(window) >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded (10 req/min)",
            headers={"Retry-After": "60"},
        )

    window.append(now)

# ─────────────────────────────────────────────
# Cost Guard (simple daily budget)
# ─────────────────────────────────────────────
_daily_cost = 0.0
_cost_day = time.strftime("%Y-%m-%d")

def check_and_record_cost(input_tokens: int, output_tokens: int):
    global _daily_cost, _cost_day

    today = time.strftime("%Y-%m-%d")

    if today != _cost_day:
        _daily_cost = 0.0
        _cost_day = today

    cost = (input_tokens / 1000) * 0.00015 + (output_tokens / 1000) * 0.0006

    if _daily_cost + cost > settings.daily_budget_usd:
        raise HTTPException(
            status_code=402,
            detail="Daily budget exceeded"
        )

    _daily_cost += cost

# ─────────────────────────────────────────────
# Auth
# ─────────────────────────────────────────────
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != settings.agent_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    return api_key

# ─────────────────────────────────────────────
# Lifespan
# ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready

    logger.info(json.dumps({"event": "startup"}))

    await asyncio.sleep(0.1)

    _is_ready = True
    logger.info(json.dumps({"event": "ready"}))

    yield

    _is_ready = False
    logger.info(json.dumps({"event": "shutdown"}))

# ─────────────────────────────────────────────
# App
# ─────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Middleware (logging + security headers)
# ─────────────────────────────────────────────
@app.middleware("http")
async def middleware(request: Request, call_next):
    global _request_count, _error_count

    start = time.time()
    _request_count += 1

    try:
        response: Response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"

        duration = round((time.time() - start) * 1000, 2)

        logger.info(json.dumps({
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "ms": duration,
        }))

        return response

    except Exception as e:
        _error_count += 1
        logger.error(json.dumps({"error": str(e)}))
        raise

# ─────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)

class AskResponse(BaseModel):
    question: str
    answer: str
    model: str
    timestamp: str

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "uptime": round(time.time() - START_TIME, 2),
        "requests": _request_count
    }


@app.get("/ready")
def ready():
    if not _is_ready:
        raise HTTPException(503, "Not ready")
    return {"ready": True}


@app.post("/ask", response_model=AskResponse)
def ask(
    body: AskRequest,
    request: Request,
    api_key: str = Depends(verify_api_key),
):
    # Rate limit
    check_rate_limit(api_key)

    # Fake token estimation
    input_tokens = len(body.question.split()) * 2
    check_and_record_cost(input_tokens, 0)

    answer = llm_ask(body.question)

    output_tokens = len(answer.split()) * 2
    check_and_record_cost(0, output_tokens)

    return AskResponse(
        question=body.question,
        answer=answer,
        model=settings.llm_model,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@app.get("/metrics")
def metrics(api_key: str = Depends(verify_api_key)):
    return {
        "requests": _request_count,
        "errors": _error_count,
        "uptime": round(time.time() - START_TIME, 2),
        "daily_cost": round(_daily_cost, 6),
        "budget": settings.daily_budget_usd,
    }

# ─────────────────────────────────────────────
# Graceful shutdown
# ─────────────────────────────────────────────
def handle_sigterm(*_):
    logger.info("SIGTERM received")

signal.signal(signal.SIGTERM, handle_sigterm)

# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )