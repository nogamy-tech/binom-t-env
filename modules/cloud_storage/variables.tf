variable "project_id" {
  type = string
}

variable "name" {
  type = string
}

variable "location" {
  type = string
}

variable "log_bucket_name" {
  type = string
  default = "t-binom"
}
variable "folder_names" {
  type = list(string)
  default = [ "Shikun/SiyuaBediyur/Upload", "Shikun/SiyuaBediyur/Download" ]
}