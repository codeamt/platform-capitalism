from fasthtml.common import Div, H2, Table, Tr, Th, Td

def transparency_panel(cfg, events):
    return Div(
        H2("Transparency Panel", cls="text-2xl font-bold mb-4"),
        Table(
            Tr(Th("Metric"), Th("Value")),
            Tr(Td("Quality Weight"), Td(cfg.quality_weight)),
            Tr(Td("Diversity Weight"), Td(cfg.diversity_weight)),
            Tr(Td("Consistency Weight"), Td(cfg.consistency_weight)),
            Tr(Td("Volatility Weight"), Td(cfg.volatility_weight)),
            cls="table-auto border mb-4"
        ),
        Div(f"Last Tick Explanations: {len(events)} events", cls="text-sm text-gray-500"),
        cls="p-4 border rounded"
    )