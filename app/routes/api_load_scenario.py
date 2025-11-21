from fasthtml import APIRouter
from fasthtml.common import Redirect
from app.simulation.scenarios import load_scenario, ALL_SCENARIOS
from app.simulation.environment import GLOBAL_ENVIRONMENT

rt = APIRouter()

@rt("/scenarios/load", methods=["POST"])
def load_scenario_route(request):
    scenario_name = request.form.get("scenario")

    if scenario_name not in ALL_SCENARIOS:
        return Redirect("/scenarios")

    load_scenario(GLOBAL_ENVIRONMENT, scenario_name)
    return Redirect("/scenarios")