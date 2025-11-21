from fasthtml.common import Div, H3, P

def agent_bio(agent):
    p = agent.profile
    return Div(
        H3("Agent Bio", cls="font-semibold mb-2"),
        P(f"Resilience: {p.emotional_resilience:.2f}"),
        P(f"Addiction Drive: {p.addiction_drive:.2f}"),
        P(f"Diversity: {p.diversity:.2f}"),
        P(f"Consistency: {p.consistency:.2f}"),
        cls="p-3 bg-gray-50 dark:bg-gray-700 rounded"
    )