from fasthtml import rt
from fasthtml.common import Div, H1
from app.components import Layout, network_graph

@rt("/network")
def network_page():
    layout = Layout("Network Graph")

    dummy_graph = {
        "nodes": [{"id": i, "group": 1} for i in range(5)],
        "links": [{"source": 0, "target": i} for i in range(1, 5)],
    }

    content = Div(
        H1("Network Graph", cls="text-3xl font-bold mb-4"),
        network_graph(dummy_graph),
        cls="space-y-4"
    )
    return layout.wrap(content, active_path="/network")