resource "google_workflows_workflow" "workflow" {
  name            = var.workflow_name
  region          = var.region
  description     = var.description
  service_account = var.service_account_email
  project         = var.project_id
  source_contents = var.source_contents
  deletion_protection = false
}
