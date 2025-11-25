"""
Simple test handler to verify Vercel is working
"""
from mangum import Mangum
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def homepage(request):
    return JSONResponse({
        "status": "ok",
        "message": "Vercel is working!",
        "path": str(request.url.path)
    })

app = Starlette(routes=[
    Route("/", homepage),
    Route("/{path:path}", homepage),
])

handler = Mangum(app, lifespan="off")
