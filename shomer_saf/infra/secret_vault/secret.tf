# Create (or manage) the secret directly
resource "google_secret_manager_secret" "secret_vault" {
  project   = var.project_id
  secret_id = var.secret_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

# Always add or update the secret value
resource "google_secret_manager_secret_version" "secret_value_version" {
  secret      = google_secret_manager_secret.secret_vault.id
  secret_data = var.secret_data
}

# Outputs
output "secret_resource_id" {
  value = google_secret_manager_secret.secret_vault.id
}

output "secret_name" {
  value = var.secret_id
}
