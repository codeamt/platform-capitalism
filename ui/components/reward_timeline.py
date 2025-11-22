from fasthtml.common import Div, H2, H3, P, Span, Canvas, Script
from monsterui.all import Card, CardBody
import json
import statistics

def reward_timeline(history, summary):
    """Display reward distribution and variance over time.
    
    Demonstrates the core research question: differential reinforcement
    provides predictable rewards, while intermittent creates high variance.
    
    Args:
        history: Environment history dict with time-series data
        summary: Current state summary for context
    """
    if not history.get("ticks") or not history.get("avg_reward"):
        return Card(
            CardBody(
                H2("📊 Reward Timeline", cls="text-xl font-bold mb-4 text-gray-100"),
                P("Run simulation ticks to see reward patterns", cls="text-gray-400")
            ),
            cls="bg-gray-800 border-gray-700"
        )
    
    ticks = history.get("ticks", [])
    avg_rewards = history.get("avg_reward", [])
    regime = summary.get("current_regime", "unknown")
    
    # Calculate variance and predictability
    if len(avg_rewards) > 1:
        variance = statistics.variance(avg_rewards)
        mean_reward = statistics.mean(avg_rewards)
        std_dev = statistics.stdev(avg_rewards)
        coefficient_of_variation = (std_dev / mean_reward) if mean_reward > 0 else 0
    else:
        variance = 0
        mean_reward = avg_rewards[0] if avg_rewards else 0
        std_dev = 0
        coefficient_of_variation = 0
    
    # Regime badge
    regime_badges = {
        "differential": ("🌱 Differential", "bg-green-100 text-green-800", "Low variance, predictable"),
        "intermittent": ("🎰 Intermittent", "bg-red-100 text-red-800", "High variance, unpredictable"),
        "hybrid": ("🔀 Hybrid", "bg-blue-100 text-blue-800", "Mixed variance"),
    }
    regime_text, regime_class, regime_desc = regime_badges.get(regime, (regime, "bg-gray-100 text-gray-800", ""))
    
    return Card(
        CardBody(
            # Header
            Div(
                H2("📊 Reward Timeline", cls="text-2xl font-bold text-gray-100"),
                Span(regime_text, cls=f"px-3 py-1 rounded-full text-sm font-semibold {regime_class}"),
                cls="flex justify-between items-center mb-2"
            ),
            P(regime_desc, cls="text-sm text-gray-400 mb-4"),
            
            # Statistics Grid
            Div(
                _stat_box("Mean Reward", f"{mean_reward:.2f}", "📈"),
                _stat_box("Variance", f"{variance:.3f}", "📊"),
                _stat_box("Std Dev", f"{std_dev:.2f}", "📉"),
                _stat_box("CV", f"{coefficient_of_variation:.2f}", "🎯", 
                         subtitle="Coefficient of Variation"),
                cls="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4"
            ),
            
            # Reward Timeline Chart
            _reward_chart(ticks, avg_rewards, mean_reward, regime),
            
            # Interpretation
            _interpretation_box(coefficient_of_variation, regime)
        ),
        cls="bg-gray-800 border-gray-700"
    )

def _stat_box(label, value, emoji, subtitle=None):
    """Display a statistics box."""
    return Div(
        Span(emoji, cls="text-2xl mb-1"),
        P(label, cls="text-xs font-medium text-gray-300"),
        P(value, cls="text-lg font-bold text-gray-100"),
        P(subtitle, cls="text-xs text-gray-400") if subtitle else None,
        cls="p-3 bg-gray-700 rounded-lg text-center"
    )

def _reward_chart(ticks, rewards, mean_reward, regime):
    """Render reward timeline chart with mean line."""
    # Color based on regime
    color_map = {
        "differential": "rgb(34, 197, 94)",
        "intermittent": "rgb(239, 68, 68)",
        "hybrid": "rgb(59, 130, 246)",
    }
    line_color = color_map.get(regime, "rgb(107, 114, 128)")
    
    # Mean line data
    mean_line = [mean_reward] * len(ticks)
    
    return Div(
        H3("Reward Distribution Over Time", cls="text-sm font-semibold text-gray-300 mb-2"),
        Canvas(id="rewardTimelineChart", style="height: 250px;"),
        Script(f"""
            (function() {{
                const ctx = document.getElementById('rewardTimelineChart');
                if (!ctx || !window.Chart) return;
                
                new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: {json.dumps(ticks)},
                        datasets: [
                            {{
                                label: 'Actual Rewards',
                                data: {json.dumps(rewards)},
                                borderColor: '{line_color}',
                                backgroundColor: '{line_color.replace('rgb', 'rgba').replace(')', ', 0.1)')}',
                                borderWidth: 2,
                                tension: 0.3,
                                fill: true,
                                pointRadius: 3,
                                pointHoverRadius: 5
                            }},
                            {{
                                label: 'Mean Reward',
                                data: {json.dumps(mean_line)},
                                borderColor: 'rgb(156, 163, 175)',
                                borderWidth: 2,
                                borderDash: [5, 5],
                                fill: false,
                                pointRadius: 0
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
                                title: {{
                                    display: true,
                                    text: 'Average Reward'
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
            }})();
        """),
        cls="mb-4"
    )

def _interpretation_box(cv, regime):
    """Display interpretation of the reward pattern."""
    # Determine interpretation based on CV and regime
    if regime == "differential":
        if cv < 0.3:
            icon = "✅"
            color = "bg-green-50 border-green-300 text-green-800"
            title = "Healthy Pattern"
            message = "Low variance indicates predictable, sustainable rewards. Creators can plan and maintain work-life balance."
        else:
            icon = "⚠️"
            color = "bg-yellow-50 border-yellow-300 text-yellow-800"
            title = "Unexpected Variance"
            message = "Differential reinforcement should have low variance. Check policy configuration."
    elif regime == "intermittent":
        if cv > 0.5:
            icon = "🚨"
            color = "bg-red-50 border-red-300 text-red-800"
            title = "High Variance - Addictive Pattern"
            message = "High variance creates 'slot machine' effect, driving compulsive behavior and burnout. This is exploitative."
        else:
            icon = "⚠️"
            color = "bg-yellow-50 border-yellow-300 text-yellow-800"
            title = "Lower Than Expected Variance"
            message = "Intermittent reinforcement typically shows high variance. Current pattern may not fully demonstrate the effect."
    else:  # hybrid
        icon = "🔀"
        color = "bg-blue-50 border-blue-300 text-blue-800"
        title = "Mixed Pattern"
        message = f"Hybrid mode shows moderate variance (CV: {cv:.2f}). Balance between predictability and discovery."
    
    return Div(
        Div(
            Span(icon, cls="text-2xl mr-2"),
            Span(title, cls="font-bold text-lg"),
            cls="flex items-center mb-2"
        ),
        P(message, cls="text-sm"),
        cls=f"p-4 rounded-lg border-2 {color}"
    )