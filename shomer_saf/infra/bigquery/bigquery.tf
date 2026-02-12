
locals {
  labels = {
    
    environment = terraform.workspace
    module      = "${var.module_type}-${var.bigquery_db_name}"
    # "${var.module_name}:${var.function_name}"
    version     = var.module_version
    owner       = var.module_owner
    project     = var.project

    
  }
}

# 1. Creates the BigQuery dataset

resource "google_bigquery_dataset" "logs_dataset" {
  dataset_id = var.bigquery_db_name
  project    = var.project_id
  location   = var.region
  description = "Stores exported logs from Cloud Logging"

  labels = local.labels
}

# 2. Creates a Logging Sink that exports logs from cloud logging into bigquery
resource "google_logging_project_sink" "logs_to_bigquery" {
  name                   = "export-logs-to-bigquery"
  project                = var.project_id
  destination            = "bigquery.googleapis.com/${google_bigquery_dataset.logs_dataset.id}"
  filter                 = "severity>=INFO" # Optional: filter which logs to include
  unique_writer_identity = true
}
# 3. Grants the sink service account permission to write
resource "google_bigquery_dataset_iam_member" "sink_writer" {
  dataset_id = google_bigquery_dataset.logs_dataset.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = google_logging_project_sink.logs_to_bigquery.writer_identity
}
