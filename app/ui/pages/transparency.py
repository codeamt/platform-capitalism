from fasthtml import rt
from fasthtml.common import Div, H1
from app.components import Layout, transparency_panel
from app.simulation.environment import GLOBAL_ENVIRONMENT

@rt("/transparency")
def transparency_page():
    layout = Layout("Transparency")
    cfg = GLOBAL_ENVIRONMENT.policy_engine.config
    events = GLOBAL_ENVIRONMENT.last_tick_explanations

    content = Div(
        H1("Transparency Dashboard", cls="text-3xl font-bold mb-4"),
        transparency_panel(cfg, events),
        cls="space-y-4"
    )
    return layout.wrap(content, active_path="/transparency")