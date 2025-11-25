# Vercel Debugging Guide

## ✅ SOLVED: ModuleNotFoundError: No module named 'mangum'

**Root Cause:** Vercel wasn't installing dependencies because `requirements.txt` needs to be in the `api/` directory for serverless functions.

**Solution:** Copy `requirements.txt` to `api/requirements.txt`

```bash
cp requirements.txt api/requirements.txt
```

---

## Previous Error: 500 INTERNAL_SERVER_ERROR - FUNCTION_INVOCATION_FAILED

### Changes Made to Fix:

#### 1. Simplified `vercel.json`
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/api/index"
    }
  ]
}
```

**Why:** Modern Vercel uses `rewrites` instead of `builds`. The warning about unused build settings indicated the old config wasn't working properly.

#### 2. Added Logging to `api/index.py`
Now includes detailed error messages if the app fails to import.

#### 3. Created Test Handler: `api/test.py`
A minimal handler to verify Mangum + Vercel works:

```bash
# Test the simple handler first
curl https://your-app.vercel.app/api/test
```

---

## Debugging Steps:

### Step 1: Test Simple Handler
```bash
vercel --prod
# Visit: https://your-app.vercel.app/api/test
```

If this works, the issue is with importing `main.py`.

### Step 2: Check Vercel Logs
```bash
vercel logs --follow
```

Look for:
- Import errors
- Missing dependencies
- Path issues

### Step 3: Common Issues

#### Issue: Missing Dependencies
**Symptom:** `ModuleNotFoundError`
**Fix:** Add to `requirements.txt`

#### Issue: Import Fails
**Symptom:** Error in logs about importing `main`
**Fix:** Check if all simulation modules are included

#### Issue: Timeout
**Symptom:** Function timeout (10s on free tier)
**Fix:** The bootstrap might be too slow

---

## Current Setup:

### Files:
- ✅ `api/index.py` - Main handler with error handling
- ✅ `api/test.py` - Simple test handler
- ✅ `requirements.txt` - Dependencies
- ✅ `vercel.json` - Simplified config
- ✅ `.vercelignore` - Exclude unnecessary files

### Dependencies:
```
python-fasthtml>=0.12.0
monsterui>=1.0.32
starlette>=0.27.0
mangum>=0.17.0
```

---

## Next Steps:

### 1. Deploy and Test Simple Handler
```bash
vercel --prod
curl https://your-app.vercel.app/api/test
```

### 2. If Test Works, Check Main Handler
```bash
curl https://your-app.vercel.app/
```

### 3. Check Logs for Errors
```bash
vercel logs
```

### 4. If Import Fails

The issue is likely:
- **Bootstrap taking too long** - The simulation initialization might timeout
- **Missing dependencies** - Some package isn't in requirements.txt
- **Path issues** - Modules can't be found

**Potential Fix:** Lazy-load the simulation instead of bootstrapping on import:

```python
# In main.py, comment out:
# bootstrap_simulation(GLOBAL_ENVIRONMENT)

# And bootstrap on first request instead
```

---

## Alternative: Minimal Vercel Version

If the full app is too heavy for Vercel, create a minimal version:

```python
# api/minimal.py
from mangum import Mangum
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route

async def homepage(request):
    return HTMLResponse("""
        <h1>Platform Capitalism Simulation</h1>
        <p>Demo version - full app available on AWS Lightsail</p>
        <a href="https://github.com/codeamt/platform-capitalism">View on GitHub</a>
    """)

app = Starlette(routes=[Route("/", homepage)])
handler = Mangum(app, lifespan="off")
```

Then update `vercel.json`:
```json
{
  "rewrites": [{"source": "/(.*)", "destination": "/api/minimal"}]
}
```

---

## Recommendation:

Given the complexity of the simulation (agents, state machine, policy engine), **Vercel might not be ideal** for the full app. Consider:

1. **Vercel** → Static landing page + link to full app
2. **AWS Lightsail** → Full simulation (already configured)

This avoids serverless cold starts and timeout issues.
