**# Usage**
**# -----**
**# 1. Configure variables:**
**#    export TF_VAR_image="ghcr.io/codeamt/platform-simulation:latest"**
**#    export TF_VAR_secret_key="your_generated_secret"**
**#    export TF_VAR_db_url="sqlite:///./simulation.db"**
**#**
**# 2. Deploy infra:**
**#    terraform init**
**#    terraform apply**
**#**
**# 3. After apply completes, Terraform outputs the public URL.**
**#    Access your app at that endpoint.**
