from fasthtml.common import Div, H1, Main
from app.components import transparency_panel
from app.simulation.environment import GLOBAL_ENVIRONMENT


def TransparencyPage():
    cfg = GLOBAL_ENVIRONMENT.policy_engine.config
    events = GLOBAL_ENVIRONMENT.last_tick_explanations

    content = Div(
        H1("Transparency Dashboard", cls="text-3xl font-bold mb-4"),
        transparency_panel(cfg, events),
        cls="space-y-4"
    )
    return Main(content)
