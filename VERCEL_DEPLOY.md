# Vercel Deployment Guide

## 🚀 Quick Deploy

```bash
# Deploy to Vercel
vercel --prod
```

## 🔧 What Was Fixed

### Issue: "This Serverless Function has crashed"

**Root Causes:**
1. Missing ASGI handler for Vercel
2. Empty `requirements.txt` (Vercel couldn't install dependencies)
3. Incorrect entry point in `vercel.json`

**Solutions:**
1. ✅ Created `api/index.py` - Vercel serverless function entry point
2. ✅ Populated `requirements.txt` with FastHTML dependencies
3. ✅ Updated `vercel.json` to point to `api/index.py`
4. ✅ Added `.vercelignore` to reduce deployment size

## 📁 New Files

### `api/index.py`
```python
# Vercel serverless function entry point
from main import app
handler = app
```

### `requirements.txt`
```
python-fasthtml>=0.12.0
monsterui>=1.0.32
```

### `.vercelignore`
Excludes unnecessary files from deployment (tests, docs, deploy configs)

## 🧪 Testing

### Local Test
```bash
# Run locally first
make dev

# Test at http://localhost:5001
```

### Deploy Preview
```bash
# Deploy preview (non-production)
vercel

# Get preview URL
# Test all routes work
```

### Deploy Production
```bash
# Deploy to production
vercel --prod

# Your app will be at:
# https://platform-capitalism.vercel.app
```

## 🔍 Debugging Vercel Deployments

### View Logs
```bash
# View deployment logs
vercel logs

# View function logs
vercel logs --follow
```

### Common Issues

#### 1. Import Errors
**Symptom:** Module not found
**Fix:** Add missing package to `requirements.txt`

#### 2. Timeout
**Symptom:** Function timeout (10s limit on free tier)
**Fix:** Optimize slow operations or upgrade to Pro

#### 3. Memory Limit
**Symptom:** Out of memory error
**Fix:** Reduce in-memory state or upgrade plan

#### 4. Cold Start
**Symptom:** First request is slow
**Fix:** Expected behavior - subsequent requests are fast

## 📊 Vercel Limits (Free Tier)

- **Function Duration:** 10 seconds
- **Function Memory:** 1024 MB
- **Deployment Size:** 100 MB
- **Bandwidth:** 100 GB/month
- **Invocations:** Unlimited

## ✅ Deployment Checklist

- [x] `api/index.py` exists
- [x] `requirements.txt` has dependencies
- [x] `vercel.json` configured
- [x] `.vercelignore` excludes unnecessary files
- [x] Tested locally with `make dev`
- [ ] Deploy preview: `vercel`
- [ ] Test preview URL
- [ ] Deploy production: `vercel --prod`
- [ ] Share production URL with collaborators

## 🆘 Still Having Issues?

1. **Check Vercel dashboard** - View detailed error logs
2. **Test locally** - Ensure app runs with `make dev`
3. **Verify dependencies** - All imports in `requirements.txt`
4. **Check function logs** - `vercel logs --follow`

## 📚 Resources

- [Vercel Python Runtime](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastHTML Documentation](https://fastht.ml/)
- [Vercel CLI Reference](https://vercel.com/docs/cli)
