from fasthtml import fast_app, Mount, serve
from fasthtml.common import Div, StaticFiles

# Import route modules
import app.routes.ui_mobile_menu
import app.routes.data_export
import app.routes.api_update_policy
import app.routes.api_load_scenario
import app.routes.dashboard
import app.routes.creator_studio
import app.routes.governance_lab
import app.routes.network
import app.routes.scenarios

# Simulation environment & agent bootstrapping
from app.simulation.environment import GLOBAL_ENVIRONMENT
from app.simulation.agents.agent import Agent
from app.simulation.agents.profile import AgentProfile

# If no agents present (fresh start), initialize demo agents
if not GLOBAL_ENVIRONMENT.agents:
    GLOBAL_ENVIRONMENT.agents.extend(
        [Agent(AgentProfile(id=i)) for i in range(5)]
    )

app, rt = fast_app(routes=[
    Mount("/api/update-policy", app.routes.api_update_policy.rt),
    Mount("/api/load-scenario", app.routes.api_load_scenario.rt),
    Mount("/export/json", app.routes.data_export.rt),
    Mount("/mobile-menu", app.routes.ui_mobile_menu.rt),
    Mount("/dashboard", app.routes.dashboard.rt),
    Mount("/creator-studio", app.routes.creator_studio.rt),
    Mount("/governance-lab", app.routes.governance_lab.rt),
    Mount("/network", app.routes.network.rt),
    Mount("/scenarios", app.routes.scenarios.rt),
], 
static_files=StaticFiles(directory="static", html=False),
)


# Health-check endpoint
@rt("/health") 
def health():
    return {"status": "ok"}

# Tick endpoint for simulation control
@rt("/tick", method="POST")
def tick():
    GLOBAL_ENVIRONMENT.tick()
    return {
        "status": "ticked",
        "events": GLOBAL_ENVIRONMENT.last_tick_explanations
    }

# Dev root fallback
@rt("/dev", method="GET")
def dev_root():
    return Div("App is running — check the dashboard at /.")

# Entry for launching
if __name__ == "__main__":
    serve()
    
    ''' Or in production 
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )
    '''