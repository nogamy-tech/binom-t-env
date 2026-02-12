output "function_name" {
  value = google_cloudfunctions2_function.python_function.name
}

output "function_uri" {
  value = google_cloudfunctions2_function.python_function.url
}
