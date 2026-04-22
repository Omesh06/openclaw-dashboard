from fastapi import FastAPI
from app.api.routes import jira, context, health, queue, safety

app = FastAPI(
    title="OpenClaw Dashboard API",
    description="Backend for the AI-Assisted Conflict Resolution Workflow",
    version="0.1.0"
)

# Include Routers
app.include_router(jira.router, prefix="/api/jira", tags=["Jira"])
app.include_router(context.router, prefix="/api/context", tags=["Context"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(queue.router, prefix="/api/queue", tags=["Queue"])
app.include_router(safety.router, prefix="/api/safety", tags=["Safety"])

@app.get("/")
async def root():
    return {"message": "Welcome to the OpenClaw Dashboard API", "status": "online"}
