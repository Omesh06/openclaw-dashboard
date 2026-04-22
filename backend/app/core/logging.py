import logging
import sys
from fastapi import Request
from fastapi.responses import JSONResponse

# Configure Professional Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("openclaw_dashboard.log")
    ]
)

logger = logging.getLogger("openclaw_dashboard")

async def global_exception_handler(request: Request, exc: Exception):
    """
    Global handler to catch all unhandled exceptions and return a 
    consistent, professional JSON response.
    """
    logger.error(f"Unhandled Exception: {str(exc)} | Path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal server error occurred. Our engineers have been notified.",
            "detail": str(exc) if os.getenv("ENV") == "development" else None
        }
    )
