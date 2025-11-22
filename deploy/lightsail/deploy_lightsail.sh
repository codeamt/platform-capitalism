#!/bin/bash
set -e

SERVICE_NAME="platform-simulation"
AWS_REGION="us-east-1"

aws lightsail create-container-service-deployment \
  --service-name $SERVICE_NAME \
  --containers file://lightsail.yaml \
  --public-endpoint '{"containerName":"app","containerPort":8080,"healthCheck":{"path":"/health","intervalSeconds":10,"timeoutSeconds":5}}' \
  --region $AWS_REGION

echo "Deployment initiated to Lightsail Container Service: $SERVICE_NAME"