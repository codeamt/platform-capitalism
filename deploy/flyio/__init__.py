"""
Platform Capitalism Simulator Deployment Module

Handles:
- Fly.io deployment configurations
- Docker container optimizations
- CI/CD pipeline integrations
- Health checks and monitoring
"""
from pathlib import Path
from typing import Optional
import json
from app.config import SETTINGS

DEPLOY_DIR = Path(__file__).parent

class DeploymentConfig:
    """Centralized deployment configuration"""
    def __init__(self):
        self.platform = "fly"
        self.region = "ord"  # Chicago
        self.min_instances = 1
        self.max_instances = 3
        self.cpu_cores = 1
        self.memory_mb = 1024

    @property
    def fly_config_path(self) -> Path:
        return DEPLOY_DIR / "fly.toml"

    @property
    def dockerfile_path(self) -> Path:
        return DEPLOY_DIR / "Dockerfile"

    def validate(self) -> bool:
        """Check all deployment files exist"""
        return all([
            self.fly_config_path.exists(),
            self.dockerfile_path.exists()
        ])

config = DeploymentConfig()