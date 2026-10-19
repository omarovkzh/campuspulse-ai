#!/usr/bin/env bash
# Usage: PROJECT_ID=my-project REGION=us-central1 bash scripts/setup_gcp.sh
set -euo pipefail
: "${PROJECT_ID:?set PROJECT_ID}"
REGION="${REGION:-us-central1}"

gcloud config set project "$PROJECT_ID"
gcloud services enable aiplatform.googleapis.com storage.googleapis.com \
  run.googleapis.com cloudbuild.googleapis.com
gcloud storage buckets create "gs://${PROJECT_ID}-staging" --location="$REGION" || true
gcloud auth application-default login
echo "Add to .env: STAGING_BUCKET=gs://${PROJECT_ID}-staging"
