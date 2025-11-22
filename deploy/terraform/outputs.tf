output "lightsail_service_name" {
  value = aws_lightsail_container_service.simulation.name
}

output "lightsail_public_url" {
  value = aws_lightsail_container_service.simulation.url
}