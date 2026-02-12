
# # try to look up the service account (if it already exists)
# data "google_service_account" "existing" {
#   account_id = var.sa_name
#   project    = var.project_id
# }

# # 1 Create Service Account if doesn't exist
# resource "google_service_account" "sa" {
#   count        = try(length(data.google_service_account.existing.email), 0) > 0 ? 0 : 1
#   account_id   = var.sa_name
#   display_name = "Service Account for ${var.sa_name}"
#   project      = var.project_id
# }
# locals {
#   service_account_email = coalesce(
#     try(data.google_service_account.existing.email, null),
#     try(google_service_account.sa[0].email, null)
#   )
# }

# Create Service Account
# note: there would be error if trying to recreate existing sa 
# (would happen when trying to recreate outside the existing state)
resource "google_service_account" "sa" {
  account_id   = var.sa_name
  display_name = "Service Account for ${var.sa_name}"
  project      = var.project_id
}

locals {
  service_account_email = google_service_account.sa.email
}



# -------------------------
# 3 Assign Permissions (Roles)
# -------------------------
locals {
  runtime_roles = [
    # Vertex AI
    "roles/aiplatform.user",
    # Vertex AI New Express access
    "roles/aiplatform.expressUser",
    "roles/documentai.apiUser",
    "roles/storage.objectAdmin",
    "roles/secretmanager.secretAccessor",
    "roles/secretmanager.viewer",
    "roles/workflows.invoker",
    # Allow invoking Cloud Functions (Cloud Run services)
    "roles/run.invoker",
    "roles/bigquery.dataEditor",
    "roles/datastore.user",
    # depreaciated: roles/logging.logsEditor
    "roles/logging.logWriter",
    "roles/logging.viewer"

  ]

  infra_roles = [
    "roles/iam.serviceAccountUser",
    "roles/storage.admin",
    "roles/bigquery.dataOwner",
    "roles/logging.admin",
    "roles/datastore.owner"


  ]
}

# Add all roles to SA
resource "google_project_iam_member" "runtime_roles" {
  for_each = toset(local.runtime_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${local.service_account_email}"
}

resource "google_project_iam_member" "infra_roles" {
  for_each = toset(local.infra_roles)
  project  = var.project_id
  role     = each.value
  member   = "serviceAccount:${local.service_account_email}"
}





# both print and create a parmeter to be used in file
output "email" {
  value = local.service_account_email
}

# -------------------------
# Allow cloudfunction-poc to impersonate nogamy-sa
# -------------------------
# resource "google_service_account_iam_member" "allow_impersonation_token_creator" {
#   service_account_id = google_service_account.sa.name
#   role               = "roles/iam.serviceAccountTokenCreator"
#   member             = "serviceAccount:cloudfunction-poc@dgt-gcp-cgov-svc-runnerfactory.iam.gserviceaccount.com"
# }

resource "google_service_account_iam_member" "gitlab_1930_token_creator" {
  service_account_id = "projects/dgt-gcp-cgov-t-binom/serviceAccounts/nogamy-sa@dgt-gcp-cgov-t-binom.iam.gserviceaccount.com"
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "principalSet://iam.googleapis.com/projects/106559040889/locations/global/workloadIdentityPools/prod-gitlab-wif-pool/attribute.project_id/1930"
}

resource "google_service_account_iam_member" "allow_impersonation_user" {
  service_account_id = google_service_account.sa.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:cloudfunction-poc@dgt-gcp-cgov-svc-runnerfactory.iam.gserviceaccount.com"
}

