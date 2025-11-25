import os
from fasthtml.common import fast_app, serve, Div
from monsterui.all import *

# API routes
from routes.api_update_policy import rt as update_policy_rt
from routes.api_load_scenario import rt as load_scenario_rt
from routes.data_export import rt as data_export_rt

# Page routes
from routes.dashboard import rt as dashboard_rt
from routes.governance_lab import rt as governance_lab_rt
from simulation import *
from ui import *


# Simulation environment & agent bootstrapping
from simulation.environment import GLOBAL_ENVIRONMENT
from simulation.agents.agent import Agent
from simulation.agents.profile import AgentProfile
from simulation.scenarios import load_scenario


def bootstrap_simulation(env, num_agents=5, default_scenario="Creator-First Platform"):
    """Initialize demo agents and load default scenario.
    
    Args:
        env: Environment instance to bootstrap
        num_agents: Number of demo agents to create
        default_scenario: Name of scenario to load initially
    """
    if not env.agents:
        env.agents.extend(
            [Agent(AgentProfile(id=i)) for i in range(num_agents)]
        )
        # Load default scenario to apply initial agent traits
        load_scenario(env, default_scenario)


# Bootstrap simulation on startup (only if no agents present)
bootstrap_simulation(GLOBAL_ENVIRONMENT)

# Create FastHTML app
# Secret key from environment variable for security (None is acceptable for dev)
app, rt = fast_app(hdrs=Theme.slate.headers(), secret_key=os.getenv("SECRET_KEY"))

# Register all APIRouters with the app using FastHTML's .to_app() method
for router in [
    # API routes
    update_policy_rt,
    load_scenario_rt,
    data_export_rt,
    # Page routes
    dashboard_rt,
    governance_lab_rt,
]:
    router.to_app(app)


# Health-check endpoint
@rt("/health") 
def health():
    return {"status": "ok"}

# Dev root fallback
@rt("/dev", methods=["GET"])
def dev_root():
    return Div("App is running — check the dashboard at /.")

# Note: /api/tick and /api/reset are now in api_update_policy.py

# Entry for launching
if __name__ == "__main__":
    serve()
    
    ''' Or in production 
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )
    '''