variable "project_id" {
  type = string
  default = "dgt-gcp-cgov-t-binom"
}

variable "host_project_id" {
  type = string
  default = "dgt-gcp-cgov-net-office-0"
}

variable "project_name" {
  type = string
  default = "binom"
}

variable "environment" {
  type = string
  default = "tst"
}

variable "region" {
  type = string
  default = "me-west1"
}

# network module

variable "vpc_name" {
  type = string
  default = "test"
}

variable "subnet_name" {
  type = string
  default = "snet-test-binom"
}

variable "connector_name" {
  type = string
  default = "binom-test-serverless-vpc"
}

# windows vm module

variable "service_account_vm_name" {
  type = string
  default = "binom-sa-vm-tst"
}

variable "zone_part" {
  type = string
  default = "a"
}

# document AI module

variable "document_ai_location" {
  type = string
  default = "eu"
}

# firestore module

variable "tables_name" {
  type = list(string)
  default = [ "results", "summaries", "activity", "console"]
}

# cloud storages module

variable "cloud_storage_name" {
  type = string
  default = "gcs"
}

# https_trigger_cloud_run module

variable "https_cloud_run_names" {
  type = list(string)
  default = [ "get-result","get-summary" ]
}

variable "https_container_images" {
  type = list(string)
  default = [ "me-west1-docker.pkg.dev/dgt-gcp-cgov-registry/binom/t_getresults:1.3.1", "me-west1-docker.pkg.dev/dgt-gcp-cgov-registry/binom/t_getsummary:1.4.2" ]
}

# module eventarc trigger

variable "service_account_eventarc_name" {
  type = string
  default = "binom-sa-eventarc-tst"
}

variable "cloud_run_automation_name" {
  type = string
  default = "automation"
}

variable "automation_container_image" {
  type = string
  default = "me-west1-docker.pkg.dev/dgt-gcp-cgov-registry/binom/t_automation:1.3.6"
}

# module load balancer

variable "neg_names" {
  type = list(string)
  default = ["neg-getresult", "neg-getsummary"]
}

variable "backend_services_names" {
  type = list(string)
  default = ["back-getresult", "back-getsummary"]
}

# Service Account

variable "roles" {
  type = list(string)
  default = ["roles/storage.bucketViewer", "roles/storage.objectUser"]
}

variable "roles_cloud_run" {
  type = list(string)
  default = [ 
    "roles/eventarc.eventReceiver",
    "roles/datastore.user",
    "roles/documentai.apiUser",
    "roles/aiplatform.user",
    "roles/storage.objectUser",
    "roles/logging.logWriter",
    "roles/modelarmor.user",
    "roles/modelarmor.viewer"
  ]
}
variable "roles_eventarc" {
  type = list(string)
  default = [ "roles/eventarc.eventReceiver", "roles/run.invoker", "roles/pubsub.publisher", "roles/pubsub.subscriber" ]
}


variable "email_binom" {
  type = string
  default = "sa-binom-tst@dgt-gcp-cgov-mng-sa-0.iam.gserviceaccount.com"
}

variable "roles_email_binom" {
  type = list(string)
  default = [ "roles/run.invoker", "roles/run.developer" ]
}

variable "sa_runner" {
  type = string
  default = "binom-team-runner@dgt-gcp-cgov-svc-runnerfactory.iam.gserviceaccount.com"
}

variable "roles_sa_runner" {
  type = list(string)
  default = [ "roles/run.developer" ]
}