"""
Vercel serverless function entry point.
Uses Mangum to adapt ASGI app (FastHTML/Starlette) to Vercel's serverless environment.
"""
import sys
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set environment for Vercel
os.environ.setdefault("ENVIRONMENT", "production")
os.environ.setdefault("LOG_LEVEL", "info")

# Import dependencies
from mangum import Mangum
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# Try to import the FastHTML app
try:
    logger.info("Attempting to import main app...")
    # Use Vercel-optimized version that delays bootstrap
    from main_vercel import app
    logger.info(f"Successfully imported app: {type(app)}")
    
    # Mangum adapts ASGI apps to work with AWS Lambda/Vercel
    handler = Mangum(app, lifespan="off")
    logger.info("Handler created successfully")
    
except Exception as e:
    # If import fails, create a minimal error handler
    import traceback
    error_msg = str(e)
    error_trace = traceback.format_exc()
    
    logger.error(f"Failed to import app: {error_msg}")
    logger.error(f"Traceback: {error_trace}")
    
    async def error_handler(request):
        return JSONResponse({
            "error": "Application failed to load",
            "details": error_msg,
            "traceback": error_trace,
            "path": str(request.url.path)
        }, status_code=500)
    
    error_app = Starlette(routes=[Route("/{path:path}", error_handler)])
    handler = Mangum(error_app, lifespan="off")
