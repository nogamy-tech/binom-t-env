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
  default     = "cloud-function-v2"
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
# cloud function params

variable "max_instances" {
  type = string
  default = "2"
}
variable "runtime" {
  type = string
  default = "python312"
}
variable "entry_point" {
  type = string
  default = "hello_http"
}

variable "cpu" {
  type = string
  default = "1"
}
variable "memory" {
  type = string
  default = "512M"
}
variable "timeout_seconds" {
  type = string
  default = "300"
}





# ---------------------------------------------------------------
variable "function_name" {
  type = string
}
variable "source_dir" {
  type = string
}

variable "service_account_email" {
  type = string
}

variable "vpc_connector" {
  type = string
  default = null
}

variable "bucket_name" {
  type = string
}
# variable "path_" {
#   type = string
# }
