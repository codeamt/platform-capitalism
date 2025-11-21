from fasthtml.common import Div, H3, Button

def simulation_replay_controls():
    return Div(
        H3("Simulation Replay Controls", cls="text-lg font-bold mb-2"),
        Button("Play", cls="px-3 py-1 bg-blue-600 text-white rounded mr-2"),
        Button("Pause", cls="px-3 py-1 bg-gray-600 text-white rounded mr-2"),
        Button("Step", cls="px-3 py-1 bg-green-600 text-white rounded"),
        cls="mb-4"
    )

def simulation_replay_view(agent):
    return Div(
        H3(f"Replay for Agent {agent.profile.id}", cls="text-sm font-semibold mb-1"),
        Div(f"[Replay view for {agent.profile.id} - history length: {len(agent.history)}]", cls="text-xs text-gray-500"),
        cls="p-3 border rounded"
    )