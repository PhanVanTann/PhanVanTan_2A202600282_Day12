from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import time
import json
import logging

from app.config import settings
from app.auth import verify_api_key
from app.rate_limiter import check_rate_limit
from app.cost_guard import add_cost
from utils.mock_llm import call_llm
import signal
import sys


# ─────────────────────────────
# JSON LOGGER (structured logging)
# ─────────────────────────────
logger = logging.getLogger("agent")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('{"level":"%(levelname)s","message":"%(message)s"}'))
logger.handlers = [handler]
logger.setLevel(logging.INFO)


def handle_sigterm(signum, frame):
    logger.info('{"event":"sigterm_received"}')
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)
# ─────────────────────────────
# Lifespan (Graceful shutdown đúng chuẩn)
# ─────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(json.dumps({"event": "startup"}))

    yield

    logger.info(json.dumps({"event": "shutdown"}))


# ─────────────────────────────
# App
# ─────────────────────────────
app = FastAPI(lifespan=lifespan)


class Req(BaseModel):
    user_id: str
    question: str


# ─────────────────────────────
# Endpoints
# ─────────────────────────────
@app.get("/health")
def health():
    logger.info(json.dumps({"event": "health_check"}))
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"ready": True}


@app.post("/ask")
def ask(req: Req, _=Depends(verify_api_key)):

    logger.info(json.dumps({"event": "ask", "user": req.user_id}))

    if not check_rate_limit(req.user_id, settings.rate_limit_per_minute):
        raise HTTPException(429, "Rate limit exceeded")

    cost = len(req.question) * 0.0001
    add_cost(cost, settings.daily_budget_usd)

    answer = call_llm(req.question)

    return {
        "answer": answer,
        "user": req.user_id,
        "ts": time.time()
    }