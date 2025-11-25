# AWS Lightsail Deployment

Deploy the Platform Capitalism Simulation to AWS Lightsail for research and production use.

## Quick Start

### 1. Build & Push Image

```bash
bash lightsail_build.sh
```

This builds the Docker image and pushes to GitHub Container Registry.

### 2. Deploy to Lightsail

```bash
bash deploy_lightsail.sh
```

This creates the Lightsail container service and deploys your app.

### 3. Monitor Logs

```bash
aws lightsail get-container-log \
  --service-name platform-capitalism \
  --region us-east-1
```

### 4. Access Your App

The deployment script will print the public endpoint URL.

---

## Configuration

### Environment Variables

The simulation uses in-memory state (no database required).

Set in `lightsail.env`:

```bash
ENVIRONMENT=production
LOG_LEVEL=info
PORT=8080
```

Optional for research deployments:
```bash
ENABLE_DATA_EXPORT=true
S3_BUCKET=platform-capitalism-research-data
```

### Container Settings

Edit `lightsail.yaml` to configure:
- **Region:** `us-east-1`, `us-west-2`, `eu-west-1`, etc.
- **Image:** Update with your GitHub username
- **Environment:** Add research-specific variables

---

## Research Deployment

For long-running research studies with data collection:

### 1. Enable Data Export

Uncomment in `lightsail.yaml`:
```yaml
ENABLE_DATA_EXPORT: "true"
S3_BUCKET: "platform-capitalism-research-data"
```

### 2. Create S3 Bucket

```bash
aws s3 mb s3://platform-capitalism-research-data --region us-east-1
```

### 3. Set Up IAM Permissions

The container needs S3 write permissions. See Terraform config for automated setup.

---

## Pricing

AWS Lightsail container pricing (as of 2024):

| Power | vCPU | RAM | Price/month |
|-------|------|-----|-------------|
| micro | 0.25 | 512 MB | $7 |
| small | 0.5 | 1 GB | $10 |
| medium | 1.0 | 2 GB | $20 |
| large | 2.0 | 4 GB | $40 |

**Recommended for research:** Medium ($20/month)

---

## Troubleshooting

### Container won't start

```bash
# Check logs
aws lightsail get-container-log \
  --service-name platform-capitalism \
  --region us-east-1

# Common issues:
# - Missing environment variables
# - Image not found (check GHCR permissions)
# - Port mismatch (should be 8080)
```

### Update deployment

```bash
# Rebuild and redeploy
bash lightsail_build.sh
bash deploy_lightsail.sh
```

---

## Alternative: Terraform

For infrastructure-as-code, use Terraform instead:

```bash
cd ../terraform
terraform init
terraform apply
```

See `../terraform/README.md` for details.
