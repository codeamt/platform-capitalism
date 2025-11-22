variable "region" {
  type    = string
  default = "us-east-1"
}

variable "service_name" {
  type    = string
  default = "platform-simulation"
}

variable "image" {
  description = "Container image for Lightsail"
  type        = string
}

variable "secret_key" {
  type        = string
  description = "App secret key"
}

variable "db_url" {
  type        = string
  description = "Database URL"
}

variable "power" {
  type    = string
  default = "medium"  # micro, small, medium, large, xlarge
}

variable "scale" {
  type    = number
  default = 1
}