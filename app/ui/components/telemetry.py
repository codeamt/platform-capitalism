from fasthtml.common import Div, H3

def agent_telemetry(agent_id):
    return Div(
        H3(f"Telemetry for Agent {agent_id}", cls="font-semibold"),
        Div(f"[Telemetry data for Agent {agent_id} would appear here]", cls="text-sm text-gray-500"),
        cls="p-3 border rounded"
    )