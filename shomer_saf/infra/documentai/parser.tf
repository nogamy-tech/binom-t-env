
# locals {
#   labels = {
    
#     environment = terraform.workspace
#     module      = "${var.module_type}-${var.parser_name}"
#     # "${var.module_name}:${var.function_name}"
#     version     = var.module_version
#     owner       = var.module_owner
#     project     = var.project

    
#   }
# }


# Using existing Document AI processor - commented out resource creation
resource "google_document_ai_processor" "parser" {
  display_name = var.parser_name
  location      = "eu"
  type          = var.parser_type
  project       = var.project_id
}


output "parser_id" {
  description = "The full resource name of the Document AI processor"
  # Using existing processor ID
  value       = google_document_ai_processor.parser.id
}

# output "parser_short_id" {
#   description = "The short processor ID"
#   value       = "833753300759c5c0"
# }
# Outputs:
# parser_id = "projects/labor-459609/locations/eu/processors/833753300759c5c0"
# 
