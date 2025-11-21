from fasthtml import fast_app, Mount, serve
from fasthtml.common import Div, StaticFiles

# Import pages so their routes register
import app.pages.dashboard
import app.pages.creator_studio
import app.pages.governance_lab
import app.pages.transparency
import app.pages.network
import app.pages.scenarios

# Import route modules
import app.routes.ui_mobile_menu
import app.routes.data_export
import app.routes.api_update_policy
import app.routes.api_load_scenario

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
    Mount("/", app.pages.dashboard.dashboard),
    Mount("/creator-studio", app.pages.creator_studio.creator_studio),
    Mount("/governance-lab", app.pages.governance_lab.governance_lab),
    Mount("/transparency", app.pages.transparency.transparency),
    Mount("/network", app.pages.network.network),
    Mount("/scenarios", app.pages.scenarios.scenarios),
    Mount("/api/update-policy", app.routes.api_update_policy.update_policy),
    Mount("/api/load-scenario", app.routes.api_load_scenario.load_scenario_route),
    Mount("/export/json", app.routes.data_export.export_json),
    Mount("/export/csv", app.routes.data_export.export_csv),
    Mount("/mobile-menu", app.routes.ui_mobile_menu.mobile_menu),
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