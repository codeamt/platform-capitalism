import json
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
    """Display system health gauge, agent trait distributions, and wellbeing trends."""
    agents = GLOBAL_ENVIRONMENT.agents
    
    # Get current and previous health scores
    health_scores = history.get("health_score", [])
    current_health = health_scores[-1] if health_scores else 0.5
    previous_health = health_scores[-2] if len(health_scores) > 1 else None
    
    # Collect agent trait distributions (initialization values)
    trait_data = {
        "Burnout": [agent.profile.burnout for agent in agents],
        "Addiction": [agent.profile.addiction_drive for agent in agents],
        "Resilience": [agent.profile.emotional_resilience for agent in agents],
        "Arousal": [agent.profile.arousal_level for agent in agents]
    }
    
    if not history.get("ticks"):
        return Div(
            # System Health Gauge
            Card(
                CardBody(
                    H2("💚 System Health Score", cls="text-xl sm:text-2xl font-bold text-gray-100 mb-4"),
                    P("Overall creator wellbeing metric (0-100)", cls="text-xs sm:text-sm text-gray-400 mb-4"),
                    Canvas(id="systemHealthGauge", style="height: 200px; max-height: 200px;"),
                    Script(f"""
                        initSystemHealthGauge('systemHealthGauge', {current_health}, {previous_health if previous_health else 'null'});
                    """)
                ),
                cls="bg-gray-800 border-gray-700 mb-6"
            ),
            # Agent Trait Distributions
            Card(
                CardBody(
                    H2("📊 Agent Trait Distributions", cls="text-xl sm:text-2xl font-bold text-gray-100 mb-4"),
                    P("Distribution of randomized initialization values across agents", cls="text-xs sm:text-sm text-gray-400 mb-4"),
                    Canvas(id="agentTraitBoxPlots", style="height: 300px; max-height: 300px;"),
                    Script(f"""
                        initAgentTraitBoxPlots('agentTraitBoxPlots', {json.dumps(trait_data)});
                    """)
                ),
                cls="bg-gray-800 border-gray-700"
            )
        )
    
    # Calculate reward characteristics
    all_rewards = []
    for agent in agents:
        if agent.history:
            all_rewards.extend([h.get("final_reward", 0) for h in agent.history])
    
    avg_reward = sum(all_rewards) / len(all_rewards) if all_rewards else 0
    variance = sum((r - avg_reward) ** 2 for r in all_rewards) / len(all_rewards) if all_rewards else 0
    predictability = 1 - min(variance, 1)  # Simple predictability metric
    
    # Calculate state transitions
    state_transitions = {}
    for agent in agents:
        if len(agent.history) > 1:
            for i in range(len(agent.history) - 1):
                from_state = agent.history[i].get("state", "UNKNOWN")
                to_state = agent.history[i + 1].get("state", "UNKNOWN")
                if from_state != to_state:
                    key = f"{from_state}->{to_state}"
                    state_transitions[key] = state_transitions.get(key, 0) + 1
    
    # Calculate correlations between metrics
    burnout_vals = history.get("avg_burnout", [])
    addiction_vals = history.get("avg_addiction", [])
    resilience_vals = history.get("avg_resilience", [])
    arousal_vals = history.get("avg_arousal", [])
    
    def calculate_correlation(x, y):
        if len(x) < 2 or len(y) < 2:
            return 0
        n = min(len(x), len(y))
        x, y = x[:n], y[:n]
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denom_x = sum((x[i] - mean_x) ** 2 for i in range(n)) ** 0.5
        denom_y = sum((y[i] - mean_y) ** 2 for i in range(n)) ** 0.5
        return numerator / (denom_x * denom_y) if denom_x and denom_y else 0
    
    correlations = {
        "Burnout_Addiction": calculate_correlation(burnout_vals, addiction_vals),
        "Burnout_Resilience": calculate_correlation(burnout_vals, resilience_vals),
        "Burnout_Arousal": calculate_correlation(burnout_vals, arousal_vals),
        "Addiction_Resilience": calculate_correlation(addiction_vals, resilience_vals),
        "Addiction_Arousal": calculate_correlation(addiction_vals, arousal_vals),
        "Resilience_Arousal": calculate_correlation(resilience_vals, arousal_vals)
    }
    
    return Div(
        # System Health Gauge
        Card(
            CardBody(
                H2("💚 System Health Score", cls="text-xl sm:text-2xl font-bold text-gray-100 mb-4"),
                P("Overall creator wellbeing metric (0-100)", cls="text-xs sm:text-sm text-gray-400 mb-4"),
                Canvas(id="systemHealthGauge", style="height: 200px; max-height: 200px;"),
                Script(f"""
                    initSystemHealthGauge('systemHealthGauge', {current_health}, {previous_health if previous_health else 'null'});
                """)
            ),
            cls="bg-gray-800 border-gray-700 mb-6"
        ),
        
        # Agent Trait Distributions (Box Plots)
        Card(
            CardBody(
                H2("📊 Agent Trait Distributions", cls="text-xl sm:text-2xl font-bold text-gray-100 mb-4"),
                P("Distribution of current trait values across agents (mean ± std)", cls="text-xs sm:text-sm text-gray-400 mb-4"),
                Canvas(id="agentTraitBoxPlots", style="height: 300px; max-height: 300px;"),
                Script(f"""
                    initAgentTraitBoxPlots('agentTraitBoxPlots', {json.dumps(trait_data)});
                """)
            ),
            cls="bg-gray-800 border-gray-700 mb-6"
        ),
        
        # 3-column grid for detailed analytics
        Div(
            # Reward Characteristics
            Card(
                CardBody(
                    H3("🎁 Reward Distribution", cls="text-lg font-bold text-gray-100 mb-2"),
                    P("Histogram of reward values", cls="text-xs text-gray-400 mb-3"),
                    Canvas(id="rewardCharacteristics", style="height: 250px; max-height: 250px;"),
                    Script(f"""
                        initRewardCharacteristics('rewardCharacteristics', {json.dumps(all_rewards)}, {avg_reward}, {variance}, {predictability});
                    """)
                ),
                cls="bg-gray-800 border-gray-700"
            ),
            
            # State Transitions
            Card(
                CardBody(
                    H3("🔄 State Transitions", cls="text-lg font-bold text-gray-100 mb-2"),
                    P("Most common state changes", cls="text-xs text-gray-400 mb-3"),
                    Canvas(id="stateTransitions", style="height: 250px; max-height: 250px;"),
                    Script(f"""
                        initStateTransitionFlow('stateTransitions', {json.dumps(state_transitions)});
                    """)
                ),
                cls="bg-gray-800 border-gray-700"
            ),
            
            # Correlation Heatmap
            Card(
                CardBody(
                    H3("🔗 Metric Correlations", cls="text-lg font-bold text-gray-100 mb-2"),
                    P("Relationships between traits", cls="text-xs text-gray-400 mb-3"),
                    Canvas(id="correlationHeatmap", style="height: 250px; max-height: 250px;"),
                    Script(f"""
                        initCorrelationHeatmap('correlationHeatmap', {json.dumps(correlations)});
                    """)
                ),
                cls="bg-gray-800 border-gray-700"
            ),
            
            cls="grid grid-cols-1 lg:grid-cols-3 gap-6"
        )
    )