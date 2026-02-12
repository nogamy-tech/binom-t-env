# Deployment Guide

This document explains how to deploy the **Cloud Function (Gen 2)** for this repository to Google Cloud.

---

## Deployment Command

Run the following command from the project root (all in one line):

```bash
gcloud functions deploy cf-nogamy-shomersaf-document-start-job --gen2   --project=dgt-gcp-cgov-d-datapro   --region=me-west1   --runtime=python312   --source=.   --entry-point=flask_app   --trigger-http   --ingress-settings=internal-only   --no-allow-unauthenticated   --vpc-connector=projects/dgt-gcp-cgov-net-office-0/locations/me-west1/connectors/binom-sha-d-serverless   --egress-settings=all  --service-account nogamy-sa@dgt-gcp-cgov-d-datapro.iam.gserviceaccount.com
```

```bash
gcloud functions add-iam-policy-binding cf-nogamy-shomersaf-document-start-job --project=dgt-gcp-cgov-d-datapro   --region=me-west1   --gen2   --member="allUsers"   --role="roles/cloudfunctions.invoker"
```

---

## Testing the Deployment

After successful deployment, you can test the function using the following curl command from VM:

```bash
curl -X POST "http://binom.dev.cgov.dgt.gcp.internal/shomer-saf/StartJob/QueueThresholdCheck" \
  -H "x-client-id: 123" \
  -H "x-scope: 321" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "ClientRequestId": "text",
    "Document": "pdfbase64",
    "Queries": [
        {
            "model": "text",
            "query": "does the name of the person is danny?"
        },
        {
            "model": "text",
            "query": "does the age mentioned is 30?"
        },
        {
            "model": "text",
            "query": "is the person mentioned lives in the US?"
        }
    ]
}'
```

curl -X POST "http://binom.dev.cgov.dgt.gcp.internal/shomer-saf/StartJob/QueueThresholdCheck"
  -H "x-client-id: 1"
  -H "x-scope: 2"
  -H "Authorization: Bearer $(gcloud auth print-access-token)"
  -H "Content-Type: application/json"
  -d '{
    "ClientRequestId": "123456789-304050_0001_20250311_1240",
    "Document": "base64encodeddocument==",
    "Queries": [
      {"query": "is the document signed", "model": "image"},
      {"query": "is it an engineering degree", "model": "text"}
    ]
  }'

### Expected Response

```json
{
  "RequestErrorCode": 202,
  "RequestErrorMessage": "OK"
}
```

---

## Notes

- **`--gen2`**: Deploys to Cloud Functions Gen 2 (runs on Cloud Run).
- **`--source=.`**: Uses the current directory; `.gcloudignore` controls which files are excluded.
- **`--entry-point=flask_app`**: Must match your Python entrypoint function.
- **Ingress/Egress**: Restricted to internal traffic; all egress goes through the given VPC connector.
- **Scaling/Resources**: Max 100 instances, 512MiB RAM, 1 vCPU, and 5-minute timeout.

---

## `.gcloudignore`

# Useful gcloud Config

Enable `.gcloudignore` support if not already enabled:

```bash
gcloud config set gcloudignore/enabled true
gcloud config list
```

Make sure `requirements.txt` is not excluded. Add this to your `.gcloudignore`:

```
# Ignore common local/dev artifacts
.git
.gitignore
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
*.ipynb

# Ensure requirements.txt is deployed
!requirements.txt


```
