"""
Vercel serverless function entry point.
Uses Mangum to adapt ASGI app (FastHTML/Starlette) to Vercel's serverless environment.
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set environment for Vercel
os.environ.setdefault("ENVIRONMENT", "production")
os.environ.setdefault("LOG_LEVEL", "info")

# Import the FastHTML app and wrap with Mangum for Vercel
try:
    from main import app
    from mangum import Mangum
    
    # Mangum adapts ASGI apps to work with AWS Lambda/Vercel
    handler = Mangum(app, lifespan="off")
    
except Exception as e:
    # If import fails, create a minimal error handler
    import traceback
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route
    from mangum import Mangum
    
    async def error_handler(request):
        return JSONResponse({
            "error": "Application failed to load",
            "details": str(e),
            "traceback": traceback.format_exc()
        }, status_code=500)
    
    error_app = Starlette(routes=[Route("/{path:path}", error_handler)])
    handler = Mangum(error_app, lifespan="off")
