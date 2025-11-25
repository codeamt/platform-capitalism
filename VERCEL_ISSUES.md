# Vercel Deployment Issues & Solutions

## 🚨 Current Status: BLOCKED

Vercel's Python runtime has fundamental compatibility issues with ASGI applications (FastHTML/Starlette).

---

## Issues Encountered:

### 1. ✅ SOLVED: Empty requirements.txt
**Error:** `ModuleNotFoundError: No module named 'mangum'`
**Solution:** Copy `requirements.txt` to `api/requirements.txt`

### 2. ✅ SOLVED: Read-only filesystem
**Error:** `OSError: [Errno 30] Read-only file system: '.sesskey'`
**Solution:** Pass `key_fname=None` to `fast_app()` and provide secret key directly

### 3. ❌ BLOCKED: Vercel Python Runtime Incompatibility
**Error:** 
```
TypeError: issubclass() arg 1 must be a class
File "/var/task/vc__handler__python.py", line 32, in <module>
    if not issubclass(base, BaseHTTPRequestHandler):
```

**Root Cause:** Vercel's Python runtime (`vc__handler__python.py`) expects handlers to be subclasses of `BaseHTTPRequestHandler` (WSGI-style), but:
- FastHTML/Starlette are ASGI applications
- Mangum converts ASGI → Lambda/Vercel format
- Vercel's wrapper can't properly detect/wrap the Mangum handler

---

## Why Vercel Doesn't Work Well for FastHTML:

### Architecture Mismatch:

```
FastHTML (ASGI) → Mangum (ASGI→Lambda) → Vercel (expects WSGI)
                                              ↑
                                         Incompatible
```

### Vercel Python Limitations:

1. **WSGI-focused:** Designed for Flask/Django (WSGI), not modern ASGI frameworks
2. **Handler detection:** Expects `BaseHTTPRequestHandler` subclass
3. **Cold starts:** Serverless isn't ideal for stateful simulations
4. **10s timeout:** Free tier times out on complex initialization
5. **Read-only filesystem:** Can't persist state between requests

---

## ✅ Recommended Solution: Use AWS Lightsail

### Why Lightsail is Better:

| Feature | Vercel | AWS Lightsail |
|---------|--------|---------------|
| **Framework Support** | WSGI only | Full ASGI support ✅ |
| **State Management** | Ephemeral | Persistent ✅ |
| **Timeout** | 10s (free) | Unlimited ✅ |
| **Filesystem** | Read-only | Full access ✅ |
| **Cost** | Free (limited) | $20/mo |
| **Setup** | 2 min | 10 min |
| **Use Case** | Static sites | Full applications ✅ |

### Deploy to Lightsail:

```bash
# Already configured!
make quick-research

# Or step-by-step
cd deploy/terraform
terraform init
terraform apply
```

---

## Alternative: Static Landing Page on Vercel

If you still want to use Vercel, create a simple landing page:

### `api/landing.py`
```python
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Platform Capitalism Simulation</title>
            <style>
                body { font-family: system-ui; max-width: 800px; margin: 50px auto; padding: 20px; }
                .cta { background: #0070f3; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>🎮 Platform Capitalism Simulation</h1>
            <p>A research-driven simulation exploring creator wellbeing under different platform governance models.</p>
            
            <h2>🚀 Try the Full Simulation</h2>
            <a href="https://your-lightsail-url.com" class="cta">Launch Simulation →</a>
            
            <h2>📚 Learn More</h2>
            <a href="https://github.com/codeamt/platform-capitalism">View on GitHub</a>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode())
```

### Update `vercel.json`:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/api/landing"
    }
  ]
}
```

---

## Testing Different Handlers:

### Test Simple WSGI Handler:
```bash
# Update vercel.json to use /api/simple
vercel --prod
```

### Test Mangum Handler:
```bash
# Update vercel.json to use /api/test
vercel --prod
```

### Test Full App:
```bash
# Update vercel.json to use /api/index
vercel --prod
```

---

## Conclusion:

**Recommendation:** Deploy the full simulation to **AWS Lightsail** (already configured) and optionally use Vercel for a static landing page that links to it.

This gives you:
- ✅ Fast, free landing page on Vercel
- ✅ Full-featured simulation on Lightsail
- ✅ Best of both platforms

---

## Quick Deploy Commands:

```bash
# Deploy landing page to Vercel
vercel --prod

# Deploy full app to Lightsail
make quick-research

# View Lightsail logs
make lightsail-logs
```
