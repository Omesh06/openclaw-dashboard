from fastapi import FastAPI
from app.api.routes import jira, context

app = FastAPI(
    title="OpenClaw Dashboard API",
    description="Backend for the AI-Assisted Conflict Resolution Workflow",
    version="0.1.0"
)

# Include Routers
app.include_router(jira.router, prefix="/api/jira", tags=["Jira"])
app.include_router(context.router, prefix="/api/context", tags=["Context"])

@app.get("/")
async def root():
    return {"message": "Welcome to the OpenClaw Dashboard API", "status": "online"}
