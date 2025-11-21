from fasthtml.common import Div, H2, P

def agent_card(agent):
    p = agent.profile
    return Div(
        H2(f"Agent {p.id}", cls="text-xl font-bold"),
        P(f"Current State: {p.current_state.name}"),
        P(f"Strategy: {p.strategy}"),
        P(f"Arousal: {p.arousal_level:.2f}"),
        P(f"Burnout: {p.burnout:.2f}"),
        cls="p-4 border rounded bg-white dark:bg-gray-800 shadow"
    )