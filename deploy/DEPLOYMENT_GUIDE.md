# Deployment Guide

This document outlines deployment options for the Platform Capitalism Simulation.

---

## 🚀 Quick Deploy Options

### 1. Vercel (Demo/Development)

**Best for:** Quick demos, prototyping, sharing with collaborators

**Pros:**
- Zero config deployment
- Free tier available
- Automatic HTTPS
- Git integration

**Deploy:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production deploy
vercel --prod
```

**Configuration:** `vercel.json` in project root

---

### 2. AWS Lightsail (Research/Production)

**Best for:** Research deployments, long-running studies, data collection

**Pros:**
- Predictable pricing ($10-40/month)
- Container service with auto-scaling
- AWS ecosystem integration
- HIPAA-compliant options

**Deploy:**

#### Option A: Manual Deployment
```bash
cd deploy/lightsail

# 1. Build and push image
bash lightsail_build.sh

# 2. Deploy to Lightsail
bash deploy_lightsail.sh

# 3. Monitor logs
aws lightsail get-container-log \
  --service-name platform-capitalism \
  --region us-east-1
```

#### Option B: Terraform (Recommended for Research)
```bash
cd deploy/terraform

# 1. Set variables
export TF_VAR_image="ghcr.io/YOUR_USERNAME/platform-capitalism:latest"
export TF_VAR_secret_key="$(openssl rand -hex 32)"
export TF_VAR_db_url="sqlite:///./simulation.db"

# 2. Initialize Terraform
terraform init

# 3. Plan deployment
terraform plan

# 4. Apply
terraform apply

# 5. Get endpoint URL
terraform output public_url
```

**Configuration:**
- `deploy/lightsail/lightsail.yaml` - Container config
- `deploy/terraform/main.tf` - Infrastructure as code
- `deploy/terraform/variables.tf` - Deployment variables

---

## 📊 Deployment Comparison

| Feature | Vercel | Lightsail |
|---------|--------|-----------|
| **Cost** | Free tier | $10-40/mo |
| **Use Case** | Demo/Sharing | Research |
| **Setup Time** | 2 min | 10 min |
| **Scaling** | Auto | Manual |
| **Data Persistence** | In-memory | In-memory |
| **HIPAA Compliance** | No | Yes |
| **Custom Domain** | Yes | Yes |
| **SSL/HTTPS** | Auto | Auto |

---

## 🔒 Security Considerations

### Environment Variables

**Required:**
- `SECRET_KEY` - Generate with `openssl rand -hex 32`
- `DB_URL` - Database connection string

**Optional:**
- `ENVIRONMENT` - `development`, `demo`, or `production`
- `LOG_LEVEL` - `debug`, `info`, `warning`, `error`

### For Research Deployments (Lightsail):

1. **Enable HTTPS:**
   ```bash
   # Add custom domain in Lightsail console
   # Enable HTTPS certificate
   ```

2. **Database Backup:**
   ```bash
   # Automated backups via AWS Backup
   # See deploy/terraform/main.tf for config
   ```

3. **Access Control:**
   ```bash
   # Use AWS IAM for access management
   # Restrict container service to specific IPs if needed
   ```

---

## 🧪 Testing Deployments

### Health Check
```bash
curl https://your-deployment-url/health
```

### Run Simulation
```bash
# Start simulation
curl -X POST https://your-deployment-url/api/tick

# Check status
curl https://your-deployment-url/api/status
```

---

## 📦 Container Registry

Images are published to GitHub Container Registry:

```bash
# Build
docker build -t ghcr.io/YOUR_USERNAME/platform-capitalism:latest .

# Push
docker push ghcr.io/YOUR_USERNAME/platform-capitalism:latest
```

**Update image references in:**
- `deploy/lightsail/lightsail.yaml`
- `deploy/terraform/variables.tf` (via TF_VAR_image)
- `deploy/flyio/fly.toml`

---

## 🔧 Troubleshooting

### Vercel: "Module not found"
```bash
# Ensure requirements.txt is up to date
pip freeze > requirements.txt
```

### Lightsail: Container won't start
```bash
# Check logs
aws lightsail get-container-log \
  --service-name platform-capitalism \
  --region us-east-1

# Common issues:
# - Port mismatch (should be 8080)
# - Missing environment variables
# - Image not found
```

### Terraform: State lock
```bash
# Force unlock (use with caution)
terraform force-unlock LOCK_ID
```

---

## 📚 Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [AWS Lightsail Containers](https://aws.amazon.com/lightsail/features/containers/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

## 🆘 Support

For deployment issues:
1. Check logs first
2. Verify environment variables
3. Test locally with Docker
4. Open an issue on GitHub

---

**Recommended Setup:**
- **Demo:** Vercel (quick sharing)
- **Research:** Lightsail + Terraform (production-ready, HIPAA-compliant)
- **Development:** Local (`python main.py`)
