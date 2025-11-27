from fasthtml.common import Div, H2, H3, P, Span, Canvas, Script, Ul, Li, A
from monsterui.all import Card, CardBody
from ui.components.decision_tree import decision_tree
from simulation.environment import GLOBAL_ENVIRONMENT
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
                H2(f"Agent {p.id}", cls="text-lg sm:text-xl font-bold inline text-gray-100"),
                Span(status_text, cls=f"ml-2 text-xs sm:text-sm font-semibold {status_color}"),
                cls="mb-2 sm:mb-3"
            ),
            
            # State & Strategy
            Div(
                P(f"🎭 State: {p.current_state.name}", cls="font-medium text-gray-200 text-sm sm:text-base"),
                P(f"📋 Strategy: {p.strategy}", cls="text-xs sm:text-sm text-gray-400"),
                P(f"⏱️ Ticks Active: {len(agent.history)} | 📊 Total Posts: {sum(h.get('posts_generated', 0) for h in agent.history):.1f}", 
                  cls="text-xs text-gray-400 mt-1"),
                P(
                    Span(f"💵 Earnings: ${sum(h.get('cpm_earnings', 0) for h in agent.history):.2f}", cls="text-green-400 text-xs sm:text-sm"),
                    Span(" | ", cls="text-gray-600"),
                    Span(f"👁️ Views: {sum(h.get('posts_generated', 0) for h in agent.history) * GLOBAL_ENVIRONMENT.policy_engine.config.avg_views_per_post:,.0f}", cls="text-blue-400 text-xs sm:text-sm"),
                    cls="text-xs font-semibold mt-1"
                ),
                cls="mb-2 sm:mb-3 pb-2 sm:pb-3 border-b border-gray-700"
            ),
            
            # Tab Navigation
            Ul(
                Li(
                    A("📊 Metrics", 
                      href="#metrics",
                      data_tab="metrics",
                      cls="block px-2 sm:px-4 py-2 text-xs sm:text-sm font-medium text-gray-400 hover:text-blue-400 cursor-pointer transition-colors")
                ),
                Li(
                    A("🧠 Decision Tree", 
                      href="#decision",
                      data_tab="decision",
                      cls="block px-2 sm:px-4 py-2 text-xs sm:text-sm font-medium text-gray-400 hover:text-blue-400 cursor-pointer transition-colors")
                ),
                role="tablist",
                cls="flex border-b border-gray-700 mb-3 -mx-2 tab-container"
            ),
            
            # Tab 1: Metrics (visible by default)
            Div(
                # Research Metrics (Key Outcomes)
                H3("Creator Wellbeing", cls="text-xs sm:text-sm font-semibold text-gray-300 mb-2"),
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
                H3("Content Traits", cls="text-xs sm:text-sm font-semibold text-gray-300 mb-2 mt-3"),
                Div(
                    P(f"Quality: {p.quality:.2f} | Diversity: {p.diversity:.2f} | Consistency: {p.consistency:.2f}",
                      cls="text-xs text-gray-400"),
                    cls="mb-2"
                ),
                
                id="metrics",
                role="tabpanel",
                cls="overflow-y-auto",
                style="max-height: 400px;"
            ),
            
            # Tab 2: Decision Tree (hidden by default)
            Div(
                decision_tree(agent),
                id="decision",
                role="tabpanel",
                cls="overflow-y-auto",
                style="max-height: 400px; display: none;"
            ),
            
            # Tab switching script
            Script("""
                setTimeout(function() {
                    document.querySelectorAll('[data-tab]').forEach(tab => {
                        tab.addEventListener('click', (e) => {
                            e.preventDefault();
                            const tabName = tab.getAttribute('data-tab');
                            const card = tab.closest('.bg-gray-800');
                            
                            // Hide all panels in this card
                            card.querySelectorAll('[role="tabpanel"]').forEach(panel => {
                                panel.style.display = 'none';
                            });
                            
                            // Remove active class from all tabs in this card
                            card.querySelectorAll('[data-tab]').forEach(t => {
                                t.classList.remove('border-b-2', 'border-blue-500', 'text-blue-400');
                                t.classList.add('text-gray-400');
                            });
                            
                            // Show selected panel
                            const panel = card.querySelector(`#${tabName}`);
                            if (panel) panel.style.display = 'block';
                            
                            // Add active class to clicked tab
                            tab.classList.add('border-b-2', 'border-blue-500', 'text-blue-400');
                            tab.classList.remove('text-gray-400');
                        });
                    });
                    
                    // Set initial active tab for each card
                    document.querySelectorAll('.tab-container').forEach(container => {
                        const firstTab = container.querySelector('[data-tab]');
                        if (firstTab) {
                            firstTab.classList.add('border-b-2', 'border-blue-500', 'text-blue-400');
                            firstTab.classList.remove('text-gray-400');
                        }
                    });
                }, 100);
            """)
        ),
        cls="bg-gray-800 border-gray-700",
        style="height: auto; max-height: 600px; flex-shrink: 0;"
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
                Canvas(id=f"burnout-{agent_id}", width="150", height="40", style="max-height: 40px; width: 100%;"),
                cls="flex-1"
            ),
            
            # Reward sparkline
            Div(
                P("🎯 Rewards", cls="text-xs text-gray-400 mb-1"),
                Canvas(id=f"reward-{agent_id}", width="150", height="40", style="max-height: 40px; width: 100%;"),
                cls="flex-1"
            ),
            
            cls="grid grid-cols-2 gap-2"
        ),
        
        # Chart.js scripts
        Script(f"""
            setTimeout(function() {{
                // Burnout sparkline
                const burnoutCtx = document.getElementById('burnout-{agent_id}');
                if (burnoutCtx && window.Chart) {{
                    // Destroy existing chart if it exists
                    const existingBurnoutChart = Chart.getChart('burnout-{agent_id}');
                    if (existingBurnoutChart) {{
                        existingBurnoutChart.destroy();
                    }}
                    
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
                    // Destroy existing chart if it exists
                    const existingRewardChart = Chart.getChart('reward-{agent_id}');
                    if (existingRewardChart) {{
                        existingRewardChart.destroy();
                    }}
                    
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
            }}, 100);
        """),
        
        cls="mt-2"
    )