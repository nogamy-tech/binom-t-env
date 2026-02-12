terraform {
  required_providers {
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 6.0"
    }
  }
}

provider "google-beta" {
  project = var.project_id
  alias  = "custom"
  # region  = "europe-west1"
}

resource "google_service_usage_consumer_quota_override" "documentai_ocr_quota" {
  provider = google-beta.custom
  project  = var.project_id

  service        = "documentai.googleapis.com"
  metric         = "documentai.googleapis.com/processor_online_process_document_requests_eu"
  limit          = urlencode("min/project/processor_type")
  override_value = "250"

  dimensions = {
   # project = var.project_id
    processor_type = "OCR_PROCESSOR"
  }

  force = true
}