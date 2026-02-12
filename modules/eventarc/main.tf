resource "google_project_service" "eventarc" {
  project = var.project_id
  service            = "eventarc.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_iam_audit_config" "storage_audit" {
  project = var.project_id
  service = "storage.googleapis.com"

  audit_log_config {
    log_type = "DATA_WRITE"
  }
}

resource "google_eventarc_trigger" "eventarc_trigger" {
  name = var.trigger_name
  location = var.cloud_run_location
  project = var.project_id

  matching_criteria {
    attribute = "type"
    value     = "google.cloud.audit.log.v1.written"
  }

  matching_criteria {
    attribute = "serviceName"
    value     = "storage.googleapis.com"
  }

  matching_criteria {
    attribute = "methodName"
    value     = "storage.objects.create"
  }

  matching_criteria {
    attribute = "resourceName"
    operator = "match-path-pattern"
    value     = "/projects/_/buckets/${var.storage_bucket_name}/objects/**/Download/*"
  }

  destination {
    cloud_run_service {
      service = var.cloud_run_name
      region  = var.cloud_run_location
      path = "/"
    }
  }

  service_account = var.service_account

  depends_on = [
    google_project_service.eventarc,
  ]
}
