from fasthtml.common import Div, H2, H3, P, Span, Canvas, Script
from monsterui.all import Card, CardBody
import json

def agent_card(agent):
    """Display agent with research-relevant metrics."""
    p = agent.profile
    
    # Health status color coding
    if p.burnout > 0.7 or p.addiction_drive > 0.7:
        status_color = "text-red-600"
        status_text = "⚠️ At Risk"
    elif p.burnout > 0.4 or p.addiction_drive > 0.5:
        status_color = "text-yellow-600"
        status_text = "⚡ Stressed"
    else:
        status_color = "text-green-600"
        status_text = "✓ Healthy"
    
    # Get strategy info
    strategy_info = agent.get_strategy_info()
    
    return Card(
        CardBody(
            # Header with status
            Div(
                H2(f"Agent {p.id}", cls="text-xl font-bold inline text-gray-100"),
                Span(status_text, cls=f"ml-2 text-sm font-semibold {status_color}"),
                cls="mb-3"
            ),
            
            # State & Strategy
            Div(
                P(f"🎭 State: {p.current_state.name}", cls="font-medium text-gray-200"),
                P(f"📋 Strategy: {p.strategy}", cls="text-sm text-gray-400"),
                cls="mb-3 pb-3 border-b border-gray-700"
            ),
            
            # Research Metrics (Key Outcomes)
            H3("Creator Wellbeing", cls="text-sm font-semibold text-gray-300 mb-2"),
            Div(
                _metric_row("Burnout", p.burnout, "🔥", danger_threshold=0.7),
                _metric_row("Addiction", p.addiction_drive, "🎰", danger_threshold=0.7),
                _metric_row("Resilience", p.emotional_resilience, "💪", inverse=True),
                _metric_row("Arousal/Anxiety", p.arousal_level, "⚡", danger_threshold=0.7),
                cls="space-y-1 mb-3"
            ),
            
            # Sparklines (if history available)
            _agent_sparklines(agent) if len(agent.history) > 1 else None,
            
            # Content Traits
            H3("Content Traits", cls="text-sm font-semibold text-gray-300 mb-2"),
            Div(
                P(f"Quality: {p.quality:.2f} | Diversity: {p.diversity:.2f} | Consistency: {p.consistency:.2f}",
                  cls="text-xs text-gray-400"),
                cls="mb-2"
            ),
            
            # Activity
            P(f"⏱️ Ticks Active: {len(agent.history)}", cls="text-xs text-gray-400")
        ),
        cls="bg-gray-800 border-gray-700"
    )

def _metric_row(label, value, emoji, danger_threshold=0.7, inverse=False):
    """Helper to display a metric with color coding."""
    # Color based on value (red = bad, green = good)
    if inverse:  # Higher is better (e.g., resilience)
        color = "text-green-600" if value > 0.6 else "text-yellow-600" if value > 0.4 else "text-red-600"
    else:  # Lower is better (e.g., burnout, addiction)
        color = "text-red-600" if value > danger_threshold else "text-yellow-600" if value > 0.4 else "text-green-600"
    
    # Progress bar
    bar_width = f"{int(value * 100)}%"
    bar_color = "bg-red-500" if (not inverse and value > danger_threshold) or (inverse and value < 0.4) else "bg-yellow-500" if value > 0.4 and value < 0.7 else "bg-green-500"
    
    return Div(
        Div(
            Span(f"{emoji} {label}", cls="text-xs font-medium"),
            Span(f"{value:.2f}", cls=f"text-xs font-bold {color}"),
            cls="flex justify-between mb-1"
        ),
        Div(
            Div(cls=f"h-1.5 rounded {bar_color}", style=f"width: {bar_width}"),
            cls="w-full bg-gray-200 rounded h-1.5"
        )
    )

def _agent_sparklines(agent):
    """Render sparkline charts for agent's burnout and reward history."""
    if not agent.history or len(agent.history) < 2:
        return None
    
    agent_id = agent.profile.id
    
    # Extract history data (last 10 ticks)
    history_slice = agent.history[-10:]
    burnout_history = []
    reward_history = []
    
    for entry in history_slice:
        # Get burnout from state or profile snapshot
        burnout_history.append(entry.get("burnout", 0))
        reward_history.append(entry.get("final_reward", 0))
    
    ticks = list(range(len(history_slice)))
    
    return Div(
        H3("Recent Trends", cls="text-sm font-semibold text-gray-300 mb-2 mt-3 pt-3 border-t border-gray-700"),
        
        # Two sparklines side by side
        Div(
            # Burnout sparkline
            Div(
                P("🔥 Burnout", cls="text-xs text-gray-400 mb-1"),
                Canvas(id=f"burnout-{agent_id}", style="height: 40px;"),
                cls="flex-1"
            ),
            
            # Reward sparkline
            Div(
                P("🎯 Rewards", cls="text-xs text-gray-400 mb-1"),
                Canvas(id=f"reward-{agent_id}", style="height: 40px;"),
                cls="flex-1"
            ),
            
            cls="grid grid-cols-2 gap-2"
        ),
        
        # Chart.js scripts
        Script(f"""
            (function() {{
                // Burnout sparkline
                const burnoutCtx = document.getElementById('burnout-{agent_id}');
                if (burnoutCtx && window.Chart) {{
                    new Chart(burnoutCtx, {{
                        type: 'line',
                        data: {{
                            labels: {json.dumps(ticks)},
                            datasets: [{{
                                data: {json.dumps(burnout_history)},
                                borderColor: 'rgb(239, 68, 68)',
                                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                                borderWidth: 1.5,
                                pointRadius: 0,
                                tension: 0.3,
                                fill: true
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{ legend: {{ display: false }} }},
                            scales: {{
                                x: {{ display: false }},
                                y: {{ display: false, min: 0, max: 1 }}
                            }}
                        }}
                    }});
                }}
                
                // Reward sparkline
                const rewardCtx = document.getElementById('reward-{agent_id}');
                if (rewardCtx && window.Chart) {{
                    new Chart(rewardCtx, {{
                        type: 'line',
                        data: {{
                            labels: {json.dumps(ticks)},
                            datasets: [{{
                                data: {json.dumps(reward_history)},
                                borderColor: 'rgb(34, 197, 94)',
                                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                                borderWidth: 1.5,
                                pointRadius: 0,
                                tension: 0.3,
                                fill: true
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{ legend: {{ display: false }} }},
                            scales: {{
                                x: {{ display: false }},
                                y: {{ display: false, min: 0 }}
                            }}
                        }}
                    }});
                }}
            }})();
        """),
        
        cls="mt-2"
    )