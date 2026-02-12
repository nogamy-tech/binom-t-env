## Prerequisites (Authentication)

Before running any Terraform commands, ensure you are authenticated with GCP. Run these two commands:

1. **Login to gcloud CLI:**
   ```powershell
   gcloud auth login
   ```
2. **Setup Application Default Credentials (ADC):**
   ```powershell
   gcloud auth application-default login
   ```

---

## Environment Toggle Steps

To switch environments, you need to update two files: `provider.tf` and `variables.tf`.

### 1. Update `provider.tf`
Toggle the comments for the followings resources based on your target environment:

#### **Datapro (Default)**
- **Project ID**: `dgt-gcp-cgov-d-datapro`
- **VPC Connector**: `...binom-sha-d-serverless`
- **Backend Bucket**: `d-datapro-iac`

#### **D-I (Development)**
- **Project ID**: `dgt-gcp-cgov-d-i-binom`
- **VPC Connector**: `...binom-dev-i-serverless`
- **Backend Bucket**: `d-i-binom-iac`

### 2. Update `variables.tf`
Toggle the `load_balancer_name` default value:
- **Datapro**: `lb-binom`
- **D-I**: `binom-lb-d-i`

---

## Load Balancer Routing Rules

| Host | Path | Backend Service |
|------|------|-----------------|
| `binom.dev.cgov.dgt.gcp.internal` | `/shomer-saf/StartJob/*` | `bs-document-start-job` |
| `binom.dev.cgov.dgt.gcp.internal` | `/shomer-saf/QueryGet/*` | `bs-document-query-get` |
| `binom.dev.cgov.dgt.gcp.internal` | `/shomer-saf/ProcessQuery/*` | `bs-document-process-query` |
| `binom.dev.cgov.dgt.gcp.internal` | `/shomer-saf/PreProcessing/*` | `bs-document-pre-processing` |
| `binom.dev.cgov.dgt.gcp.internal` | `/shomer-saf/PageProcessing/*` | `bs-document-page-processing` |

---

## Deployment Commands

After toggling the values in the files, run the following commands in order:

### 1. Initialize (Reconfigure)
Since you are switching between different GCS buckets for the state file, you **must** use the `-reconfigure` flag:
```powershell
terraform init -reconfigure
```

### 2. Plan (Optional but Recommended)
Verify what will be changed:
```powershell
terraform plan
```

### 3. Apply
Apply the changes to the selected environment:
```powershell
terraform apply -auto-approve
```

> [!IMPORTANT]
> Always double-check that you are in the correct directory and that your `gcloud` credentials are set to the correct project before running `terraform apply`.
