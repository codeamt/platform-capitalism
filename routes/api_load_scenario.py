from fasthtml.common import APIRouter
from simulation.scenarios import load_scenario, ALL_SCENARIOS
from simulation.environment import GLOBAL_ENVIRONMENT
from ui.pages.dashboard import DashboardPage
from ui.pages.governance_lab import GovernanceLabPage

rt = APIRouter()

@rt("/scenarios/load", methods=["POST"])
def load_scenario_route(scenario: str, source: str = "dashboard"):
    """Load a scenario and return updated page content.
    
    Called via HTMX from scenario_selector buttons.
    Returns the appropriate page based on source parameter.
    
    Args:
        scenario: Name of the scenario to load
        source: Either 'dashboard' or 'governance' to determine which page to return
    """
    if scenario in ALL_SCENARIOS:
        load_scenario(GLOBAL_ENVIRONMENT, scenario)
    
    # Return the appropriate page based on where the request came from
    if source == "governance":
        return GovernanceLabPage()
    else:
        return DashboardPage()