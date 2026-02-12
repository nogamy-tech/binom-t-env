variable "project_id" {
  description = "The ID of the project in which the resource belongs."
  type        = string
}

variable "workflow_name" {
  description = "Name of the workflow."
  type        = string
}

variable "region" {
  description = "The region of the workflow."
  type        = string
}

variable "description" {
  description = "Description of the workflow."
  type        = string
  default     = "Managed by Terraform"
}

variable "service_account_email" {
  description = "Service account email to run the workflow."
  type        = string
}

variable "source_contents" {
  description = "Content of the workflow YAML."
  type        = string
}

variable "deletion_protection" {
  description = "Whether to enable deletion protection."
  type        = bool
  default     = false
}
