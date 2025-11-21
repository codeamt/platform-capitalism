from fasthtml.common import Div, H1, Main
from app.components import network_graph


def NetworkPage():
    dummy_graph = {
        "nodes": [{"id": i, "group": 1} for i in range(5)],
        "links": [{"source": 0, "target": i} for i in range(1, 5)],
    }

    content = Div(
        H1("Network Graph", cls="text-3xl font-bold mb-4"),
        network_graph(dummy_graph),
        cls="space-y-4"
    )
    return Main(content)