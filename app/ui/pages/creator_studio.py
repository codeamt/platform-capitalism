from fasthtml.common import Div, H1, Main
from app.components import agent_bio, decision_tree, compressed_state_flow
from app.simulation.environment import GLOBAL_ENVIRONMENT


def CreatorStudioPage():
    content = Div(
        H1("Creator Studio", cls="text-3xl font-bold mb-4"),
        agent_bio(a),
        decision_tree(a),
        compressed_state_flow(a),
        cls="space-y-4"
    )
    return Main(content)