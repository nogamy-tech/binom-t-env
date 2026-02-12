variable "region" {
  default = "us-west1"
}

variable "zone" {
  default = "us-west1-a"
}

variable "project_id" {
  default = "qwiklabs-gcp-00-c67fc0134ef9" # replace this with your actual Project ID
}

variable "network" {
  description = "The self_link of the VPC network to attach instances to."
  type        = string
}

variable "subnet_01" {
  description = "The self_link of subnet-01."
  type        = string
}

# variable "subnet_02" {
#   description = "The self_link of subnet-02."
#   type        = string
# }



