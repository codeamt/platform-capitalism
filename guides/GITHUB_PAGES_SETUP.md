# GitHub Pages Setup Guide

## 🚀 Enable GitHub Pages

### Step 1: Push Your Changes

First, commit and push all the documentation files:

```bash
git add .
git commit -m "Add complete MkDocs documentation and GitHub Pages setup"
git push
```

### Step 2: Enable GitHub Pages in Repository Settings

1. Go to your repository on GitHub: `https://github.com/codeamt/platform-capitalism`
2. Click **Settings** (top right)
3. Scroll down to **Pages** (left sidebar)
4. Under **Source**, select:
   - **Source:** Deploy from a branch
   - **Branch:** `gh-pages` (this will be created by the workflow)
   - **Folder:** `/ (root)`
5. Click **Save**

### Step 3: Trigger the Workflow

The workflow will run automatically when you push to `main`, but you can also trigger it manually:

1. Go to **Actions** tab
2. Click **Deploy Docs** workflow
3. Click **Run workflow** → **Run workflow**

### Step 4: Wait for Deployment

- The workflow takes ~1-2 minutes to run
- Once complete, your docs will be available at: `https://codeamt.github.io/platform-capitalism`

---

## 🔍 Troubleshooting

### "404 Page Not Found"

**Cause:** GitHub Pages not enabled or `gh-pages` branch doesn't exist yet

**Fix:**
1. Check that the workflow ran successfully (Actions tab)
2. Verify `gh-pages` branch exists (Branches dropdown)
3. Enable GitHub Pages in Settings → Pages

### "Workflow Failed"

**Cause:** Missing dependencies or build errors

**Fix:**
1. Check workflow logs in Actions tab
2. Verify `mkdocs.yml` is valid
3. Ensure all referenced files exist

### "Permission Denied"

**Cause:** Workflow doesn't have permission to push to `gh-pages`

**Fix:**
1. Go to Settings → Actions → General
2. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
3. Save changes
4. Re-run the workflow

---

## ✅ Verification

Once deployed, verify your docs:

1. **Homepage:** `https://codeamt.github.io/platform-capitalism`
2. **Architecture:** `https://codeamt.github.io/platform-capitalism/architecture/overview/`
3. **API Reference:** `https://codeamt.github.io/platform-capitalism/api/agents/`

---

## 🔄 Automatic Updates

After initial setup, docs will automatically update whenever you:

1. Push to `main` branch
2. Modify any files in `docs/` directory
3. Update `mkdocs.yml`

The workflow runs automatically - no manual intervention needed! 🎉

---

## 📊 Current Setup

- **Workflow:** `.github/workflows/docs.yml`
- **Config:** `mkdocs.yml`
- **Source:** `docs/` directory
- **Theme:** Material for MkDocs
- **Plugins:** Search, Mermaid diagrams
- **URL:** `https://codeamt.github.io/platform-capitalism`

---

## 🆘 Still Not Working?

Check these common issues:

1. **Repository is private** - GitHub Pages requires public repos (or GitHub Pro)
2. **Branch protection** - `gh-pages` branch might be protected
3. **Workflow permissions** - Need write access to repository
4. **First deployment** - Can take 5-10 minutes for first deploy

If issues persist, check the Actions tab for detailed error logs.
