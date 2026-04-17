#  Delivery Checklist — Day 12 Lab Submission

> **Student Name:** Phan Văn Tấn 
> **Student ID:** 2A202600282
> **Date:** 17/04/2026

---

##  Submission Requirements

Submit a **GitHub repository** containing:

### 1. Mission Answers (40 points)

Create a file `MISSION_ANSWERS.md` with your answers to all exercises:

```markdown
# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. API key và DATABASE_URL hardcode trong code
2. Không có config management có thể bỏ trong file .env
3. Print thay vì proper logging khó quản lý log và có thể print luôn cả key bí mật nữa.
4. Không có health check endpoint
5. Port cố định — không đọc từ environment
...

### Exercise 1.3: Comparison table
| Feature | Basic | Advanced | Tại sao quan trọng? |
|---------|-------|----------|---------------------|
| Config | Hardcode | Env vars |Ngăn chặn lộ API Key/Password lên Git. Dễ dàng thay đổi cấu hình cho các môi trường khác nhau (Dev/Prod) mà không cần sửa code.|
| Health check | không | Có endpoint riêng |Giúp các nền tảng (Render, Kubernetes) biết ứng dụng có đang sống không để tự động khởi động lại (auto-restart) hoặc điều hướng traffic nếu app bị treo. |
| Logging | print() | JSON | Log JSON giúp các hệ thống quản lý log dễ dàng parse (đọc/hiểu), lọc lỗi theo mức độ (INFO, ERROR) và tìm kiếm nguyên nhân khi hệ thống sập. |
| Shutdown | Đột ngột | Graceful | Cho phép ứng dụng xử lý nốt các request đang dang dở và đóng kết nối database an toàn trước khi tắt, tránh mất mát dữ liệu của người dùng.|
...

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image là gì? Nó sẽ tái sử dụng lại tối đa những gì chưa bị thay đổi ở các lần build trước, giúp tốc độ phát triển và cập nhật phần mềm nhanh hơn gấp nhiều lần.
2. Working directory là gì? là thư mục hiện tại mà chương trình hoặc terminal đang “đứng” để thực thi lệnh và truy cập file.
3. Tại sao COPY requirements.txt trước? tận dụng Docker cache,tăng tốc build,tránh reinstall dependencies không cần thiết.
4. CMD vs ENTRYPOINT khác nhau thế nào? CMD là lệnh mặc định có thể bị ghi đè,ENTRYPOINT lệnh cố định không dễ bị override
...

### Exercise 2.3: Image size comparison
- Develop: [413] MB
- Production: [56.7] MB
- Difference: [86.3]%

## Part 3: Cloud Deployment

### Exercise 3.1: Render deployment
- URL: https://ai-agent-qb4o.onrender.com
- Screenshot: [Link to screenshot in repo]
![alt text](screenshot/image.png)
![alt text](screenshot/image1.png)

## Part 4: API Security

### Exercise 4.1-4.3: Test results
[Paste your test outputs]
#develop
##  Không có key
(venv) (base) macos@MACBOOKPRO develop % curl -X POST -H "Content-Type: application/json" \ 
         -d '{"question":"hello"}' \ 
         http://localhost:8000/ask
{"detail":"Missing API key. Include header: X-API-Key: <your-key>"}%  
## có key 
(venv) (base) macos@MACBOOKPRO develop % curl -H "X-API-Key: demo-key-change-in-production" \
     -X POST \
     "http://localhost:8000/ask?question=hello"
{"question":"hello","answer":"Đây là câu trả lời từ AI agent (mock). Trong production, đây sẽ là response từ OpenAI/Anthropic."}%  
#production
## lấy token
(venv) (base) macos@MACBOOKPRO production % curl -X POST http://localhost:8000/auth/token \ 
         -H "Content-Type: application/json" \ 
         -d '{"username": "student", "password": "demo123"}'
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHVkZW50Iiwicm9sZSI6InVzZXIiLCJpYXQiOjE3NzY0MjU1NzMsImV4cCI6MTc3NjQyOTE3M30.997fJDX7x0qsZCP1pRTh6aHoBLWSbWgoPFAYWmcpMk8","token_type":"bearer","expires_in_minutes":60,"hint":"Include in header: Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."}%           
## dùng token
(venv) (base) macos@MACBOOKPRO production % curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHVkZW50Iiwicm9sZSI6InVzZXIiLCJpYXQiOjE3NzY0MjU1NzMsImV4cCI6MTc3NjQyOTE3M30.997fJDX7x0qsZCP1pRTh6aHoBLWSbWgoPFAYWmcpMk8" \  
         -X POST http://localhost:8000/ask \
         -H "Content-Type: application/json" \
         -d '{"question": "what is docker?"}'
{"question":"what is docker?","answer":"Container là cách đóng gói app để chạy ở mọi nơi. Build once, run anywhere!","usage":{"requests_remaining":9,"budget_remaining_usd":1.9e-05}}%  
### Exercise 4.4: Cost guard implementation
- Algorithm nào được dùng? Hệ thống sử dụng Sliding Window Counter. Mỗi user có một danh sách timestamp (deque), các request cũ ngoài khoảng 60 giây sẽ bị loại bỏ trước khi kiểm tra limit.
- Limit là bao nhiêu requests/minute?	User thường: 10 requests/phút, Admin: 100 requests/phút
- Làm sao bypass limit cho admin?Admin không hoàn toàn bypass mà được cấp limit cao hơn bằng cách sử dụng một rate limiter riêng (rate_limiter_admin). Khi hệ thống nhận request, nếu role là admin thì sẽ dùng limiter này thay vì limiter của user thường.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
[Your explanations and test results]
```
- 5.1
  (venv) (base) macos@MACBOOKPRO production % curl http://localhost:8000/health
  {"status":"ok","uptime_seconds":10.6,"version":"1.0.0","environment":"development","timestamp":"2026-04-17T12:12:42.584008+00:00","checks":{"memory":{"status":"ok","used_percent":77.8}}}%  
- 5.2
  (venv) (base) macos@MACBOOKPRO production % curl http://localhost:8000/ready
  {"ready":true,"in_flight_requests":1}% 
---

### 2. Full Source Code - Lab 06 Complete (60 points)

Your final production-ready agent with all files:

```
your-repo/
├── app/
│   ├── main.py              # Main application
│   ├── config.py            # Configuration
│   ├── auth.py              # Authentication
│   ├── rate_limiter.py      # Rate limiting
│   └── cost_guard.py        # Cost protection
├── utils/
│   └── mock_llm.py          # Mock LLM (provided)
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Full stack
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
├── .dockerignore            # Docker ignore
├── railway.toml             # Railway config (or render.yaml)
└── README.md                # Setup instructions
```

**Requirements:**
-  All code runs without errors
-  Multi-stage Dockerfile (image < 500 MB)
-  API key authentication
-  Rate limiting (10 req/min)
-  Cost guard ($10/month)
-  Health + readiness checks
-  Graceful shutdown
-  Stateless design (Redis)
-  No hardcoded secrets

=======================================================
  Production Readiness Check — Day 12 Lab
=======================================================

📁 Required Files
  ✅ Dockerfile exists
  ✅ docker-compose.yml exists
  ✅ .dockerignore exists
  ✅ .env.example exists
  ✅ requirements.txt exists
  ✅ railway.toml or render.yaml exists

🔒 Security
  ✅ .env in .gitignore
  ✅ No hardcoded secrets in code

🌐 API Endpoints (code check)
  ✅ /health endpoint defined
  ✅ /ready endpoint defined
  ✅ Authentication implemented
  ✅ Rate limiting implemented
  ✅ Graceful shutdown (SIGTERM)
  ✅ Structured logging (JSON)

🐳 Docker
  ✅ Multi-stage build
  ✅ Non-root user
  ✅ HEALTHCHECK instruction
  ✅ Slim base image
  ✅ .dockerignore covers .env
  ✅ .dockerignore covers __pycache__

=======================================================
  Result: 20/20 checks passed (100%)
  🎉 PRODUCTION READY! Deploy nào!
=======================================================
---

### 3. Service Domain Link

Create a file `DEPLOYMENT.md` with your deployed service information:

```markdown
# Deployment Information

## Public URL
https://ai-agent-qb4o.onrender.com

## Platform
Railway / Render / Cloud Run

## Test Commands

### Health Check
```bash
curl https://your-agent.railway.app/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST https://your-agent.railway.app/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "question": "Hello"}'
```

## Environment Variables Set
- PORT
- REDIS_URL
- AGENT_API_KEY
- LOG_LEVEL

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
```

##  Pre-Submission Checklist

- [ ] Repository is public (or instructor has access)
- [ ] `MISSION_ANSWERS.md` completed with all exercises
- [ ] `DEPLOYMENT.md` has working public URL
- [ ] All source code in `app/` directory
- [ ] `README.md` has clear setup instructions
- [ ] No `.env` file committed (only `.env.example`)
- [ ] No hardcoded secrets in code
- [ ] Public URL is accessible and working
- [ ] Screenshots included in `screenshots/` folder
- [ ] Repository has clear commit history

---

##  Self-Test

Before submitting, verify your deployment:

```bash
# 1. Health check
curl https://your-app.railway.app/health

# 2. Authentication required
curl https://your-app.railway.app/ask
# Should return 401

# 3. With API key works
curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
  -X POST -d '{"user_id":"test","question":"Hello"}'
# Should return 200

# 4. Rate limiting
for i in {1..15}; do 
  curl -H "X-API-Key: YOUR_KEY" https://your-app.railway.app/ask \
    -X POST -d '{"user_id":"test","question":"test"}'; 
done
# Should eventually return 429
```

---

##  Submission

**Submit your GitHub repository URL:**

```
https://github.com/PhanVanTann/PhanVanTan_2A202600282_Day12
```

**Deadline:** 17/4/2026

---

##  Quick Tips

1.  Test your public URL from a different device
2.  Make sure repository is public or instructor has access
3.  Include screenshots of working deployment
4.  Write clear commit messages
5.  Test all commands in DEPLOYMENT.md work
6.  No secrets in code or commit history

---

##  Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [CODE_LAB.md](CODE_LAB.md)
- Ask in office hours
- Post in discussion forum

---

**Good luck! **
