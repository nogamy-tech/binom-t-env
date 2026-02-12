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
  default     = "secret-vault"
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
variable "secret_data" {
  type = string
}

variable "secret_id" {
  type = string
}