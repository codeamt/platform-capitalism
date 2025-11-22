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

# If no agents present (fresh start), initialize demo agents
if not GLOBAL_ENVIRONMENT.agents:
    GLOBAL_ENVIRONMENT.agents.extend(
        [Agent(AgentProfile(id=i)) for i in range(5)]
    )
    # Load default scenario to apply initial agent traits
    load_scenario(GLOBAL_ENVIRONMENT, "Creator-First Platform")

# Create FastHTML app
app, rt = fast_app(hdrs=Theme.slate.headers(),secret_key=None)

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