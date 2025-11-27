from fasthtml.common import Div, H1, H2, H3, P, Button, Span, Progress, Li, A, Ul, Canvas, Script
from monsterui.all import Slider, Container, TabContainer, Card, CardBody
from ui.components import (
    activity_feed,
    scenario_selector,
    agent_card
)
from simulation.environment import GLOBAL_ENVIRONMENT


def DashboardPage():
    """Primary research interface showing system health and creator wellbeing.
    
    Layout:
    - Hero section with instructions and controls
    - Status bar (full width - always visible)
    - Tabbed content:
      - Tab 1: Simulation (selector + reward timeline)
      - Tab 2: Agents (carousel only)
      - Tab 3: System Health (pie chart + arousal trend)
    """
    summary = GLOBAL_ENVIRONMENT.summary()
    history = GLOBAL_ENVIRONMENT.history
    agents = GLOBAL_ENVIRONMENT.agents
    tick_count = GLOBAL_ENVIRONMENT.tick_count
    
    content = Div(
        # Hero Section
        Div(
            Div(
                H1("🎯 Quick Start", cls="text-2xl sm:text-3xl font-bold text-gray-100"),
                P("1. Select a scenario below to compare platform governance strategies",
                  cls="text-xs sm:text-sm text-gray-400 mt-2"),
                P("2. Click ▶️ Run Tick to advance the simulation and watch creator wellbeing metrics",
                  cls="text-xs sm:text-sm text-gray-400"),
                P("3. Compare differential (predictable) vs intermittent (exploitative) reinforcement patterns",
                  cls="text-xs sm:text-sm text-gray-400"),
                cls="flex-1 mb-4 sm:mb-0"
            ),
            Div(
                Button("▶️ Run Tick",
                       hx_post="/api/tick",
                       hx_target="#main-content",
                       hx_swap="outerHTML",
                       cls="px-3 sm:px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold text-sm sm:text-base w-full sm:w-auto mb-2 sm:mb-0 sm:mr-2"),
                Button("🔄 Reset",
                       hx_post="/api/reset",
                       hx_target="#main-content",
                       hx_swap="outerHTML",
                       cls="px-3 sm:px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 font-semibold text-sm sm:text-base w-full sm:w-auto"),
                cls="flex flex-col sm:flex-row gap-2"
            ),
            cls="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-4 sm:mb-6 pb-4 sm:pb-6 border-b border-gray-700"
        ),
        
        # Status Bar (full width)
        _status_bar(tick_count, summary, agents),
        
        # Tabbed Content Container
        Container(
            TabContainer(
                Li(A("🎮 Simulation", href='#', cls='uk-active text-xs sm:text-base')),
                Li(A("👥 Agents", href='#', cls='text-xs sm:text-base')),
                Li(A("📊 Health", href='#', cls='text-xs sm:text-base')),
                uk_switcher='connect: #dashboard-tabs; animation: uk-animation-fade',
                alt=True
            ),
            Ul(id="dashboard-tabs", cls="uk-switcher")(
                # Tab 1: Simulation (Selector + Activity Feed in responsive grid)
                Li(
                    Div(
                        scenario_selector(GLOBAL_ENVIRONMENT.current_scenario or "Creator-First Platform", source="dashboard"),
                        activity_feed(),
                        cls="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6",
                        style="grid-template-columns: 1fr; lg:grid-template-columns: 1fr 2fr;"
                    )
                ),
                
                # Tab 2: Agents (Just carousel, full width)
                Li(
                    Div(
                        H2("👥 Individual Creators", cls="text-xl sm:text-2xl font-bold mb-4 text-gray-100"),
                        Slider(
                            *[agent_card(a) for a in agents] if agents else [P("No agents. Load a scenario to begin.", cls="text-gray-400 text-center py-8")],
                            items_cls='gap-4',
                            uk_slider='autoplay: true; autoplay-interval: 3000; finite: true'
                        ) if agents else P("No agents. Load a scenario to begin.", cls="text-gray-400 text-center py-8")
                    )
                ),
                
                # Tab 3: System Health
                Li(
                    _health_trend_only(history)
                )
            ),
            cls="mt-6"
        ),
        
        cls="max-w-7xl mx-auto p-3 sm:p-6",
        id="main-content"
    )
    
    return content

def _status_bar(tick_count, summary, agents):
    """Status bar showing simulation progress and key metrics."""
    num_agents = len(agents)
    avg_burnout = summary.get("avg_burnout", 0)
    avg_addiction = summary.get("avg_addiction", 0)
    avg_resilience = summary.get("avg_resilience", 0)
    burnout_rate = summary.get("burnout_rate", 0)
    
    # Calculate total platform earnings
    total_earnings = sum(
        sum(h.get('cpm_earnings', 0) for h in agent.history)
        for agent in agents
    )
    
    mode = GLOBAL_ENVIRONMENT.policy_engine.config.mode
    
    # Determine status color based on burnout
    if avg_burnout < 0.4:
        status_color = "bg-green-600"
        status_text = "✅ Healthy"
    elif avg_burnout < 0.7:
        status_color = "bg-yellow-600"
        status_text = "⚠️ Warning"
    else:
        status_color = "bg-red-600"
        status_text = "🚨 Critical"
    
    return Div(
        Div(
            # Top: Status indicator and day
            Div(
                Span(status_text, cls=f"px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-semibold text-white {status_color}"),
                Span(f"Day {tick_count}", cls="text-xs sm:text-sm font-semibold text-gray-300 ml-2 sm:ml-4"),
                cls="flex items-center mb-3 sm:mb-0"
            ),
            
            # Bottom: All metrics (wrap on mobile)
            Div(
                Span(f"👥 {num_agents}", cls="text-xs sm:text-sm text-gray-400 mr-2 sm:mr-4"),
                Span(f"💰 ${total_earnings:.2f}", cls="text-xs sm:text-sm font-semibold text-green-400 mr-2 sm:mr-4"),
                Span(f"🔥 {avg_burnout:.2f}", cls="text-xs sm:text-sm text-gray-400 mr-2 sm:mr-4"),
                Span(f"🎮 {avg_addiction:.2f}", cls="text-xs sm:text-sm text-gray-400 mr-2 sm:mr-4"),
                Span(f"🛡️ {avg_resilience:.2f}", cls="text-xs sm:text-sm text-gray-400 mr-2 sm:mr-4"),
                Span(f"📈 {burnout_rate:.2f}", cls="text-xs sm:text-sm text-gray-400 mr-2 sm:mr-4 hidden sm:inline"),
                Span(f"{mode.capitalize()}", cls="text-xs sm:text-sm text-gray-400 hidden sm:inline"),
                cls="flex items-center flex-wrap gap-y-2"
            ),
            
            cls="flex flex-col sm:flex-row sm:justify-between sm:items-center"
        ),
        cls="bg-gray-800 border border-gray-700 rounded-lg p-3 sm:p-4 mb-4 sm:mb-6"
    )

def _health_trend_only(history):
    """Display agent distribution pie chart and arousal trend."""
    agents = GLOBAL_ENVIRONMENT.agents
    
    # Count agents by state
    state_counts = {}
    for agent in agents:
        state = agent.profile.current_state.name
        state_counts[state] = state_counts.get(state, 0) + 1
    
    # Prepare data for pie chart
    state_labels = list(state_counts.keys())
    state_values = list(state_counts.values())
    
    # Color mapping for states
    state_colors = {
        "OPTIMIZER": "rgb(34, 197, 94)",
        "HUSTLER": "rgb(234, 179, 8)",
        "TRUE_BELIEVER": "rgb(59, 130, 246)",
        "BURNED_OUT": "rgb(239, 68, 68)",
        "ADDICTED": "rgb(168, 85, 247)",
        "RESILIENT": "rgb(16, 185, 129)"
    }
    colors = [state_colors.get(s, "rgb(107, 114, 128)") for s in state_labels]
    
    if not history.get("ticks"):
        return Card(
            CardBody(
                H2("🎯 Agent Distribution", cls="text-xl sm:text-2xl font-bold text-gray-100 mb-4"),
                Canvas(id="agentDistributionPie", style="height: 300px; max-height: 300px;"),
                Script(f"""
                    setTimeout(function() {{
                        const ctx = document.getElementById('agentDistributionPie');
                        if (!ctx) return;
                        
                        // Destroy existing chart if it exists
                        const existingChart = Chart.getChart('agentDistributionPie');
                        if (existingChart) {{
                            existingChart.destroy();
                        }}
                        
                        new Chart(ctx, {{
                            type: 'pie',
                            data: {{
                                labels: {state_labels},
                                datasets: [{{
                                    data: {state_values},
                                    backgroundColor: {colors},
                                    borderColor: 'rgb(31, 41, 55)',
                                    borderWidth: 2
                                }}]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    legend: {{
                                        display: true,
                                        position: 'right',
                                        labels: {{
                                            color: 'rgb(209, 213, 219)',
                                            font: {{ size: 12 }}
                                        }}
                                    }}
                                }}
                            }}
                        }});
                    }}, 100);
                """)
            ),
            cls="bg-gray-800 border-gray-700"
        )
    
    ticks = history.get("ticks", [])
    arousal = history.get("avg_arousal", [])
    
    return Div(
        # Pie chart for agent distribution
        Card(
            CardBody(
                H2("🎯 Agent Distribution", cls="text-xl sm:text-2xl font-bold text-gray-100 mb-4"),
                Canvas(id="agentDistributionPie", style="height: 300px; max-height: 300px;"),
                Script(f"""
                    setTimeout(function() {{
                        const ctx = document.getElementById('agentDistributionPie');
                        if (!ctx) return;
                        
                        // Destroy existing chart if it exists
                        const existingChart = Chart.getChart('agentDistributionPie');
                        if (existingChart) {{
                            existingChart.destroy();
                        }}
                        
                        new Chart(ctx, {{
                            type: 'pie',
                            data: {{
                                labels: {state_labels},
                                datasets: [{{
                                    data: {state_values},
                                    backgroundColor: {colors},
                                    borderColor: 'rgb(31, 41, 55)',
                                    borderWidth: 2
                                }}]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    legend: {{
                                        display: true,
                                        position: 'right',
                                        labels: {{
                                            color: 'rgb(209, 213, 219)',
                                            font: {{ size: 12 }}
                                        }}
                                    }}
                                }}
                            }}
                        }});
                    }}, 100);
                """)
            ),
            cls="bg-gray-800 border-gray-700 mb-6"
        ),
        
        # Arousal trend line chart
        Card(
            CardBody(
                H2("📈 Arousal Trend (Last 20 Ticks)", cls="text-xl sm:text-2xl font-bold text-gray-100 mb-4"),
                P("Track creator arousal/engagement over time", cls="text-xs sm:text-sm text-gray-400 mb-4"),
                Canvas(id="arousalTrendChart", style="height: 300px; max-height: 300px;"),
                Script(f"""
                    setTimeout(function() {{
                        const ctx = document.getElementById('arousalTrendChart');
                        if (!ctx) return;
                        
                        // Destroy existing chart if it exists
                        const existingChart = Chart.getChart('arousalTrendChart');
                        if (existingChart) {{
                            existingChart.destroy();
                        }}
                        
                        new Chart(ctx, {{
                            type: 'line',
                            data: {{
                                labels: {ticks},
                                datasets: [
                                    {{
                                        label: 'Arousal',
                                        data: {arousal},
                                        borderColor: 'rgb(59, 130, 246)',
                                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                        tension: 0.3,
                                        fill: true
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    legend: {{
                                        display: true,
                                        position: 'top',
                                        labels: {{
                                            color: 'rgb(209, 213, 219)',
                                            font: {{ size: 12 }}
                                        }}
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
                                        grid: {{
                                            color: 'rgba(75, 85, 99, 0.3)'
                                        }},
                                        ticks: {{
                                            color: 'rgb(156, 163, 175)'
                                        }}
                                    }},
                                    x: {{
                                        grid: {{
                                            color: 'rgba(75, 85, 99, 0.3)'
                                        }},
                                        ticks: {{
                                            color: 'rgb(156, 163, 175)'
                                        }}
                                    }}
                                }}
                            }}
                        }});
                    }}, 100);
                """)
            ),
            cls="bg-gray-800 border-gray-700"
        )
    )