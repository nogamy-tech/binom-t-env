resource "google_project_service" "model_armor" {
  project = var.project_id
  service            = "modelarmor.googleapis.com"
  disable_on_destroy = false
}


resource "google_model_armor_template" "armor_template" {
    location = "europe-west1"
    template_id = "armor_template"
    project = var.project_id

    filter_config {
        malicious_uri_filter_settings {
            filter_enforcement = "DISABLED"
        }
        rai_settings {
            rai_filters {
                filter_type = "HATE_SPEECH"
                confidence_level = "HIGH"
            }
            rai_filters {
                filter_type = "SEXUALLY_EXPLICIT"
                confidence_level = "HIGH"
            }
            rai_filters {
                filter_type = "HARASSMENT"
                confidence_level = "HIGH"
            }
            rai_filters {
                filter_type = "DANGEROUS"
                confidence_level = "HIGH"
            }
        }
        sdp_settings {
            basic_config {
                filter_enforcement = "ENABLED"
            }
        }
        pi_and_jailbreak_filter_settings {
            filter_enforcement =  "ENABLED"
            confidence_level = "HIGH"
        }
    }

    template_metadata {
        log_sanitize_operations = true
        multi_language_detection {
            enable_multi_language_detection  = true
        }
    }

    depends_on = [ google_project_service.model_armor ]
}

output "id_template" {
    value = google_model_armor_template.armor_template.id
}