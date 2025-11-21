from fasthtml import rt
from fasthtml.common import Div, H1
from app.components import Layout, agent_bio, decision_tree, compressed_state_flow
from app.simulation.environment import GLOBAL_ENVIRONMENT

@rt("/creator-studio")
def creator_studio_page():
    layout = Layout("Creator Studio")
    a = GLOBAL_ENVIRONMENT.agents[0] if GLOBAL_ENVIRONMENT.agents else None

    content = Div(
        H1("Creator Studio", cls="text-3xl font-bold mb-4"),
        agent_bio(a),
        decision_tree(a),
        compressed_state_flow(a),
        cls="space-y-4"
    )
    return layout.wrap(content, active_path="/creator-studio")