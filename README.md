# OpenClaw Dashboard - Production Setup Guide

## 🚀 Quick Start (Docker)
The fastest way to deploy the OpenClaw Dashboard is using Docker Compose.

```bash
git clone https://github.com/Omesh06/openclaw-dashboard.git
cd openclaw-dashboard
docker-compose up -d
```
The API will be available at `http://localhost:8000` and the Frontend at `http://localhost:3000`.

## 🛠️ Manual Installation

### Backend
1. `cd backend`
2. `python3 -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## ⚙️ Configuration
The backend requires a `.jira_config` file in the workspace root:
```env
JIRA_DOMAIN=your-domain.atlassian.net
JIRA_EMAIL=user@email.com
JIRA_API_TOKEN=your_token
```

## 📖 API Reference
- `GET /api/health/status`: Get global repo health.
- `GET /api/jira/ticket/{id}`: Fetch business intent.
- `POST /api/context/summarize`: AI Intent translation.
- `POST /api/safety/dry-run`: Verify merge in sandbox.
- `POST /api/safety/revert`: Emergency panic revert.
- `GET /api/queue/pending`: View HITL queue.
