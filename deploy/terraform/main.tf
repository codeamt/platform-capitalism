provider "aws" {
  region = var.region
}

resource "aws_lightsail_container_service" "simulation" {
  name        = var.service_name
  power       = var.power
  scale       = var.scale
  is_disabled = false
}

resource "aws_lightsail_container_deployment" "deploy" {
  service_name = aws_lightsail_container_service.simulation.name

  container {
    container_name = "app"
    image          = var.image

    ports = {
      "8080" = "HTTP"
    }

    environment = {
      ENVIRONMENT       = "production"
      LOG_LEVEL         = "info"
      SECRET_KEY        = var.secret_key
      DB_URL            = var.db_url
      AWS_DEFAULT_REGION = var.region
    }
  }

  public_endpoint {
    container_name = "app"
    container_port = 8080

    health_check {
      healthy_threshold   = 2
      unhealthy_threshold = 2
      timeout_seconds     = 5
      interval_seconds    = 10
      path                = "/health"
    }
  }
}