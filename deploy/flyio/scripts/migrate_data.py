import json
import datetime
from pathlib import Path
from app.simulation import get_env
from app.utils.logger import logger

def backup_simulation_state():
    """Create timestamped backup of simulation state"""
    env = get_env()
    backup_dir = Path("/data/backups")
    backup_dir.mkdir(exist_ok=True)

    state = {
        "version": "1.1",
        "tick": env.tick,
        "agents": [a.to_dict() for a in env.agents],
        "platform": env.platform.config.dict(),
        "metrics": env.metrics.history
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"sim_state_{timestamp}.json"

    with open(backup_path, "w") as f:
        json.dump(state, f, indent=2)

    logger.info(f"Backup created at {backup_path}")
    return backup_path

def restore_backup(backup_path: str):
    """Restore simulation from backup"""
    with open(backup_path) as f:
        state = json.load(f)

    env = get_env()
    env.reset()

    # Version-specific restoration logic
    if state.get("version") == "1.1":
        env.tick = state["tick"]
        env.metrics.history = state["metrics"]
        # Additional restoration logic

    logger.info(f"Restored from {backup_path}")