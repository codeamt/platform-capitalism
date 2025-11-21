from fasthtml import rt
from fasthtml.common import Div, H1
from app.components import Layout, policy_controls
from app.simulation.environment import GLOBAL_ENVIRONMENT

@rt("/governance-lab")
def governance_lab_page():
    cfg = GLOBAL_ENVIRONMENT.policy_engine.config
    layout = Layout("Governance Lab")

    content = Div(
        H1("Governance Lab", cls="text-3xl font-bold mb-4"),
        policy_controls(cfg.mode, cfg),
        cls="space-y-4"
    )
    return layout.wrap(content, active_path="/governance-lab")