
# # main.tf

# all connection info in provider.tf file

# ==============================================================================
# 1. IDENTITY & PROJECT INFRASTRUCTURE
# ==============================================================================

# 1.1 Service Account for Impersonation & Execution
# Creates the core Service Account and assigns necessary roles.
module "nogamy_sa" {
  source     = "./infra/service_account"
  sa_name    = var.sa_name
  project_id = var.project_id
}

# Print and forward parameter
output "nogamy_sa_email" {
  value = module.nogamy_sa.email
}




# Generate a random string (8 bytes) -  bucket names must be globally unique
resource "random_id" "random_prefix" {
  byte_length = 5
}
locals {
  prefix              = "${var.project_id}-${random_id.random_prefix.hex}"
  modules_source_path = abspath("${path.root}/modules")
}

output "modules_source_path" {
  value = local.modules_source_path
}

locals {
  function_names = [
    var.function_name_1,
    var.function_name_2,
    var.function_name_3,
    var.function_name_4,
    var.function_name_5,
  ]
  function_url_paths = {
    (var.function_name_1) = "PageProcessing"
    (var.function_name_2) = "PreProcessing"
    (var.function_name_3) = "ProcessQuery"
    (var.function_name_4) = "StartJob"
    (var.function_name_5) = "QueryGet"
  }
}





# ==============================================================================
# 2. CORE SERVICES & DATABASES
# ==============================================================================

# 2.1 Enable GCP APIs
module "nogamy_services" {
  source = "./infra/enable_services"
}

# 2.2 Document AI Processor
module "nogamy_documentai" {
  source      = "./infra/documentai"
  project_id  = var.project_id
  parser_name = var.documentai_parser_name
}



# 2.3 Firestore Databases
module "nogamy_firestore" {
  source            = "./infra/firestore"
  project_id        = var.project_id
  firestore_db_name = var.firestore_db_name_1
}

module "accounts_db_firestore" {
  source            = "./infra/firestore"
  project_id        = var.project_id
  firestore_db_name = var.firestore_db_name_2
}

# ==============================================================================
# 3. STORAGE BUCKETS
# ==============================================================================

# 3.0 PERMANENT Bucket for Cloud Function Source ZIPs (NEVER DELETE)
resource "google_storage_bucket" "permanent_source_bucket" {
  name          = "gcs-binom-shomer-saf-test"
  location      = var.region
  project       = var.project_id
  storage_class = "STANDARD"

  # Prevent Terraform from destroying this bucket ##
  lifecycle {
    prevent_destroy = true
  }

  logging {

    log_bucket = module.logging_bucket.name

  }

  # Uniform bucket-level access (recommended)
  uniform_bucket_level_access = true

  # Enable versioning to protect against accidental overwrites
  versioning {
    enabled = true
  }
}

# 3.1 Logging Bucket (receives logs from other buckets - no logging on itself to avoid loop)
module "logging_bucket" {
  source            = "./infra/bucket"
  bucket_name       = "logs-${local.prefix}"
  log_bucket_name   = "t-binom-outputs"
  log_object_prefix = "logs-bucket-logs"
}

# 3.1 Data Bucket (with designated folders)
locals {
  BUCKET_NAME = "${var.bucket_name_1}-${local.prefix}"
  folder_names = [
    var.folder_name_1, var.folder_name_2, var.folder_name_3
  ]
}

module "bucket" {
  source            = "./infra/bucket"
  bucket_name       = local.BUCKET_NAME
  folder_names      = local.folder_names
  log_bucket_name   = "t-binom-outputs"
  log_object_prefix = "logging"
}

# 3.2 Functions Source Code Bucket
module "source_bucket" {
  source            = "./infra/bucket"
  bucket_name       = "src-${local.prefix}"
  log_bucket_name   = "t-binom-outputs"
  log_object_prefix = "src-bucket-logs"
}

# ==============================================================================
# 4. CLOUD FUNCTIONS (HTTP & EVENT TRIGGERED)
# ==============================================================================

# 4.1 HTTP Cloud Functions (Deployment & Configuration)
module "http_cloud_functions" {
  for_each = toset(local.function_names)

  source        = "./infra/http_cloud_function"
  function_name = each.value
  source_dir    = "${local.modules_source_path}/${each.value}"
  # bucket_name           = module.source_bucket.name
  bucket_name           = google_storage_bucket.permanent_source_bucket.name
  vpc_connector         = var.vpc_connector
  service_account_email = module.nogamy_sa.email
  project_id            = var.project_id
  entry_point           = "flask_app"
}



# # delete bucket after functions are deployed
# resource "null_resource" "cleanup_function_bucket" {
#   depends_on = [module.http_cloud_functions]
#   provisioner "local-exec" {
#     command = "gsutil rm -r gs://${google_storage_bucket.function_bucket.name}"
#   }
# }

# ==============================================================================
# 5. LOAD BALANCING & NETWORKING
# ==============================================================================

# 5.1 NEGs & Backend Services per function
module "load_balancer_rules" {
  for_each      = local.function_url_paths
  source        = "./infra/load_balancer_rule"
  function_name = each.key
  url_path      = each.value
  project_id    = var.project_id

  depends_on = [module.http_cloud_functions]
}

# 5.2 Unified URL Map (Routing Rules)
# resource "google_compute_region_url_map" "lb_url_map" {
#   name            = var.load_balancer_name
#   project         = var.project_id
#   region          = var.region
#   default_service = "projects/${var.project_id}/regions/${var.region}/backendServices/bs-cloudrun"

#   host_rule {
#     hosts        = ["binom.dev.cgov.dgt.gcp.internal"]
#     path_matcher = "path-matcher-1"
#   }

#   path_matcher {
#     name            = "path-matcher-1"
#     default_service = "projects/${var.project_id}/regions/${var.region}/backendServices/bs-cloudrun"

#     # Dynamic rules for shomer-saf functions
#     dynamic "path_rule" {
#       for_each = local.function_url_paths
#       content {
#         paths   = ["/shomer-saf/${path_rule.value}/*"]
#         service = module.load_balancer_rules[path_rule.key].backend_service_id
#       }
#     }
#   }

#   depends_on = [module.load_balancer_rules]
# }

# # 5.3 Target HTTP Proxy
# resource "google_compute_region_target_http_proxy" "lb_proxy" {
#   name    = var.load_balancer_proxy_name
#   project = var.project_id
#   region  = var.region
#   url_map = google_compute_region_url_map.lb_url_map.id
# }



# 4.2 Async Tasks & Database Cleanup (PubSub + Scheduler)
resource "google_pubsub_topic" "clear_db_topic" {
  name    = "topic-document-clear-db"
  project = var.project_id
}

module "document_clear_db" {
  source                = "./infra/pubsub_cloud_function"
  function_name         = var.function_name_6
  trigger_topic         = google_pubsub_topic.clear_db_topic.id
  source_dir            = "${local.modules_source_path}/${var.function_name_6}"
  bucket_name           = google_storage_bucket.permanent_source_bucket.name
  vpc_connector         = var.vpc_connector
  service_account_email = module.nogamy_sa.email
  project_id            = var.project_id
  entry_point           = "main"
}

resource "google_cloud_scheduler_job" "clear_db_scheduler" {
  name        = "document-clear-db-12h"
  description = "Trigger document-clear-db function every 12 hours"
  schedule    = "0 0,12 * * *"
  time_zone   = "Asia/Jerusalem"
  region      = "europe-west3"
  project     = var.project_id

  pubsub_target {
    topic_name = google_pubsub_topic.clear_db_topic.id
    data       = base64encode("{\"items\": []}")
  }

  depends_on = [module.nogamy_services]
}

# ==============================================================================
# 6. SECRET MANAGEMENT (VAULT)
# ==============================================================================
# save LLM model to use (text and image):
# text: #gemini-2.5-flash is optimized for speed/efficiency, Alternative for complex tasks gemini-2.5-pro
# image (multimodal): gemini-2.5-pro there is no alternative
module "nogamy_secret_text_model" {
  source      = "./infra/secret_vault"
  secret_id   = "NOGAMY_TEXT_MODEL"
  secret_data = "gemini-2.5-flash"
  project_id  = var.project_id
}


module "nogamy_secret_image_model" {
  source      = "./infra/secret_vault"
  secret_id   = "NOGAMY_IMAGE_MODEL"
  secret_data = "gemini-2.5-pro"
  project_id  = var.project_id
}

module "nogamy_secret_bucket" {
  source      = "./infra/secret_vault"
  secret_id   = "NOGAMY_BUCKET"
  secret_data = local.BUCKET_NAME
  project_id  = var.project_id

  depends_on = [module.bucket]


}

module "nogamy_secret_sa" {
  source      = "./infra/secret_vault"
  secret_id   = "NOGAMY_SA"
  secret_data = module.nogamy_sa.email
  project_id  = var.project_id

  depends_on = [module.nogamy_sa]
}


module "nogamy_secret_firestore" {
  source      = "./infra/secret_vault"
  secret_id   = "NOGAMY_FIRESTORE"
  secret_data = var.firestore_db_name_1
  project_id  = var.project_id

  depends_on = [module.nogamy_firestore]
}

module "accounts_db_secret_firestore" {
  source      = "./infra/secret_vault"
  secret_id   = "ACCOUNTS_FIRESTORE"
  secret_data = var.firestore_db_name_2
  project_id  = var.project_id

  depends_on = [module.accounts_db_firestore]

}

module "nogamy_secret_documentai" {
  source      = "./infra/secret_vault"
  secret_id   = "NOGAMY_DOCUMENTAI_PROCESSOR_ID"
  secret_data = module.nogamy_documentai.parser_id
  project_id  = var.project_id


  depends_on = [module.nogamy_documentai]
}

module "secret_buckets_time_clear_cutoff" {
  source      = "./infra/secret_vault"
  secret_id   = "BUCKETS_TIME_CLEAR_CUTOFF"
  secret_data = "1"
  project_id  = var.project_id
}

module "secret_firestore_time_clear_cutoff" {
  source      = "./infra/secret_vault"
  secret_id   = "FIRESTORE_TIME_CLEAR_CUTOFF"
  secret_data = "1"
  project_id  = var.project_id
}

module "secret_nogamy_workflow" {
  source      = "./infra/secret_vault"
  secret_id   = "NOGAMY_WORKFLOW"
  secret_data = "wf-binom-parent"
  project_id  = var.project_id
}

# ==============================================================================
# 7. WORKFLOW ORCHESTRATION
# ==============================================================================

module "parent_workflow" {
  source                = "./infra/workflow"
  workflow_name         = "wf-binom-parent"
  region                = "me-west1"
  description           = "parent workflow"
  service_account_email = module.nogamy_sa.email
  project_id            = var.project_id
  source_contents = replace(
    file("${local.modules_source_path}/nogamy_workflow/wf-binom-parent.yaml"),
    "$${DOCUMENT_PRE_PROCESSING_URI}",
    module.http_cloud_functions[var.function_name_2].function_uri
  )
}

module "child_workflow_1" {
  source                = "./infra/workflow"
  workflow_name         = "wf-binom-DocumentPageProcessing"
  region                = "me-west1"
  description           = "DocumentPageProcessing"
  service_account_email = module.nogamy_sa.email
  project_id            = var.project_id
  source_contents = replace(
    file("${local.modules_source_path}/nogamy_workflow/wf-binom-DocumentPageProcessing.yaml"),
    "$${DOCUMENT_PAGE_PROCESSING_URI}",
    module.http_cloud_functions[var.function_name_1].function_uri
  )
}

module "child_workflow_2" {
  source                = "./infra/workflow"
  workflow_name         = "wf-binom-DocumentProcessQuery"
  region                = "me-west1"
  description           = "DocumentProcessQuery"
  service_account_email = module.nogamy_sa.email
  project_id            = var.project_id
  source_contents = replace(
    file("${local.modules_source_path}/nogamy_workflow/wf-binom-DocumentProcessQuery.yaml"),
    "$${DOCUMENT_PROCESS_QUERY_URI}",
    module.http_cloud_functions[var.function_name_3].function_uri
  )
}

# --------------------------------------------------------
# # create bigquery db
# # not enabled in d-i-binom; not sure its needed
# # module "nogamy_bigquery" {
# #   source      = "./infra/bigquery"
# #   project_id     = var.project_id
# #   bigquery_db_name        = var.bigquery_db_name
# #   # depends_on      = [time_sleep.wait_for_apis]

# # }


output "my_message" {
  value = "Terraform run completed!"
}
