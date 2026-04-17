# Deployment Information

## Public URL
https://ai-agent-qb4o.onrender.com

## Test

curl https://your-url/health

curl -X POST https://your-url/ask \
 -H "X-API-Key: dev-key" \
 -H "Content-Type: application/json" \
 -d '{"user_id":"1","question":"hello"}'