#!/bin/bash
# MediCopilot Cloud Build direct deployment script

set -e

PROJECT_ID="medicopilot-503723"
REGION="us-central1"
SERVICE_BACKEND="medicopilot-backend"
SERVICE_FRONTEND="medicopilot-frontend"

echo "=== 1. Setting GCP Project ==="
gcloud config set project $PROJECT_ID

echo "=== 2. Deploying FastAPI Backend via Cloud Run Source Deploy ==="
gcloud run deploy $SERVICE_BACKEND \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000 \
  --set-env-vars VECTOR_PROVIDER=in_memory,ENVIRONMENT=production

echo "=== 3. Deploying Next.js Frontend via Cloud Run Source Deploy ==="
cd frontend
gcloud run deploy $SERVICE_FRONTEND \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 3000

echo "=== MediCopilot Deployment Complete! ==="
gcloud run services list
