# 🚀 OpenClaw Dashboard - Project Master Plan

This document serves as the absolute source of truth for the development of the OpenClaw Dashboard. No feature is considered complete until it is implemented, tested, and verified.

## 🎯 Project Goal
Build a high-level AI-Assisted Conflict Resolution Workflow dashboard that integrates Git, Jira, and AI to manage complex code merges.

---

## 🏗️ Implementation Phases

### Phase 1: The Context Engine (Option A) - **CURRENT**
*Goal: Link code changes to business intent.*
- [ ] **Backend: Jira Integration Layer**
    - [ ] Route: `GET /jira/ticket/{ticket_id}`
    - [ ] Service: Fetch User Stories, Acceptance Criteria, and comments.
    - [ ] Test: `tests/test_jira_integration.py`
- [ ] **Backend: Intent Translation Service**
    - [ ] Logic: AI-driven summary of "Why this change happened" based on Jira context.
    - [ ] Route: `POST /context/summarize`
    - [ ] Test: `tests/test_intent_summary.py`
- [ ] **Backend: Git-to-Jira Linker**
    - [ ] Logic: Parse commit messages to find linked Jira tickets.
    - [ ] Test: `tests/test_git_linker.py`

### Phase 2: The Conflict Radar (Option B)
*Goal: Global visibility of repo health.*
- [ ] **Backend: Repo Health Scanner**
    - [ ] Logic: Scan multiple repos for overlapping branches.
    - [ ] Logic: Generate "Traffic Light" status (Green/Yellow/Red).
    - [ ] Route: `GET /health/status`
    - [ ] Test: `tests/test_health_scanner.py`
- [ ] **Backend: HITL (Human-in-the-Loop) Queue**
    - [ ] Logic: Priority queue for AI-generated conflict reports.
    - [ ] Route: `GET /queue/pending`
    - [ ] Test: `tests/test_hitl_queue.py`
- [ ] **Backend: Active Agent Tracker**
    - [ ] Logic: Real-time status of OpenClaw's background tasks.
    - [ ] Route: `GET /agent/status`
    - [ ] Test: `tests/test_agent_status.py`

### Phase 3: The Safety Suite (Option C)
*Goal: Prevent production breaks.*
- [ ] **Backend: Dry-Run Sandbox**
    - [ ] Logic: Create temporary hidden branches for test merges.
    - [ ] Logic: Trigger automated build/compile tests.
    - [ ] Route: `POST /safety/dry-run`
    - [ ] Test: `tests/test_dry_run.py`
- [ ] **Backend: The Panic Button**
    - [ ] Logic: One-click `git revert` for the last AI merge.
    - [ ] Route: `POST /safety/revert`
    - [ ] Test: `tests/test_panic_button.py`
- [ ] **Backend: Auto-Merge Rules Engine**
    - [ ] Logic: Configurable rules for whitespace vs. logical conflicts.
    - [ ] Test: `tests/test_rules_engine.py`

### Phase 4: The Resolution Workspace (Core Feature)
*Goal: Interactive conflict solving.*
- [ ] **Backend: Smart 3-Way Diff Generator**
    - [ ] Logic: Generate diffs for Branch A, Branch B, and AI Proposal.
    - [ ] Route: `GET /resolution/diff`
    - [ ] Test: `tests/test_diff_generator.py`
- [ ] **Backend: Proposed Code Editor**
    - [ ] Logic: Apply developer tweaks to AI proposals.
    - [ ] Route: `POST /resolution/update-proposal`
    - [ ] Test: `tests/test_proposal_editor.py`
- [ ] **Backend: Final Merge Execution**
    - [ ] Logic: Secure merge to SIT/UAT branches.
    - [ ] Route: `POST /resolution/merge`
    - [ ] Test: `tests/test_merge_execution.py`

### Phase 5: The High-Level Frontend
*Goal: Professional UI implementation (Next.js/React).*
- [ ] **The Command Center** (Overview & Triage)
- [ ] **The AI Communication Console** (Chat & Notification Hub)
- [ ] **The Resolution Workspace** (3-Way Diff & Edit)
- [ ] **The Context Engine Panel** (Jira Integration View)
- [ ] **Safety Controls** (Panic Button & Sandbox UI)

---

## 🧪 Testing & Verification Standard
For every single feature:
1. **API Test File:** A dedicated Python test file ensuring the route returns the correct status and data.
2. **Verification Script:** A separate script that simulates a real-world scenario (e.g., "Create a conflict $\rightarrow$ Run AI Fix $\rightarrow$ Verify result").
3. **Documentation:** Updated `docs/` folder explaining the feature's logic.
