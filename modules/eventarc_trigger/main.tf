module "cloud_run" {
  source = "../trigger_cloud_run"
  project_id = var.project_id
  cloud_run_name = var.cloud_run_name
  location = var.location
  container_image = var.container_image
  service_account = var.default_sa
  connector_name = var.connector_name
  host_project_id = var.host_project_id
}

module "eventarc" {
  source = "../eventarc"
  project_id = var.project_id
  trigger_name = var.trigger_name
  cloud_run_location = module.cloud_run.location
  storage_bucket_name = var.cloud_storage_name
  cloud_run_name = module.cloud_run.name
  service_account = var.email_sa
}
