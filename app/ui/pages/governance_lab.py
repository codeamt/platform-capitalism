from fasthtml.common import Div, H1, Main
from app.components import policy_controls
from app.simulation.environment import GLOBAL_ENVIRONMENT


def GovernanceLabPage():
    cfg = GLOBAL_ENVIRONMENT.policy_engine.config
    content = Div(
        H1("Governance Lab", cls="text-3xl font-bold mb-4"),
        policy_controls(cfg.mode, cfg),
        cls="space-y-4"
    )
    return Main(content)