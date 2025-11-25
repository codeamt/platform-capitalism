variable "region" {
  type    = string
  default = "us-east-1"
}

variable "service_name" {
  type    = string
  default = "platform-capitalism"
  description = "Name of the Lightsail container service"
}

variable "image" {
  description = "Container image for Lightsail"
  type        = string
  default     = "ghcr.io/YOUR_USERNAME/platform-capitalism:latest"
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Deployment environment"
}

variable "power" {
  type    = string
  default = "medium"  # micro, small, medium, large, xlarge
}

variable "scale" {
  type    = number
  default = 1
}