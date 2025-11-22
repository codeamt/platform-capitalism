from fasthtml.common import Div, H2, H3, P, Span
from monsterui.all import Card, CardBody

def agent_state_distribution(summary):
    """Visual distribution of agent states with health indicators.
    
    Shows how agents are distributed across different behavioral states,
    which is a key indicator of system health.
    """
    state_dist = summary.get("state_distribution", {})
    total_agents = summary.get("num_agents", 0)
    
    if total_agents == 0:
        return Card(
            CardBody(
                H2("Agent State Distribution", cls="text-xl font-bold mb-4"),
                P("No agents in simulation", cls="text-gray-500")
            )
        )
    
    # State colors and descriptions
    state_info = {
        "OPTIMIZER": ("🎯", "Balanced, consistent creation", "bg-blue-100 text-blue-800 border-blue-300"),
        "HUSTLER": ("⚡", "High-output, chasing engagement", "bg-yellow-100 text-yellow-800 border-yellow-300"),
        "TRUE_BELIEVER": ("🌟", "Creative experimentation", "bg-purple-100 text-purple-800 border-purple-300"),
        "BURNOUT": ("🔥", "Exhausted, needs recovery", "bg-red-100 text-red-800 border-red-300"),
    }
    
    return Card(
        CardBody(
            H2("Agent State Distribution", cls="text-xl font-bold mb-4"),
            P(f"Total Agents: {total_agents}", cls="text-sm text-gray-600 mb-4"),
            
            # Visual bars for each state
            Div(
                *[_state_bar(state, count, total_agents, state_info.get(state, ("", "", "bg-gray-100")))
                  for state, count in state_dist.items()],
                cls="space-y-3"
            ),
            
            # Health warning if too many in burnout
            _burnout_warning(state_dist.get("BURNOUT", 0), total_agents) if state_dist.get("BURNOUT", 0) > 0 else None
        )
    )

def _state_bar(state_name, count, total, state_info):
    """Display a single state as a horizontal bar."""
    emoji, description, color_class = state_info
    percentage = (count / total * 100) if total > 0 else 0
    
    bar_color = color_class.replace("bg-", "").replace("text-", "").replace("border-", "")
    
    return Div(
        # Header: State name and count
        Div(
            Span(emoji, cls="text-xl mr-2"),
            Span(f"{state_name}", cls="font-semibold text-sm text-gray-200 flex-1"),
            Span(f"{count} agents ({percentage:.0f}%)", cls="text-xs text-gray-400"),
            cls="flex items-center mb-1"
        ),
        # Description
        P(description, cls="text-xs text-gray-400 mb-2 ml-7"),
        # Progress bar
        Div(
            Div(cls=f"h-6 rounded {bar_color}", style=f"width: {percentage}%"),
            cls="w-full bg-gray-700 rounded h-6"
        ),
        cls="p-3 bg-gray-700 rounded-lg mb-3"
    )

def _burnout_warning(burnout_count, total):
    """Display warning if burnout rate is high."""
    burnout_rate = (burnout_count / total) if total > 0 else 0
    
    if burnout_rate > 0.5:
        severity = "🚨 CRITICAL"
        color = "bg-red-100 border-red-500 text-red-800"
    elif burnout_rate > 0.3:
        severity = "⚠️ WARNING"
        color = "bg-yellow-100 border-yellow-500 text-yellow-800"
    else:
        return None
    
    return Div(
        Div(
            Span(severity, cls="font-bold"),
            Span(f"{burnout_rate*100:.0f}% of creators are burned out", cls="ml-2"),
            cls="flex items-center"
        ),
        P("This indicates an unhealthy creator ecosystem. Consider switching to differential reinforcement.",
          cls="text-sm mt-2"),
        cls=f"mt-4 p-3 rounded border-2 {color}"
    )

# Keep old function name for backwards compatibility
def network_graph(agents):
    """Legacy function - now shows state distribution."""
    # Create a summary-like dict from agents
    from simulation.agents.state_machine import CreatorState
    
    if not agents:
        summary = {"num_agents": 0, "state_distribution": {}}
    else:
        state_counts = {state.name: 0 for state in CreatorState}
        for agent in agents:
            state_counts[agent.profile.current_state.name] += 1
        summary = {
            "num_agents": len(agents),
            "state_distribution": state_counts
        }
    
    return agent_state_distribution(summary)