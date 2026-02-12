# VM instance not used - commented out to pass KICS security scan
# resource "google_compute_instance" "tf-instance-1" {
#   name         = "tf-instance-1"
#   machine_type = "e2-standard-2"
#   zone         = var.zone

#   boot_disk {
#     initialize_params {
#       image = "debian-cloud/debian-11"
#     }
#   }

#   network_interface {
#     network    = var.network
#     subnetwork = var.subnet_01
#   }

#   metadata_startup_script = <<-EOT
#     #!/bin/bash
#   EOT

#   allow_stopping_for_update = true
# }

# resource "google_compute_instance" "tf-instance-2" {
#   name         = "tf-instance-2"
#   machine_type = "e2-standard-2"
#   zone         = var.zone

#   boot_disk {
#     initialize_params {
#       image = "debian-cloud/debian-11"
#     }
#   }

#   network_interface {
#     network    = var.network
#     subnetwork = var.subnet_02
#   }

#   metadata_startup_script = <<-EOT
#     #!/bin/bash
#   EOT

#   allow_stopping_for_update = true
# }
