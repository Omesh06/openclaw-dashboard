# 📖 OpenClaw Dashboard - API Specification

This document defines the REST API for the OpenClaw Dashboard.

## Base URL
`http://localhost:8000/api`

---

## 🛠️ Endpoints

### 1. Jira Integration (`/api/jira`)
- **`GET /ticket/{ticket_id}`**
    - **Description**: Fetches full context of a ticket.
    - **Response**: `{ "issue_id": "...", "summary": "...", "description": "...", "comments": [...] }`

### 2. Context Engine (`/api/context`)
- **`POST /summarize`**
    - **Request**: `{ "ticket_id": "PROJ-123" }`
    - **Response**: `{ "ticket_id": "...", "intent_summary": "...", "context_used": {...} }`

### 3. Health Radar (`/api/health`)
- **`GET /status`**
    - **Description**: Global health status of tracked repos.
    - **Response**: `{ "status": "success", "data": [ { "repo": "...", "status": "Green", "health_score": 100, ... } ] }`

### 4. HITL Queue (`/api/queue`)
- **`GET /pending`**
    - **Description**: List of pending conflict reports.
- **`POST /resolve/{report_id}`**
    - **Description**: Mark report as resolved.

### 5. Safety Suite (`/api/safety`)
- **`POST /dry-run`**
    - **Request**: `{ "source_branch": "...", "target_branch": "...", "test_command": [...] }`
    - **Response**: `{ "merge_success": true, "tests_passed": true, "output": "..." }`
- **`POST /revert`**
    - **Description**: Emergency panic revert of the last merge.

### 6. Resolution Workspace (`/api/resolution`)
- **`GET /diff`**
    - **Request**: `?branch_a=...&branch_b=...&proposal_branch=...`
    - **Response**: `{ "branch_a_diff": "...", "branch_b_diff": "...", "proposal_diff": "...", "confidence_score": "85%" }`
- **`POST /update-proposal`**
    - **Description**: Apply developer tweaks to the proposed code.
- **`POST /merge`**
    - **Description**: Finalize the merge into SIT/UAT.

### 7. AI Command Center (`/api/commands`)
- **`POST /execute`**
    - **Request**: `{ "text": "Scan the health of the repos" }`
    - **Response**: `{ "status": "executing", "intent": "...", "message": "..." }`

### 8. Audit & Metrics (`/api/audit`)
- **`GET /metrics`**: Aggregated success/failure rates.
- **`GET /logs`**: Full historical audit trail.
