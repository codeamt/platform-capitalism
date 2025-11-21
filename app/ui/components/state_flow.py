from fasthtml.common import Div, H3

def compressed_state_flow(agent):
    return Div(
        H3("State Flow Timeline", cls="font-semibold"),
        Div(f"[State transitions for agent {agent.profile.id}]", cls="text-xs text-gray-500"),
        cls="p-3 border rounded"
    )