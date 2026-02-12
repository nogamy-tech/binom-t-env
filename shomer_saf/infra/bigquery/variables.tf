variable "region" {
  type = string
  default = "me-west1"
}

variable "zone" {
  type = string
  default = "me-west1-a"
}

variable "project_id" {
  type = string
  # default = "dgt-gcp-molb-doc-ai-nogamy-dev" # replace this with your actual Project ID
}
# ---------------------------------------------------------------------------------------
# labels:

variable "module_type" {
  description = "The name of this module (for labeling)"
  type        = string
  default     = "bigquery"
}

variable "module_version" {
  description = "The version of this module (for labeling)"
  type        = string
  default     = "v1-0-0"
}

variable "module_owner" {
  description = "The owner of this module (for labeling)"
  type        = string
  default     = "nogamy"
}

variable "project" {
  description = "The project name of this module (for labeling)"
  type        = string
  default     = "shomer-saf"
}
# --------------------------------------------------------------
variable "bigquery_db_name" {
  type = string
}

# variable "bucket_retention_period" {
#   type        = number
#   # default     = 604800  # 7 days
#   # default     = 30  # 0.5 minute
#   default = 1

#   description = "Retention period in seconds"
# }

# variable "lifecycle_rule_age" {
#   type        = number
#   default     = 30
#   description = "Number of days before lifecycle rule triggers (e.g., delete or storage class change)"
# }

# variable "folder_names" {
#   description = "List of folder names to create inside the GCS bucket"
#   type        = list(string)
#   # default     = ["folder1", "folder2", "folder3"]
# }
