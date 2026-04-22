from fastapi import FastAPI
from app.api.routes import jira, context, health, queue, safety, resolution
from app.core.database import init_db

app = FastAPI(
    title="OpenClaw Dashboard API",
    description="Backend for the AI-Assisted Conflict Resolution Workflow",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    init_db()

# Include Routers
app.include_router(jira.router, prefix="/api/jira", tags=["Jira"])
app.include_router(context.router, prefix="/api/context", tags=["Context"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(queue.router, prefix="/api/queue", tags=["Queue"])
app.include_router(safety.router, prefix="/api/safety", tags=["Safety"])
app.include_router(resolution.router, prefix="/api/resolution", tags=["Resolution"])

@app.get("/")
async def root():
    return {"message": "Welcome to the OpenClaw Dashboard API", "status": "online"}
