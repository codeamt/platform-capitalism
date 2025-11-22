#!/bin/bash
# Production deployment script

echo "🚀 Starting Platform Capitalism Simulator deployment"

# Validate deployment config
python -c "from app.deploy import config; assert config.validate(), 'Invalid deployment configuration'"

# Fly.io deployment
if [[ "$1" == "fly" ]]; then
    echo "🛫 Deploying to Fly.io"
    flyctl deploy --remote-only \\
        --vm-memory ${MEMORY:-1024} \\
        --vm-cpus ${CPUS:-1} \\
        --region ${REGION:-ord}

elif [[ "$1" == "docker" ]]; then
    echo "🐳 Building Docker image"
    docker build -t platform-sim:latest . \\
        --build-arg PYTHON_VERSION=3.11-slim \\
        --build-arg APP_ENV=production

    # Add your registry push commands here
else
    echo "❌ Invalid deployment target"
    exit 1
fi

echo "✅ Deployment completed successfully"