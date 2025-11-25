from fasthtml.common import Div, H2, Table, Tr, Th, Td
from monsterui.all import Card, CardBody

def transparency_panel(cfg, events):
    return Card(
        CardBody(
            H2("🔍 Transparency Panel", cls="text-xl font-bold text-gray-100 mb-4"),
            Table(
                Tr(
                    Th("Metric", cls="text-left text-sm font-semibold text-gray-300 p-2"), 
                    Th("Value", cls="text-right text-sm font-semibold text-gray-300 p-2")
                ),
                Tr(
                    Td("Baseline Guarantee", cls="text-sm text-gray-400 p-2"), 
                    Td(f"{cfg.baseline_guarantee:.2f}", cls="text-sm text-gray-200 text-right p-2")
                ),
                # Monetary rewards section
                Tr(
                    Td("Base Payment (per post)", cls="text-sm text-gray-400 p-2 pt-4 font-semibold"), 
                    Td(f"{cfg.base_payment:.3f}", cls="text-sm text-gray-200 text-right p-2 pt-4")
                ),
                Tr(
                    Td("Quality Bonus Multiplier", cls="text-sm text-gray-400 p-2"), 
                    Td(f"{cfg.quality_bonus_multiplier:.2f}x", cls="text-sm text-gray-200 text-right p-2")
                ),
                Tr(
                    Td("Engagement Multiplier", cls="text-sm text-gray-400 p-2"), 
                    Td(f"{cfg.engagement_multiplier:.2f}x", cls="text-sm text-gray-200 text-right p-2")
                ),
                # CPM Economics section
                Tr(
                    Td("CPM Rate ($/1000 views)", cls="text-sm text-gray-400 p-2 pt-4 font-semibold"), 
                    Td(f"${cfg.cpm_rate:.2f}", cls="text-sm text-gray-200 text-right p-2 pt-4")
                ),
                Tr(
                    Td("Avg Views per Post", cls="text-sm text-gray-400 p-2"), 
                    Td(f"{cfg.avg_views_per_post:,}", cls="text-sm text-gray-200 text-right p-2")
                ),
                Tr(
                    Td("Est. Earnings (10 posts)", cls="text-sm text-gray-400 p-2 italic"), 
                    Td(f"${(10 * cfg.avg_views_per_post / 1000.0 * cfg.cpm_rate):.2f}", cls="text-sm text-green-400 text-right p-2")
                ),
                Tr(
                    Td("Quality Weight", cls="text-sm text-gray-400 p-2"), 
                    Td(f"{cfg.quality_weight:.2f}", cls="text-sm text-gray-200 text-right p-2")
                ),
                Tr(
                    Td("Diversity Weight", cls="text-sm text-gray-400 p-2"), 
                    Td(f"{cfg.diversity_weight:.2f}", cls="text-sm text-gray-200 text-right p-2")
                ),
                Tr(
                    Td("Consistency Weight", cls="text-sm text-gray-400 p-2"), 
                    Td(f"{cfg.consistency_weight:.2f}", cls="text-sm text-gray-200 text-right p-2")
                ),
                Tr(
                    Td("Volume Weight", cls="text-sm text-gray-400 p-2"), 
                    Td(f"{cfg.volume_weight:.2f}", cls="text-sm text-gray-200 text-right p-2")
                ),
                Tr(
                    Td("Volatility Weight", cls="text-sm text-gray-400 p-2"), 
                    Td(f"{cfg.volatility_weight:.2f}", cls="text-sm text-gray-200 text-right p-2")
                ),
                cls="w-full border-collapse mb-4"
            ),
            Div(f"📊 Last Tick Explanations: {len(events)} events", cls="text-sm text-gray-400")
        ),
        cls="bg-gray-800 border-gray-700"
    )