resource "google_storage_bucket_iam_binding" "sa-safe-binom-tst" {
  bucket = google_storage_bucket.storage_bucket.name
  role   = "roles/storage.objectUser"  
  members = [
    "serviceAccount:sa-safe-binom-tst@dgt-gcp-cgov-mng-sa-0.iam.gserviceaccount.com"
  ]
}


resource "google_storage_bucket" "storage_bucket" {
  project = var.project_id
  name = var.name
  location = var.location
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  logging {
    log_bucket = var.log_bucket_name
    log_object_prefix = "logs/"
  }
}
resource "google_storage_bucket_object" "empty_folder" {
  name   = "${var.folder_names[count.index]}/"
  content = " "
  bucket = google_storage_bucket.storage_bucket.name
  count = length(var.folder_names)
}
resource "null_resource" "delete_bucket_objects_1" {
  provisioner "local-exec" {
    command = "gcloud storage rm --recursive gs://binom-gcs-tst/Shikun/SiyuaBediyur/Download || true"
  }
}