resource "google_project_service" "run" {
  project = var.project_id
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

data "google_vpc_access_connector" "connector" {
  name = var.connector_name
  region = var.location
  project = var.host_project_id
}

resource "google_cloud_run_v2_service" "cloud_run"{
  project = var.project_id
  name = var.cloud_run_name
  location = var.location
  ingress = "INGRESS_TRAFFIC_INTERNAL_ONLY"
  deletion_protection = false
  template {
    containers {
      ports {
        container_port = 8080
      }
      image = var.container_image
    }

    vpc_access{
      connector = data.google_vpc_access_connector.connector.id
      egress = "ALL_TRAFFIC"
    }
  }

  depends_on = [ google_project_service.run ]
}

resource "google_cloud_run_v2_service_iam_member" "invoker" {
  project = google_cloud_run_v2_service.cloud_run.project
  location = google_cloud_run_v2_service.cloud_run.location
  name  = google_cloud_run_v2_service.cloud_run.name

  role   = "roles/run.invoker"
  member = "allUsers"
}
