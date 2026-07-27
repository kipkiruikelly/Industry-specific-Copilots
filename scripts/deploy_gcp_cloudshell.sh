#!/bin/bash
# MediCopilot GCP Deployment Script using Google Artifact Registry (pkg.dev)

set -e

PROJECT_ID="medicopilot-503723"
REGION="us-central1"
REPO_NAME="medicopilot-repo"

echo "=== 1. Setting GCP Project ==="
gcloud config set project $PROJECT_ID

echo "=== 2. Creating Artifact Registry Repository ==="
gcloud artifacts repositories create $REPO_NAME \
  --repository-format=docker \
  --location=$REGION \
  --description="MediCopilot Enterprise Docker Repository" || true

echo "=== 3. Authenticating Docker to Artifact Registry ==="
gcloud auth configure-docker $REGION-docker.pkg.dev --quiet

BACKEND_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/medicopilot-backend:latest"
FRONTEND_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/medicopilot-frontend:latest"

echo "=== 4. Pushing FastAPI Backend Image ==="
docker tag gcr.io/$PROJECT_ID/medicopilot-backend:latest $BACKEND_IMAGE
docker push $BACKEND_IMAGE

echo "=== 5. Deploying Backend to Cloud Run ==="
gcloud run deploy medicopilot-backend \
  --image $BACKEND_IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000

echo "=== 6. Building and Pushing Next.js Frontend Image ==="
cd frontend
docker build -t $FRONTEND_IMAGE .
docker push $FRONTEND_IMAGE

echo "=== 7. Deploying Frontend to Cloud Run ==="
gcloud run deploy medicopilot-frontend \
  --image $FRONTEND_IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 3000

echo "=== MediCopilot Deployment Complete! ==="
gcloud run services list
