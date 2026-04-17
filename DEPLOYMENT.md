# Deployment Information

## Public URL
https://ai-agent-qb4o.onrender.com

## Platform
Render

---

## Test Commands

### 1. Health Check (public endpoint)

```bash
curl https://ai-agent-qb4o.onrender.com/auth/health/
```
### API Test (with authentication)
```bash
curl -X POST https://ai-agent-qb4o.onrender.com/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"lap@gmail.com","password":"123456"}'
- result :{"success": true, "message": "Login successful", "user_id": "6896f2040d8ae3b3c114a531", "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjg5NmYyMDQwZDhhZTNiM2MxMTRhNTMxIiwicm9sZSI6InVzZXIiLCJleHAiOjE3NzY0NTUwMjAsInB1cnBvc2UiOiJ1c2VyX2F1dGhlbnRpY2F0aW9uIn0.UqmhI5EJgj1gHaxu9hxHdcdCJBvh8_ZkoosWBAHGOs4", "role": "user"}
```
lấy access_token gán vào dưới
```bash

curl "https://ai-agent-qb4o.onrender.com/users/?user_id=6896f2040d8ae3b3c114a531" \
  --cookie "access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjg5NmYyMDQwZDhhZTNiM2MxMTRhNTMxIiwicm9sZSI6InVzZXIiLCJleHAiOjE3NzY0NTUwMjAsInB1cnBvc2UiOiJ1c2VyX2F1dGhlbnRpY2F0aW9uIn0.UqmhI5EJgj1gHaxu9hxHdcdCJBvh8_ZkoosWBAHGOs4"


- result :{"success": true, "data": {"_id": "6896f2040d8ae3b3c114a531", "email": "lap@gmail.com", "first_name": "cuzz", "last_name": "lap", "role": "user", "avatar": "https://res.cloudinary.com/debzpay3s/image/upload/v1756717265/ckmvu07p3pcghkhcysbq.png", "introduce": "\r\nng\u01b0\u1eddi b\u00ecnh th\u01b0\u1eddng"}}
```
## Environment Variables Set
#Mongo url
MOGO_URL = 
MOGO_DB_NAME = ThreadsCity

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
#Email host user and password
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

SECRET_KEY=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

API_KEY=
API_SECRET = 
CLOUD_NAME = 
## Screenshots
![Deployment dashboard](screenshot/image3.png)
![Service running](screenshot/image4.png)
![Test results](screenshot/image5.png)
