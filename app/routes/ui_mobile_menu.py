from fasthtml import APIRouter
from fasthtml.common import Div, A

rt = APIRouter()

@rt("/mobile-menu")
def mobile_menu():
    return Div(
        A("Dashboard", href="/", cls="block p-2"),
        A("Creator Studio", href="/creator-studio", cls="block p-2"),
        A("Governance Lab", href="/governance-lab", cls="block p-2"),
        A("Transparency", href="/transparency", cls="block p-2"),
        A("Network", href="/network", cls="block p-2"),
        A("Scenarios", href="/scenarios", cls="block p-2"),
        cls="space-y-2 p-4 bg-gray-100 dark:bg-gray-800 rounded shadow"
    )