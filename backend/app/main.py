from fastapi import FastAPI
from app.api.routes import jira, context, health, queue, safety, resolution, audit, commands, chat
from app.core.database import init_db
from app.core.logging import global_exception_handler

app = FastAPI(
    title="OpenClaw Dashboard API",
    description="Backend for the AI-Assisted Conflict Resolution Workflow",
    version="1.0.0"
)

# Register Global Exception Handler
app.add_exception_handler(Exception, global_exception_handler)

@app.on_event("startup")
async def startup_event():
    init_db()
    # Start background health scanner
    from app.api.routes.health import cache_service
    cache_service.start_background_worker(interval=300)
    cache_service.update_cache() # Initial sync


# Include Routers
app.include_router(jira.router, prefix="/api/jira", tags=["Jira"])
app.include_router(context.router, prefix="/api/context", tags=["Context"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(queue.router, prefix="/api/queue", tags=["Queue"])
app.include_router(safety.router, prefix="/api/safety", tags=["Safety"])
app.include_router(resolution.router, prefix="/api/resolution", tags=["Resolution"])
app.include_router(audit.router, prefix="/api/audit", tags=["Audit"])
app.include_router(commands.router, prefix="/api/commands", tags=["Commands"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to the OpenClaw Dashboard API", "status": "online"}
