from fasthtml.common import Div, H1, Main
from app.components import agent_card
from app.simulation.environment import GLOBAL_ENVIRONMENT


def DashboardPage():
    content = Div(
        H1("Platform Simulation Dashboard", cls="text-3xl font-bold mb-4"),
        Div(
            *[agent_card(a) for a in GLOBAL_ENVIRONMENT.agents],
            cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
        ),
    )
    return Main(content)