# Terraform Deployment for AWS Lightsail

Deploy Platform Capitalism Simulation to AWS Lightsail using Infrastructure as Code.

## Quick Start

### 1. Configure Variables

```bash
# Set your GitHub username
export TF_VAR_image="ghcr.io/YOUR_USERNAME/platform-capitalism:latest"

# Optional: Change environment
export TF_VAR_environment="production"  # or "staging"
```

### 2. Initialize Terraform

```bash
terraform init
```

### 3. Plan Deployment

```bash
terraform plan
```

### 4. Deploy

```bash
terraform apply
```

### 5. Get Public URL

```bash
terraform output public_url
```

Access your app at the output URL!

---

## Configuration

### Variables

Edit `variables.tf` or set via environment:

- **`image`** - Container image (default: `ghcr.io/YOUR_USERNAME/platform-capitalism:latest`)
- **`service_name`** - Lightsail service name (default: `platform-capitalism`)
- **`region`** - AWS region (default: `us-east-1`)
- **`power`** - Container size: `micro`, `small`, `medium`, `large`, `xlarge` (default: `medium`)
- **`scale`** - Number of instances 1-20 (default: `1`)
- **`environment`** - Deployment environment (default: `production`)

### Recommended for Research

```bash
export TF_VAR_power="medium"   # 1 vCPU, 2GB RAM - $20/month
export TF_VAR_scale="1"        # Single instance
```

---

## Outputs

After deployment, Terraform provides:

- **`public_url`** - Public endpoint URL
- **`service_name`** - Lightsail service name
- **`region`** - Deployment region

---

## Updating Deployment

```bash
# Pull latest code
git pull

# Rebuild and push image
docker build -t ghcr.io/YOUR_USERNAME/platform-capitalism:latest .
docker push ghcr.io/YOUR_USERNAME/platform-capitalism:latest

# Redeploy
terraform apply
```

---

## Destroying Infrastructure

```bash
terraform destroy
```

**Warning:** This will delete all resources and cannot be undone.

---

## Troubleshooting

### State Lock Issues

```bash
# If state is locked
terraform force-unlock LOCK_ID
```

### Container Won't Start

```bash
# Check Lightsail console logs
# Or use AWS CLI:
aws lightsail get-container-log \
  --service-name platform-capitalism \
  --region us-east-1
```

---

## Cost Estimate

| Power | vCPU | RAM | Monthly Cost |
|-------|------|-----|--------------|
| micro | 0.25 | 512 MB | $7 |
| small | 0.5 | 1 GB | $10 |
| **medium** | **1.0** | **2 GB** | **$20** ⭐ |
| large | 2.0 | 4 GB | $40 |

**Recommended:** Medium for research deployments

---

## Alternative: Makefile

Use the project Makefile for easier commands:

```bash
# From project root
make terraform-init
make terraform-plan
make terraform-apply
```
