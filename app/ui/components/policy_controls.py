from fasthtml.common import Div, H3, Form, Input, Label, Button

def policy_controls(mode, cfg):
    return Div(
        H3(f"Policy Controls — Mode: {mode}", cls="text-xl font-bold mb-2"),
        Form(
            Label("Quality Weight"),
            Input(name="quality_weight", value=cfg.quality_weight, type="number", step="0.01"),
            Label("Diversity Weight"),
            Input(name="diversity_weight", value=cfg.diversity_weight, type="number", step="0.01"),
            Label("Consistency Weight"),
            Input(name="consistency_weight", value=cfg.consistency_weight, type="number", step="0.01"),
            Label("Break Reward"),
            Input(name="break_reward", value=cfg.break_reward, type="number", step="0.01"),
            Button("Update", cls="mt-2 px-3 py-1 bg-blue-600 text-white rounded"),
            action="/api/update-policy", method="post",
            cls="space-y-2"
        ),
        cls="p-4 border rounded shadow"
    )