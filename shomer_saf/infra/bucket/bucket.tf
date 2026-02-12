
locals {
  labels = {
    
    environment = terraform.workspace
    module      = "${var.module_type}-${var.bucket_name}"
    # "${var.module_name}:${var.function_name}"
    version     = var.module_version
    owner       = var.module_owner
    project     = var.project

    
  }
}




# resource "google_storage_bucket" "tf-bucket" {
#   name                        = var.bucket_name_1
#   location                    = "EU" #"me-west1"

#   force_destroy               = true # Allows bucket deletion even if it contains objects.
#   uniform_bucket_level_access = true
# }



resource "google_storage_bucket" "bucket" {
    name     = var.bucket_name
    labels = local.labels

    # Bucket location: "EU":Multi-region (high availability across European data centers), "ME-WEST1": single region - Tel Aviv
    location = var.region

    # Storage class options:
    # - STANDARD (frequent access, low latency)
    # - NEARLINE (monthly access)
    # - COLDLINE (quarterly access)
    # - ARCHIVE (rare access)
    storage_class = "STANDARD"
    # # Enables Autoclass to automatically manage object storage class based on access patterns
    # autoclass {enabled = true}


    # Prevents any public access to this bucket or its objects
    # Options: "enforced", "unspecified"
    public_access_prevention = "enforced"

    uniform_bucket_level_access = true  # Use IAM-only access, no legacy object-level ACLs
    force_destroy               = true # Allows bucket deletion even if it contains objects.

    # Enable versioning for data protection (required by KICS security scan)
    versioning {
      enabled = true
    }

    # Optional: Log bucket access to a separate logging bucket
    logging {
      log_bucket        = var.log_bucket_name
      log_object_prefix = var.log_object_prefix
    }


    # Optional: soft delete retention window (7 days) - prevents objects from being deleted before a certain number of seconds
    # retention_policy {
    #   retention_period = var.bucket_retention_period
    # }

    # Automatically delete objects older than 30 days
    lifecycle_rule {
      action {
        type = "Delete"
      }
      condition {
        age = var.lifecycle_rule_age
      }
    }

    # when terraform runs: prevent deletion of resource & renaming it (deletion and recreation with diffrent name)
    # note: when commenting out the module terraform is un aware of lifecycle and deletion woul occur
    # lifecycle {
    # prevent_destroy = true
    # ignore_changes  = [name]
    # }
}




# create sub folders in bucket - not used if list is empty (defaul value)
resource "google_storage_bucket_object" "folder_marker" {
  depends_on = [google_storage_bucket.bucket]
  for_each = toset(var.folder_names)

  name    = "${each.value}/"      # the trailing slash makes it a folder marker
  bucket  = google_storage_bucket.bucket.name
  content = " "                   # minimal placeholder file
}


# both print and create a parmeter to be used in file
output "name" {
  value = google_storage_bucket.bucket.name
}

# output "my_message" {
#   value = "bucket created: ${var.bucket_name}"
# }
