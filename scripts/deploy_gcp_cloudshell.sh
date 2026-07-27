#!/bin/bash
# MediCopilot Direct Docker Build & Deploy Script for GCP Cloud Shell

set -e

PROJECT_ID="medicopilot-503723"
REGION="us-central1"

echo "=== 1. Setting GCP Project ==="
gcloud config set project $PROJECT_ID

echo "=== 2. Configuring Local Docker Authentication ==="
gcloud auth configure-docker --quiet

echo "=== 3. Building and Pushing FastAPI Backend Image ==="
docker build -t gcr.io/$PROJECT_ID/medicopilot-backend:latest .
docker push gcr.io/$PROJECT_ID/medicopilot-backend:latest

echo "=== 4. Deploying Backend to Cloud Run ==="
gcloud run deploy medicopilot-backend \
  --image gcr.io/$PROJECT_ID/medicopilot-backend:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000

echo "=== 5. Building and Pushing Next.js Frontend Image ==="
cd frontend
docker build -t gcr.io/$PROJECT_ID/medicopilot-frontend:latest .
docker push gcr.io/$PROJECT_ID/medicopilot-frontend:latest

echo "=== 6. Deploying Frontend to Cloud Run ==="
gcloud run deploy medicopilot-frontend \
  --image gcr.io/$PROJECT_ID/medicopilot-frontend:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 3000

echo "=== MediCopilot Deployment Complete! ==="
gcloud run services list
