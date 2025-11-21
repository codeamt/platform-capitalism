from fasthtml.common import Div, Script, H3

def network_graph(graph):
    return Div(
        H3("Network Graph", cls="text-xl font-bold mb-2"),
        Div(id="network-graph", cls="w-full h-64 border rounded"),
        Script(src="https://d3js.org/d3.v7.min.js"),
        Script(f"console.log('Network graph loaded', {graph});"),
        cls="p-4 border rounded"
    )