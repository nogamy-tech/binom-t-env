variable "project_id" {
  type = string
}
variable "region" {
  type    = string
  default = "me-west1"
}
variable "function_name" {
  type = string
}
variable "source_dir" {
  type = string
}
variable "bucket_name" {
  type = string
}
variable "service_account_email" {
  type = string
}
variable "vpc_connector" {
  type    = string
  default = null
}
variable "trigger_topic" {
  type        = string
  description = "The Pub/Sub topic ID to trigger the function"
}

# Optional configurations
variable "runtime" {
  type    = string
  default = "python312"
}
variable "entry_point" {
  type    = string
  default = "main" # existing code uses "main"
}
variable "memory" {
  type    = string
  default = "512M"
}
variable "cpu" {
  type    = string
  default = "1"
}
variable "timeout_seconds" {
  type    = string
  default = "300"
}
variable "max_instances" {
  type    = string
  default = "2"
}

# Labels
variable "module_type" {
  type    = string
  default = "cloud-function-v2-pubsub"
}
variable "module_version" {
  type    = string
  default = "v1-0-0"
}
variable "module_owner" {
  type    = string
  default = "nogamy"
}
variable "project" {
  type    = string
  default = "shomer-saf"
}
