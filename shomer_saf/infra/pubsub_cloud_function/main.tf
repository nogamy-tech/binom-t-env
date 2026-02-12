locals {
  labels = {
    environment = terraform.workspace
    module      = "${var.module_type}-${var.function_name}"
    version     = var.module_version
    owner       = var.module_owner
    project     = var.project
  }
}

# # 1. Archive the function source code
# data "archive_file" "function_zip" {
#   type        = "zip"
#   output_path = "${path.root}/tmp/${var.function_name}-src.zip"
#   source_dir  = var.source_dir
# }

# # 2. Upload ZIP to GCS bucket
# resource "google_storage_bucket_object" "function_archive" {
#   name   = "${var.function_name}/function.zip"
#   bucket = var.bucket_name
#   source = data.archive_file.function_zip.output_path
# }

# 3. Deploy the Cloud Function with Pub/Sub Trigger
resource "google_cloudfunctions2_function" "function" {
  name        = "cf-nogamy-${var.function_name}"
  project     = var.project_id
  location    = var.region
  description = "A Python Cloud Function deployed via Terraform with Pub/Sub trigger"
  labels      = local.labels

  build_config {
    runtime     = var.runtime
    entry_point = var.entry_point
    source {
      storage_source {
        bucket = var.bucket_name
        # object = google_storage_bucket_object.function_archive.name
        object = "${var.function_name}/function.zip"
      }
    }
  }

  service_config {
    max_instance_count             = tonumber(var.max_instances)
    available_cpu                  = tonumber(var.cpu)
    available_memory               = var.memory
    timeout_seconds                = tonumber(var.timeout_seconds)
    ingress_settings               = "ALLOW_INTERNAL_ONLY" # Allows traffic from Eventarc (Pub/Sub)
    service_account_email          = var.service_account_email
    all_traffic_on_latest_revision = true
  }

  event_trigger {
    trigger_region = var.region
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = var.trigger_topic
    retry_policy   = "RETRY_POLICY_DO_NOT_RETRY" # Simple default
  }
}

# 4. VPC Egress Update (Workaround for Terraform limitation if needed, copied from http module)
# resource "null_resource" "function_vpc_egress" {
#   depends_on = [google_cloudfunctions2_function.function]
#   provisioner "local-exec" {
#     command = "gcloud run services update ${google_cloudfunctions2_function.function.name} --region=${var.region} --vpc-egress=all-traffic --vpc-connector=${var.vpc_connector} --project=${var.project_id}"
#   }
# }

# # 5. Cleanup zip file
# resource "null_resource" "cleanup_zip" {
#   depends_on = [google_storage_bucket_object.function_archive]

#   provisioner "local-exec" {
#     command = "del /f ${path.root}\\tmp\\${var.function_name}-src.zip"
#     interpreter = ["cmd", "/C"]
#   }
# }
