
# ----------------------------------------------------------------------
# Enable all Google Cloud APIs required for the Nogamy infrastructure
# ----------------------------------------------------------------------
# Terraform does NOT automatically enable APIs — this ensures all necessary
# services are active before creating dependent resources.
# ----------------------------------------------------------------------


resource "google_project_service" "required_services" {
  for_each = toset([
    # ----------------------------------------------------
    # 🔹 CORE APIs — required for project + IAM operations
    # ----------------------------------------------------
    "cloudresourcemanager.googleapis.com", # Needed for IAM policy bindings & project metadata
    "iam.googleapis.com",                  # Service Accounts, roles, and permissions
    "serviceusage.googleapis.com",         # Allows enabling/disabling other APIs programmatically

    # ----------------------------------------------------
    # 🔹 STORAGE & SECRETS
    # ----------------------------------------------------
    "storage.googleapis.com",              # Google Cloud Storage (buckets, folders, static files)
    "secretmanager.googleapis.com",        # Secret Manager for storing sensitive config values

    # ----------------------------------------------------
    # 🔹 FIRESTORE DATABASE
    # ----------------------------------------------------
    "firestore.googleapis.com",            # Firestore in native mode (NoSQL database)
    "datastore.googleapis.com",            # Datastore compatibility layer for Firestore APIs
    # ----------------------------------------------------
    # 🔹 BIGQUERY DATABASE
    # ----------------------------------------------------
    "bigquery.googleapis.com",
    # ----------------------------------------------------
    # 🔹 CLOUD FUNCTIONS + CLOUD RUN (Serverless backends)
    # ----------------------------------------------------
    "cloudfunctions.googleapis.com",       # Core API to deploy and manage Cloud Functions
    "artifactregistry.googleapis.com",     # Stores packaged function code (used by Cloud Functions v2)
    "run.googleapis.com",                  # Cloud Run runtime (Cloud Functions v2 executes on Cloud Run)
    "eventarc.googleapis.com",             # Routes events to Cloud Functions and Cloud Run
    "vpcaccess.googleapis.com",            # Allows Cloud Functions to connect to VPC networks
    "compute.googleapis.com",              # Required for load balancers, backend services, and VPCs

    # ----------------------------------------------------
    # 🔹 LOGGING & MONITORING
    # ----------------------------------------------------
    "logging.googleapis.com",              # Centralized logging (Cloud Logging)
    "monitoring.googleapis.com",           # Cloud Monitoring (metrics, dashboards)

    # ----------------------------------------------------
    # 🔹 DOCUMENT AI
    # ----------------------------------------------------
    "documentai.googleapis.com",           # Used by the Document AI parser module

    # ----------------------------------------------------
    # 🔹 OPTIONAL / SUPPORTING SERVICES
    # ----------------------------------------------------
    "pubsub.googleapis.com",               # Pub/Sub for async communication and triggers
    "cloudscheduler.googleapis.com",       # Cloud Scheduler for scheduled jobs
    "cloudbuild.googleapis.com"            # Cloud Build for building and packaging functions
  ])

  service = each.key
}

# ----------------------------------------------------------------------
# Optional: Wait a few seconds after enabling APIs
# Some APIs take 10–20 seconds to fully activate.
# ----------------------------------------------------------------------
resource "time_sleep" "wait_for_apis" {
  depends_on      = [google_project_service.required_services]
  create_duration = "20s"
}