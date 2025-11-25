# Deployment Options

Choose the right deployment strategy for your use case.

---

## 🎯 Recommended Deployments

### For Demos & Sharing
**→ Use Vercel**
- Zero config
- Free tier
- Instant deploys
- See: `../vercel.json`

### For Research & Production
**→ Use AWS Lightsail + Terraform**
- HIPAA-compliant
- Predictable pricing ($20/month recommended)
- Data persistence
- See: `terraform/` or `lightsail/`

---

## 📁 Directory Structure

```
deploy/
├── DEPLOYMENT_GUIDE.md      # Comprehensive deployment guide
├── vercel.json               # Vercel configuration (in project root)
├── lightsail/                # AWS Lightsail manual deployment
│   ├── README.md
│   ├── lightsail.yaml
│   ├── lightsail_build.sh
│   └── deploy_lightsail.sh
└── terraform/                # AWS Lightsail via Terraform (recommended)
    ├── README.md
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

---

## 🚀 Quick Commands

### Vercel (Demo)
```bash
# From project root
vercel
```

### Lightsail (Research)
```bash
# Manual
cd lightsail
bash lightsail_build.sh
bash deploy_lightsail.sh

# Terraform (recommended)
cd terraform
terraform init
terraform apply
```

---

## 📊 Comparison

| Platform | Use Case | Cost | Setup | HIPAA |
|----------|----------|------|------------|-------|
| **Vercel** | Demos/Sharing | Free | 2 min | ❌ |
| **Lightsail** | Research | $20/mo | 10 min | ✅ |

---

## 📚 Documentation

- **Full Guide:** [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md)
- **Lightsail:** [`lightsail/README.md`](lightsail/README.md)
- **Terraform:** [`terraform/README.md`](terraform/README.md)

---

## 🔒 Security Notes

### For Research Deployments:

1. **Generate secure keys:**
   ```bash
   openssl rand -hex 32
   ```

2. **Enable HTTPS** (automatic with Lightsail)

3. **Set up data backups** (see Terraform config)

4. **Restrict access** via AWS IAM

---

## 🆘 Need Help?

1. Check [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md)
2. Review logs (see platform-specific README)
3. Open an issue on GitHub

---

**Updated:** November 2024  
**Maintained by:** Platform Capitalism Research Team
