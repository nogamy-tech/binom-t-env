variable "project_id" {
  type = string
}

variable "service_account_vm_name" {
  type = string
}

variable "zone" {
  type = string
}

variable "vm_name" {
  type = string
}

variable "network_id" {
  type = string
}

variable "subnetwork_id" {
  type = string
}

variable "machine_type" {
  type = string
  default = "e2-medium"
}

variable "image" {
  type = string
  default = "windows-server-2025-dc-v20241212"
}

variable "roles" {
  type = list(string)
  default = ["roles/storage.bucketViewer", "roles/storage.objectUser", "roles/run.invoker"]
}
