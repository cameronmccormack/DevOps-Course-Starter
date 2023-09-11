variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "github_client_id" {
  sensitive = true
}

variable "github_secret" {
  sensitive = true
}

variable "flask_secret" {
    sensitive = true
}

variable "loggly_token" {
    sensitive = true
}
