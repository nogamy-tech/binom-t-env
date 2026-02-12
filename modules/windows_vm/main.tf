resource "google_project_service" "compute" {
  project = var.project_id
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "iam" {
  project = var.project_id
  service            = "iam.googleapis.com"
  disable_on_destroy = false
}

resource "time_sleep" "wait_60_seconds" {
  create_duration = "60s"
  depends_on = [ google_project_service.compute ]
}

resource "google_service_account" "vm_instance_service_account" {
  project = var.project_id
  account_id   = var.service_account_vm_name
  display_name = "SA for windows-VM Instance"
  depends_on = [ google_project_service.iam ]
}

resource "google_project_iam_member" "bucket_user" {
  project = var.project_id
  role = var.roles[count.index]
  member = "serviceAccount:${google_service_account.vm_instance_service_account.email}"
  count = length(var.roles)
}

resource "google_compute_instance" "windows_vm"{
    project = var.project_id
    name = var.vm_name
    machine_type = var.machine_type
    allow_stopping_for_update = true
    zone = var.zone
    labels = {
      always-on = "false"
      auto-start = "true"
    }
    tags = ["allow-rdp"]
    boot_disk {
      initialize_params {
        image = var.image
      }
    }
    network_interface {
      network = var.network_id
      subnetwork = var.subnetwork_id
    }
    service_account {
      email = google_service_account.vm_instance_service_account.email
      scopes = [
        "https://www.googleapis.com/auth/compute",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring",
        "https://www.googleapis.com/auth/pubsub",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/devstorage.full_control",
        "https://www.googleapis.com/auth/taskqueue",
        "https://www.googleapis.com/auth/userinfo.email"
      ]
    }
    metadata = {
      "block-project-ssh-keys" = true
      "enable-oslogin" = "TRUE"
    }
    depends_on = [ time_sleep.wait_60_seconds ]
}
