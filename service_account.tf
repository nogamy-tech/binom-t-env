resource "google_project_service" "serviceusage" {
  project = var.project_id
  service            = "serviceusage.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudresourcemanager" {
  project = var.project_id
  service            = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
  depends_on = [ google_project_service.serviceusage ]
}

resource "google_project_iam_member" "sa-binom" {
  project = var.project_id
  role = var.roles_email_binom[count.index]
  member = "serviceAccount:${var.email_binom}"
  count = length(var.roles_email_binom)
}


resource "google_project_service" "iam" {
  project = var.project_id
  service            = "iam.googleapis.com"
  disable_on_destroy = false
  depends_on = [google_project_service.cloudresourcemanager]
}

resource "google_project_service" "pubsub" {
  project = var.project_id
  service            = "pubsub.googleapis.com"
  disable_on_destroy = false
}

resource "time_sleep" "wait_60_seconds" {
  create_duration = "60s"
  depends_on = [ google_project_service.iam ]
}

resource "google_service_account" "eventarc_sa" {
  project = var.project_id
  account_id = var.service_account_eventarc_name
  display_name = "Eventarc Trigger Service Account"
  depends_on = [ time_sleep.wait_60_seconds ]
}

resource "google_project_iam_member" "eventreceiver" {
  project = var.project_id
  role = var.roles_eventarc[count.index]
  member = "serviceAccount:${google_service_account.eventarc_sa.email}"
  count = length(var.roles_eventarc)
}

data "google_storage_project_service_account" "gcs_account" {
  project = var.project_id
}

resource "google_project_iam_member" "pubsubpublisher" {
  project = var.project_id
  role = "roles/pubsub.publisher"
  member = "serviceAccount:${data.google_storage_project_service_account.gcs_account.email_address}"
}

data "google_project" "project" {
  project_id = var.project_id
}

data "google_service_account" "cloud_run_sa" {
  account_id = "${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

resource "google_project_iam_member" "cloud_run_roles" {
  project = var.project_id
  role = var.roles_cloud_run[count.index]
  member = "serviceAccount:${data.google_service_account.cloud_run_sa.email}"
  count = length(var.roles_cloud_run)
}

resource "google_project_service" "vertex_ai" {
  project = var.project_id
  service = "aiplatform.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_iam_member" "deploy_cloud_run" {
  project = var.project_id
  role = var.roles_sa_runner[count.index]
  member = "serviceAccount:${var.sa_runner}"
  count = length(var.roles_sa_runner)
}