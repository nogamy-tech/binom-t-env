resource "google_project_service" "compute" {
  project = var.project_id
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}

resource "time_sleep" "wait_60_seconds" {
  create_duration = "60s"
  depends_on = [ google_project_service.compute ]
}

resource "google_compute_region_network_endpoint_group" "serverless_neg" {
  project = var.project_id
  name                  = var.neg_name[count.index]
  region                = var.region
  network_endpoint_type = "SERVERLESS"
  cloud_run {
    service = var.cloud_run_names[count.index]
  }
  count = length(var.neg_name)
  depends_on = [ time_sleep.wait_60_seconds ]
}

resource "google_compute_region_backend_service" "backend_service" {
  project = var.project_id
  name                  = var.backend_service_name[count.index]
  region                = var.region
  load_balancing_scheme = "INTERNAL_MANAGED"
  protocol              = "HTTP"
  backend {
    group = google_compute_region_network_endpoint_group.serverless_neg[count.index].id
  }
  count = length(var.backend_service_name)
}

resource "google_compute_region_url_map" "url_map" {
  project = var.project_id
  name   = var.lb_name
  region = var.region

  default_service = google_compute_region_backend_service.backend_service[0].id

  host_rule {
    hosts        = ["*"]
    path_matcher = "path-matcher"
  }

  path_matcher {
    name = "path-matcher"

    default_service = google_compute_region_backend_service.backend_service[0].id

    path_rule {
      paths   = ["/getResult"]
      service = google_compute_region_backend_service.backend_service[0].id
    }

    path_rule {
      paths   = ["/getSummary"]
      service = google_compute_region_backend_service.backend_service[1].id
    }
  }
}

resource "google_compute_region_target_http_proxy" "http_proxy" {
  project = var.project_id
  name            = var.http_proxy_name
  region          = var.region
  url_map         = google_compute_region_url_map.url_map.id
}

resource "google_compute_forwarding_rule" "http_forwarding_rule" {
  project = var.project_id
  name                  = var.http_forwarding_rule_name
  region                = var.region
  load_balancing_scheme = "INTERNAL_MANAGED"
  target                = google_compute_region_target_http_proxy.http_proxy.self_link
  port_range            = "80"
  network               = var.network
  subnetwork            = var.subnetwork
}
