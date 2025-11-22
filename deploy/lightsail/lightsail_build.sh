#!/bin/bash
set -e

SERVICE_NAME="platform-simulation"
IMAGE_NAME="${SERVICE_NAME}:latest"
AWS_REGION="us-east-1"

# Build container
docker build -t $IMAGE_NAME .

# Tag for Lightsail
LIGHTSAIL_IMAGE="${SERVICE_NAME}:lightsail"
docker tag $IMAGE_NAME $LIGHTSAIL_IMAGE

# Push to Lightsail Container Service
aws lightsail push-container-image \
  --service-name $SERVICE_NAME \
  --label app \
  --image $LIGHTSAIL_IMAGE \
  --region $AWS_REGION