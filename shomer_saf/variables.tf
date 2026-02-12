



variable "region" {
  type    = string
  default = "me-west1"
}

variable "zone" {
  type    = string
  default = "me-west1-a"
}

# --------------------------------------------------------------------------------

variable "sa_name" {
  description = "Service Account name"
  type        = string
  default     = "nogamy-sa"

}

variable "bucket_name_1" {
  type    = string
  default = "bucket_shomer_saf"
}

variable "folder_name_1" {
  type    = string
  default = "documents_bucket_folder"
}
variable "folder_name_2" {
  type    = string
  default = "pages_bucket_folder"
}
variable "folder_name_3" {
  type    = string
  default = "data_bucket_folder"
}


variable "function_name_1" {
  type    = string
  default = "document-page-processing"
}
variable "function_name_2" {
  type    = string
  default = "document-pre-processing"
}

variable "function_name_3" {
  type    = string
  default = "document-process-query"
}
variable "function_name_4" {
  type    = string
  default = "document-start-job"
}
variable "function_name_5" {
  type    = string
  default = "document-query-get"
}

# isnt with http endpoint - needs a diffrent terraform
variable "function_name_6" {
  type    = string
  default = "document-clear-db"
}


variable "firestore_db_name_1" {
  type    = string
  default = "firestore-shomer-saf"
}
variable "firestore_db_name_2" {
  type    = string
  default = "firestore-accounts-db-temporary"
}

variable "bigquery_db_name" {
  type    = string
  default = "bigquery_shomer_saf"
}
variable "documentai_parser_name" {
  type    = string
  default = "nogamy-document-processor"
}




variable "load_balancer_name" {
  type        = string
  description = "The name of the regional Load Balancer (URL Map)"
  # binom datapro:
  # default     = "lb-binom"
  # binom d-i:
  default = "binom-lb-t"
}

# variable "load_balancer_proxy_name" {
#   type    = string
#   # binom datapro:
#   # default = "lb-binom-target-proxy"
#   # binom d-i:
#   default = "binom-proxy-d-i"
# }


