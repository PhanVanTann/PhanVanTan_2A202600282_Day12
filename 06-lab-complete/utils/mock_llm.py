"""
Mock LLM — Production-safe version for FastAPI demo.
No external API required.
"""
import asyncio
import random


MOCK_RESPONSES = {
    "default": [
        "Đây là câu trả lời từ AI agent (mock).",
        "Agent đang hoạt động tốt 🚀",
        "Tôi là AI agent deployed trên cloud.",
    ],
    "docker": ["Docker giúp đóng gói ứng dụng chạy mọi môi trường."],
    "deploy": ["Deployment là quá trình đưa app lên server."],
    "health": ["System OK — all services running."],
}


def ask(question: str) -> str:
    """Sync mock response (safe for FastAPI sync endpoints)."""

    q = question.lower()

    for k, v in MOCK_RESPONSES.items():
        if k in q:
            return random.choice(v)

    return random.choice(MOCK_RESPONSES["default"])


# ─────────────────────────────
# Async-safe version (khuyến nghị)
# ─────────────────────────────
async def ask_async(question: str) -> str:
    await asyncio.sleep(0.1)  # non-blocking latency
    return ask(question)


# ─────────────────────────────
# Streaming mock
# ─────────────────────────────
async def ask_stream(question: str):
    response = ask(question)

    for word in response.split():
        await asyncio.sleep(0.05)
        yield word + " "