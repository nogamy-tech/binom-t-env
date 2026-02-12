resource "google_project_service" "cloudresourcemanager" {
  project = var.project_id
  service            = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "documentai" {
  project = var.project_id
  service            = "documentai.googleapis.com"
  disable_on_destroy = false
}

resource "google_document_ai_processor" "processor" {
  project = var.project_id
  location = var.location
  display_name = var.name
  type = var.type
  depends_on = [ 
    google_project_service.cloudresourcemanager,
    google_project_service.documentai 
  ]
}
