# 🧾 Terraform Aplication Deployment — GCP Landing Zone Architecture

This repository contains a **modular, cloud-native document processing system** built on **Google Cloud Platform (GCP)**, using **Terraform** for infrastructure management and **Python** services deployed as **Cloud Functions** or **Cloud Run** instances. The system processes documents through multiple stages, integrates with Salesforce, and uses Google Document AI for OCR.

---

## 🛠️ Architecture Overview

The project is designed as a **Landing Zone blueprint** for GCP — a secure, scalable, and compliant multi-project environment. It follows Google Cloud best practices for:
- Project and folder hierarchy
- IAM roles and policies
- Networking and security baselines
- Audit logging and monitoring

Infrastructure is provisioned through [Terraform Example Foundation](https://github.com/terraform-google-modules/terraform-example-foundation), a well-supported, highly modular Terraform framework.

---

## 🧱 Core Principles

- **Infrastructure-as-Code**: All GCP infrastructure is defined using Terraform modules.
- **Application Modularity**: Business logic is structured as microservices for flexibility and isolation.
- **Environment Separation**: `dev` and `prod` environments are fully isolated with separate Terraform state, configs, and deployment flows.
- **Version Control**: New versions are developed and tested in `dev`, then promoted to `prod` via controlled workflows.
- **Experimentation-Driven Development**: Jupyter notebooks are used to validate, test, and document every module and integration.



# Use Gcloud CLI
## Install gcloud CLI and add to pc path
https://cloud.google.com/sdk/docs/install
## run from CLI
gcloud init

gcloud components update


# Connect to GCP project via Gcloud CLI

## clear old credentials or switch accounts
gcloud auth application-default revoke -q
## Sets Application Default Credentials (ADC) - Terraform uses it
gcloud auth application-default login 
## Log in to account
gcloud auth  login 
## Set the default project (for both gcloud and Terraform)
gcloud config set project YOUR_GCP_PROJECT # dgt-gcp-cgov-d-i-binom
 

# optional
## Check accounts (users)
gcloud auth list
## Set active account 
gcloud config set account your_email@gmail.com
## Check accounts (project)
gcloud config list project
## Log in to account using web login
gcloud auth application-default login





# Deploy Project into GCP via Terraform
## Run from CLI
terraform init 

terraform apply -auto-approve 

## Optional Commands:
terraform state list

terraform init -reconfigure #forces Terraform to reload your backend and reauthenticate using the new ADC.

# Use Multiple Workspaces (separate state file per workspace)
terraform workspace new dev

terraform workspace new prod

terraform workspace select dev








