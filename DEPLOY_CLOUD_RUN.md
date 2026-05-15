Cloud Run deployment guide

Prerequisites
- Google Cloud project
- `gcloud` installed locally
- Billing enabled and Cloud Run API enabled

Quick manual deploy (local):

1. Build and push image:

```bash
gcloud auth configure-docker
IMAGE=gcr.io/$(gcloud config get-value project)/sistec-chatbot:latest
docker build -t $IMAGE .
docker push $IMAGE
```

2. Deploy to Cloud Run:

```bash
gcloud run deploy sistec-chatbot \
  --image $IMAGE \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory=2Gi
```

CI/CD via GitHub Actions

This repo includes `.github/workflows/cloud-run-deploy.yml` which:
- Builds the Docker image
- Pushes it to Google Container Registry
- Deploys it to Cloud Run

Required GitHub secrets:
- `GCP_PROJECT` - your GCP project ID
- `GCP_SA_KEY` - JSON service account key (as plaintext secret)
- `CLOUD_RUN_SERVICE` - name of the Cloud Run service to deploy (e.g. `sistec-chatbot`)
- `GCP_REGION` - Cloud Run region (e.g. `us-central1`)

Service account permissions
- Grant the service account these roles:
  - `roles/run.admin`
  - `roles/storage.admin` (for pushing images)
  - `roles/iam.serviceAccountUser`

Notes
- This approach packages the full application (including heavy deps) into a container, so Vercel size limits no longer apply.
- If you prefer Artifact Registry instead of GCR, update the workflow image path accordingly.
