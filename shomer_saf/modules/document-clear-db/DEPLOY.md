# Deployment Guide

This document explains how to deploy the **Cloud Function (Gen 2)** for this repository to Google Cloud.

---

## 1. Deployment

First, create the Pub/Sub topic and then deploy the Cloud Function.

### Create Pub/Sub Topic

Run the following command to create the Pub/Sub topic that will trigger the function:

```bash
gcloud pubsub topics create clear-db-topic
```

### Deploy the Function

Run the following command from the project root to deploy the function:

```bash
gcloud functions deploy document-clear-db \
  --gen2 \
  --runtime python312 \
  --region me-west1 \
  --source=. \
  --entry-point=main \
  --trigger-topic=clear-db-topic \
  --ingress-settings internal-only 
```

---

## 2. Testing the Deployment

After successful deployment, you can test the function by publishing a message to the `clear-db-topic` Pub/Sub topic.

The function expects a JSON payload with a list of strings under the key "items".

### Example Test Message

```json
{
  "items": ["DnaTransaction1", "DnaTransaction2", "DnaTransaction3"]
}
```

### Publish a Test Message

Use the following `gcloud` command to publish the message:

```bash
gcloud pubsub topics publish clear-db-topic --message='{"items": ["DnaTransaction1", "DnaTransaction2", "DnaTransaction3"]}'
```

After publishing the message, check the function's logs in the Google Cloud Console to verify that it was executed successfully.

---

## 3. Checking Logs

You can monitor the function's execution and view logs using the `gcloud` command-line tool. This is useful for confirming that the function ran successfully or for debugging errors.

### View All Logs

To view the logs for the `document-clear-db` function, run the following command:

```bash
gcloud functions logs read document-clear-db --gen2 --region=me-west1 --limit=50
```

### Health Check

To perform a health check, publish a special message to the topic:

```bash
gcloud pubsub topics publish clear-db-topic --message='{"health_check": true}'
```

Then, check the logs. You should see a "Health check successful" message.

---

## 4. Schedule Daily Clear (Noon + Midnight UTC)

To schedule the function to run daily at Noon (12:00 PM) and midnight (00:00 AM) UTC, create a Cloud Scheduler job that publishes a message to the `clear-db-topic`.

The following command creates a job that sends a message with an empty list of items. You can modify the `--message-body` if you need to clear specific items on a schedule.

```bash
gcloud scheduler jobs create pubsub document-clear-db-12h   --location europe-west2   --schedule "0 0,12 * * *"   --time-zone "Asia/Jerusalem"   --topic clear-db-topic   --message-body '{"items": []}'
```

---

## 5. Notes

- **`--gen2`**: Deploys to Cloud Functions Gen 2 (which runs on Cloud Run).
- **`--source=.`**: Uses the current directory for the source code. The `.gcloudignore` file controls which files are excluded from the deployment.
- **`--entry-point=main`**: This must match the name of the Python function in `main.py` that will be executed.
- **`--trigger-topic=clear-db-topic`**: This specifies that the function is triggered by messages published to the `clear-db-topic` Pub/Sub topic.

---

## 6. `.gcloudignore`

Make sure you have a `.gcloudignore` file in your project root to exclude unnecessary files from the deployment, which can speed up the process.

### Enable `.gcloudignore`

Run this command to ensure `.gcloudignore` is enabled:

```bash
gcloud config set gcloudignore/enabled true
```

### Example `.gcloudignore`

Here is a recommended `.gcloudignore` file for this project:

```
# Ignore common local/dev artifacts
.git
.gitignore
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
*.ipynb
data/
tests/

# Ensure requirements.txt is deployed
!requirements.txt
```
