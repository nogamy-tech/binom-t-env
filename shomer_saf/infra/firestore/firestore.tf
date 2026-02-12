

# locals {
#   labels = {
    
#     environment = terraform.workspace
#     module      = "${var.module_type}-${var.firestore_db_name}"
#     # "${var.module_name}:${var.function_name}"
#     version     = var.module_version
#     owner       = var.module_owner
#     project     = var.project

    
#   }
# }




# Create firestore db (not a function calling):
# no need to create collections - they are created when first file is transfered
resource "google_firestore_database" "custom" {
    project     = var.project_id
    name        = var.firestore_db_name
    # "(default)"      # literal string, not a variable
    location_id = var.region
    type        = "FIRESTORE_NATIVE"

    # prevent deletion using terraform and dont recreate if name changes
    lifecycle {
    prevent_destroy = false
    ignore_changes  = [name]
    }
    # labels not supported
    # labels = var.labels
}