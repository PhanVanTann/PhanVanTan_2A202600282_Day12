import os

class Settings:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    app_name = os.getenv("APP_NAME", "AI Agent")
    app_version = os.getenv("APP_VERSION", "1.0.0")

    agent_api_key = os.getenv("AGENT_API_KEY", "dev-key")
    redis_url = os.getenv("REDIS_URL", "")

    rate_limit_per_minute = int(os.getenv("RATE_LIMIT", 10))
    daily_budget_usd = float(os.getenv("BUDGET", 10))

    allowed_origins = ["*"]

settings = Settings()