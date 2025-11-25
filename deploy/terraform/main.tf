provider "aws" {
  region = var.region
}

resource "aws_lightsail_container_service" "simulation" {
  name        = var.service_name
  power       = var.power  # micro, small, medium, large, xlarge
  scale       = var.scale  # Number of instances (1-20)
  is_disabled = false
  
  tags = {
    Project     = "Platform Capitalism Research"
    Environment = "production"
    ManagedBy   = "Terraform"
  }
}

resource "aws_lightsail_container_deployment" "deploy" {
  service_name = aws_lightsail_container_service.simulation.name

  container {
    container_name = "app"
    image          = var.image
    command        = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

    ports = {
      "8080" = "HTTP"
    }

    environment = {
      ENVIRONMENT = var.environment
      LOG_LEVEL   = "info"
      PORT        = "8080"
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