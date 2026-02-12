# locals {
#   labels_neg = {
    
#     environment = terraform.workspace
#     module      = "neg-${var.function_name}"
#     # "${var.module_name}:${var.function_name}"
#     version     = var.module_version
#     owner       = var.module_owner
#     project     = var.project

    
#   }

#     labels_be = {
    
#     environment = terraform.workspace
#     module      = "be-${var.function_name}"
#     # "${var.module_name}:${var.function_name}"
#     version     = var.module_version
#     owner       = var.module_owner
#     project     = var.project

    
#   }
# }



# 1. Create a Serverless region NEG (network_endpoint_group) for your function
      # regional unlike global  doesn't support labels
resource "google_compute_region_network_endpoint_group" "run_neg" {
  name                  = "neg-${var.function_name}"
  region                = var.region


  # labels = local.labels_neg
  
  network_endpoint_type = "SERVERLESS"


  cloud_run {
  service = "cf-nogamy-${var.function_name}"
  }

}



# 2. Create a *regional* Backend Service for that NEG
    # regional unlike global  doesn't support labels
resource "google_compute_region_backend_service" "cloud_function_backend" {
  name                  = "bs-${var.function_name}"
  region                = var.region
  # labels = local.labels_be
  
  protocol              = "HTTPS"
  load_balancing_scheme = "INTERNAL_MANAGED"

  backend {
    group           = google_compute_region_network_endpoint_group.run_neg.id
    balancing_mode  = "UTILIZATION"      
    capacity_scaler = 1.0
  }

  port_name                    = "http"
  timeout_sec                  = 30
  session_affinity             = "NONE"
  connection_draining_timeout_sec = 0
  enable_cdn                   = false

  # not sure what it is - but thats how defined in gui
#   log_config {
#     enable = false
#   }
}

# 3. Attach the rule to your existing URL map without terraform control over load balancer
# resource "null_resource" "add_lb_rule" {
#   depends_on = [google_compute_region_backend_service.cloud_function_backend]

#   provisioner "local-exec" {
#     command = <<EOT
# gcloud compute url-maps add-path-rule lb-binom --path-matcher-name=path-matcher-1 --paths="/shomer-saf/${var.url_path}/*" --service=${google_compute_region_backend_service.cloud_function_backend.id} --region=${var.region} --project=${var.project_id}
# EOT

#   }
# }








# output "my_message" {
#   value = "bucket created: ${var.function_name}"
# }
