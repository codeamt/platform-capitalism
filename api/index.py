"""
Vercel serverless function entry point.
This file is required for Vercel to properly route requests to the FastHTML app.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the FastHTML app
from main import app

# Vercel expects the ASGI app to be named 'app' or exposed as a handler
# FastHTML's app is already ASGI-compatible (Starlette-based)
handler = app
