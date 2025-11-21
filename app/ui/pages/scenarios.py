from fasthtml import rt
from fasthtml.common import Div, H1, Form, Select, Option, Button
from app.components import Layout
from app.simulation.scenarios import ALL_SCENARIOS, load_scenario
from app.simulation.environment import GLOBAL_ENVIRONMENT

@rt("/scenarios")
def scenarios_page():
    layout = Layout("Scenarios")

    options = [Option(name) for name in ALL_SCENARIOS.keys()]

    content = Div(
        H1("Scenarios", cls="text-3xl font-bold mb-4"),
        Form(
            Select(name="scenario", children=options),
            Button("Load Scenario", cls="mt-2 px-3 py-1 bg-blue-600 text-white rounded"),
            action="/scenarios/load", method="post",
            cls="space-y-2"
        ),
        cls="space-y-4"
    )
    return layout.wrap(content, active_path="/scenarios")