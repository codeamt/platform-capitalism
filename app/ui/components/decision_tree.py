from fasthtml.common import Div, H3, Pre

def decision_tree(agent):
    return Div(
        H3("Decision Trace", cls="font-semibold"),
        Pre(str(agent.decision_trace or "No decisions yet."), cls="text-xs bg-gray-900 text-white p-2 rounded overflow-x-auto"),
        cls="mt-2"
    )