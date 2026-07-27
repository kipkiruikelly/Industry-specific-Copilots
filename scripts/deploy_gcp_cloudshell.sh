#!/bin/bash
# MediCopilot Cloud Shell One-Click Deployment Script for Project: medicopilot-503723

set -e

PROJECT_ID="medicopilot-503723"
REGION="us-central1"

echo "=== 1. Setting GCP Project ==="
gcloud config set project $PROJECT_ID

echo "=== 2. Enabling Required GCP APIs ==="
gcloud services enable run.googleapis.com \
                       containerregistry.googleapis.com \
                       artifactregistry.googleapis.com \
                       cloudbuild.googleapis.com

echo "=== 3. Cloning MediCopilot Repository ==="
if [ -d "Industry-specific-Copilots" ]; then
  cd Industry-specific-Copilots
  git pull
else
  git clone https://github.com/kipkiruikelly/Industry-specific-Copilots.git
  cd Industry-specific-Copilots
fi

echo "=== 4. Building and Deploying FastAPI Backend ==="
gcloud builds submit --tag gcr.io/$PROJECT_ID/medicopilot-backend:latest .
gcloud run deploy medicopilot-backend \
  --image gcr.io/$PROJECT_ID/medicopilot-backend:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000

echo "=== 5. Building and Deploying Next.js Frontend ==="
cd frontend
gcloud builds submit --tag gcr.io/$PROJECT_ID/medicopilot-frontend:latest .
gcloud run deploy medicopilot-frontend \
  --image gcr.io/$PROJECT_ID/medicopilot-frontend:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 3000

echo "=== MediCopilot Deployment Complete! ==="
gcloud run services list
