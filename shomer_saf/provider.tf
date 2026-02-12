# Parameter which requires changing between gcp envirements:
variable "project_id" {
  type = string
  # binom datapro:
  # default = "dgt-gcp-cgov-d-datapro" 
  # binom d-i:
  default = "dgt-gcp-cgov-t-binom"
  # default = "labor-459609"
}
# Parameter which requires changing between gcp envirements:
variable "vpc_connector" {
  type = string
  # binom datapro:
  # default = "projects/dgt-gcp-cgov-net-office-0/locations/me-west1/connectors/binom-sha-d-serverless"
  # binom d-i:
  default = "projects/dgt-gcp-cgov-net-office-0/locations/me-west1/connectors/binom-dev-i-serverless"
  # default = null
}


# # Remote State Management
# # This configures Terraform to store the state file remotely, in a Google Cloud Storage (GCS) bucket
# # When you run terraform init, Terraform:Connects to GCS,Checks if a state file exists,Creates one if it doesn’t
# # The account running Terraform must have:roles/storage.admin or at minimum roles/storage.objectAdmin
# # it uses backend.hcl for parameters

terraform {
  backend "gcs" {
    bucket                      = "t-binom-iac"
    impersonate_service_account = "t-binom-iac@dgt-gcp-cgov-t-binom.iam.gserviceaccount.com"
    prefix                      = "shomer-saf"

  }
}


terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      # version = "~> 4.0"
      version = "~> 7.7" #latest version
    }
  }
}


# use in cicd:

provider "google" {
  # never comment out:  
  project                     = var.project_id
  region                      = var.region
  zone                        = var.zone
  impersonate_service_account = "t-binom-iac@dgt-gcp-cgov-t-binom.iam.gserviceaccount.com"
  # default_labels = {
  #   business_project_number = "null"
  #   project_name            = "cgov_binom"
  #   created_by              = "dataprofbinom_at_digital_gov_il"
  #   owner_role              = "platform-owner"
  #   owner_email             = "dataprofbinom_at_digital_gov_il"
  #   team_name               = "datadelivery"
  #   team_email              = "datadelivery_at_digital_gov_il"
  #   office_name             = "digital"
  #   office_number           = "10000638"
  #   department              = "data_and_ai"
  #   environment             = "test"
  #   purchase_order_number   = "4502283189"
  # }
}
provider "google-beta" {
  impersonate_service_account = "t-binom-iac@dgt-gcp-cgov-t-binom.iam.gserviceaccount.com"
}
