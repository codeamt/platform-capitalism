from fasthtml.common import Div, H2, H3, P, Span, Canvas, Script
from monsterui.all import Card, CardBody
import json

def system_health_card(summary, history=None):
    """Display overall system health metrics - key research outcomes.
    
    Shows the comparative health of the creator ecosystem under
    different reinforcement strategies (differential vs intermittent).
    
    Args:
        summary: Current state summary dict
        history: Optional history dict with time-series data for charts
    """
    health_score = summary.get("system_health_score", 0)
    regime = summary.get("current_regime", "unknown")
    history = history or {}
    
    # Health score color coding
    if health_score > 0.7:
        health_color = "text-green-600"
        health_bg = "bg-green-50"
        health_status = "🌟 Thriving"
    elif health_score > 0.5:
        health_color = "text-yellow-600"
        health_bg = "bg-yellow-50"
        health_status = "⚡ Stressed"
    else:
        health_color = "text-red-600"
        health_bg = "bg-red-50"
        health_status = "⚠️ Crisis"
    
    # Regime badge
    regime_badges = {
        "differential": ("🌱 Differential", "bg-green-100 text-green-800"),
        "intermittent": ("🎰 Intermittent", "bg-red-100 text-red-800"),
        "hybrid": ("🔀 Hybrid", "bg-blue-100 text-blue-800"),
    }
    regime_text, regime_class = regime_badges.get(regime, (regime, "bg-gray-100 text-gray-800"))
    
    return Card(
        CardBody(
            # Header
            Div(
                H2("System Health", cls="text-2xl font-bold text-gray-100"),
                Span(regime_text, cls=f"px-3 py-1 rounded-full text-sm font-semibold {regime_class}"),
                cls="flex justify-between items-center mb-4"
            ),
            
            # Overall Health Score
            Div(
                H3("Overall Health Score", cls="text-sm font-semibold text-gray-300 mb-2"),
                Div(
                    Span(f"{health_score:.2f}", cls=f"text-4xl font-bold {health_color}"),
                    Span(health_status, cls=f"ml-3 text-lg font-semibold {health_color}"),
                    cls="flex items-center"
                ),
                Div(
                    Div(cls=f"h-3 rounded {health_color.replace('text-', 'bg-')}", 
                        style=f"width: {int(health_score * 100)}%"),
                    cls="w-full bg-gray-200 rounded h-3 mt-2"
                ),
                cls=f"p-4 rounded-lg {health_bg} mb-4"
            ),
            
            # Key Metrics Grid
            Div(
                _health_metric(
                    "Avg Burnout",
                    summary.get("avg_burnout", 0),
                    "🔥",
                    "Lower is better",
                    inverse=False
                ),
                _health_metric(
                    "Avg Addiction",
                    summary.get("avg_addiction", 0),
                    "🎰",
                    "Lower is better",
                    inverse=False
                ),
                _health_metric(
                    "Avg Resilience",
                    summary.get("avg_resilience", 0),
                    "💪",
                    "Higher is better",
                    inverse=True
                ),
                _health_metric(
                    "Burnout Rate",
                    summary.get("burnout_rate", 0),
                    "📊",
                    "% in burnout state",
                    inverse=False,
                    is_percentage=True
                ),
                cls="grid grid-cols-2 gap-4 mb-4"
            ),
            
            # Health Trend Chart (if history available)
            _health_trend_chart(history) if history.get("ticks") else None,
            
            # Reward Characteristics
            Div(
                H3("Reward Characteristics", cls="text-sm font-semibold text-gray-300 mb-2"),
                Div(
                    _small_metric("Predictability", summary.get("reward_predictability", 0), "📈"),
                    _small_metric("Variance", summary.get("reward_variance", 0), "📊"),
                    _small_metric("Transparency", summary.get("transparency", 0), "🔍"),
                    _small_metric("Baseline Guarantee", summary.get("baseline_guarantee", 0), "🛡️"),
                    cls="grid grid-cols-2 gap-2"
                ),
                cls="pt-4 border-t border-gray-700"
            )
        ),
        cls="bg-gray-800 border-gray-700"
    )

def _health_metric(label, value, emoji, description, inverse=False, is_percentage=False):
    """Display a health metric with color coding."""
    # Determine color
    if inverse:  # Higher is better
        color = "text-green-600" if value > 0.6 else "text-yellow-600" if value > 0.4 else "text-red-600"
    else:  # Lower is better
        color = "text-green-600" if value < 0.4 else "text-yellow-600" if value < 0.7 else "text-red-600"
    
    display_value = f"{int(value * 100)}%" if is_percentage else f"{value:.2f}"
    
    return Div(
        Div(
            Span(emoji, cls="text-2xl"),
            cls="mb-2"
        ),
        P(label, cls="text-sm font-semibold text-gray-300"),
        P(display_value, cls=f"text-2xl font-bold {color}"),
        P(description, cls="text-xs text-gray-400"),
        cls="p-3 bg-gray-700 rounded-lg"
    )

def _small_metric(label, value, emoji):
    """Small metric display."""
    return Div(
        Span(f"{emoji} {label}", cls="text-xs font-medium text-gray-300"),
        Span(f"{value:.2f}", cls="text-sm font-bold text-gray-100"),
        cls="flex justify-between items-center p-2 bg-gray-700 rounded"
    )

def _health_trend_chart(history):
    """Render health metrics trend chart using Chart.js."""
    if not history.get("ticks"):
        return None
    
    # Prepare data for Chart.js
    ticks = history.get("ticks", [])
    health_scores = history.get("health_score", [])
    burnout = history.get("avg_burnout", [])
    addiction = history.get("avg_addiction", [])
    resilience = history.get("avg_resilience", [])
    
    return Div(
        H3("📈 Health Trend (Last 20 Ticks)", cls="text-sm font-semibold text-gray-300 mb-2 mt-4"),
        Canvas(id="healthTrendChart", style="height: 200px; max-height: 200px;"),
        Script(f"""
            setTimeout(function() {{
                const ctx = document.getElementById('healthTrendChart');
                if (!ctx || !window.Chart) return;
                
                // Destroy existing chart if it exists
                const existingChart = Chart.getChart('healthTrendChart');
                if (existingChart) {{
                    existingChart.destroy();
                }}
                
                new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: {json.dumps(ticks)},
                        datasets: [
                            {{
                                label: 'Health Score',
                                data: {json.dumps(health_scores)},
                                borderColor: 'rgb(34, 197, 94)',
                                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                                borderWidth: 2,
                                tension: 0.3,
                                fill: true
                            }},
                            {{
                                label: 'Burnout',
                                data: {json.dumps(burnout)},
                                borderColor: 'rgb(239, 68, 68)',
                                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                                borderWidth: 2,
                                tension: 0.3,
                                fill: false
                            }},
                            {{
                                label: 'Addiction',
                                data: {json.dumps(addiction)},
                                borderColor: 'rgb(249, 115, 22)',
                                backgroundColor: 'rgba(249, 115, 22, 0.1)',
                                borderWidth: 2,
                                tension: 0.3,
                                fill: false
                            }},
                            {{
                                label: 'Resilience',
                                data: {json.dumps(resilience)},
                                borderColor: 'rgb(59, 130, 246)',
                                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                borderWidth: 2,
                                tension: 0.3,
                                fill: false
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'bottom'
                            }},
                            tooltip: {{
                                mode: 'index',
                                intersect: false
                            }}
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                max: 1,
                                title: {{
                                    display: true,
                                    text: 'Score (0-1)'
                                }}
                            }},
                            x: {{
                                title: {{
                                    display: true,
                                    text: 'Tick'
                                }}
                            }}
                        }}
                    }}
                }});
            }}, 100);
        """),
        cls="pt-4 border-t mb-4"
    )

# Keep old function for backwards compatibility
def agent_telemetry(agent_id):
    return Div(
        H3(f"Telemetry for Agent {agent_id}", cls="font-semibold"),
        Div(f"[Telemetry data for Agent {agent_id} would appear here]", cls="text-sm text-gray-500"),
        cls="p-3 border rounded"
    )