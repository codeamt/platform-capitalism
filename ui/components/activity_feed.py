from fasthtml.common import Div, H2, H3, P, Span
from monsterui.all import Card, CardBody
from simulation.environment import GLOBAL_ENVIRONMENT

def activity_feed():
    """Display recent creator activity and state transitions."""
    agents = GLOBAL_ENVIRONMENT.agents
    tick_count = GLOBAL_ENVIRONMENT.tick_count
    
    # Collect recent activities from all agents
    activities = []
    
    for agent in agents:
        if not agent.history:
            continue
            
        # Get last few history entries
        recent_history = agent.history[-3:] if len(agent.history) >= 3 else agent.history
        
        for entry in recent_history:
            state = entry.get("state", "UNKNOWN")
            tick = entry.get("tick", 0)
            burnout = entry.get("burnout", 0)
            reward = entry.get("final_reward", 0)
            
            # Generate activity description based on state and metrics
            action = _generate_activity_description(state, burnout, reward)
            time_ago = _format_time_ago(tick_count, tick)
            
            activities.append({
                "agent_id": agent.profile.id,
                "agent_name": f"Creator {agent.profile.id}",
                "action": action,
                "time": time_ago,
                "state": state,
                "tick": tick
            })
    
    # Sort by most recent first
    activities.sort(key=lambda x: x["tick"], reverse=True)
    
    # Take top 10 most recent
    activities = activities[:10]
    
    if not activities:
        return Card(
            CardBody(
                H2("📋 Recent Activity", cls="text-lg sm:text-2xl font-bold text-gray-100 mb-3 sm:mb-4"),
                P("No activity yet. Run a tick to see creator behavior.", cls="text-xs sm:text-sm text-gray-400 text-center py-6 sm:py-8")
            ),
            cls="bg-gray-800 border-gray-700"
        )
    
    return Card(
        CardBody(
            H2("📋 Recent Activity", cls="text-lg sm:text-2xl font-bold text-gray-100 mb-3 sm:mb-4"),
            P("Live feed of creator state transitions and behaviors", cls="text-xs sm:text-sm text-gray-400 mb-3 sm:mb-4"),
            Div(
                *[_activity_item(a) for a in activities],
                cls="space-y-2 sm:space-y-3 overflow-y-auto",
                style="max-height: 600px;"
            )
        ),
        cls="bg-gray-800 border-gray-700"
    )

def _activity_item(activity):
    """Render a single activity item."""
    state = activity["state"]
    state_emoji = _get_state_emoji(state)
    state_color = _get_state_color(state)
    
    return Div(
        Div(
            # Left: Avatar/Icon
            Div(
                Span(state_emoji, cls="text-xl sm:text-2xl"),
                cls="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-gray-700 flex items-center justify-center"
            ),
            
            # Middle: Activity text
            Div(
                P(
                    Span(activity["agent_name"], cls="font-semibold text-gray-200 text-xs sm:text-sm"),
                    Span(" " + activity["action"], cls="text-gray-400 text-xs sm:text-sm"),
                    cls="text-xs sm:text-sm"
                ),
                P(
                    Span(state, cls=f"text-xs px-1.5 sm:px-2 py-0.5 rounded-full {state_color}"),
                    cls="mt-1"
                ),
                cls="flex-1 ml-2 sm:ml-3"
            ),
            
            # Right: Time
            P(activity["time"], cls="text-xs text-gray-500 flex-shrink-0 hidden sm:block"),
            
            cls="flex items-start"
        ),
        cls="p-2 sm:p-3 bg-gray-750 rounded-lg border border-gray-700 hover:border-gray-600 transition-colors"
    )

def _generate_activity_description(state, burnout, reward):
    """Generate human-readable activity description based on state and metrics."""
    descriptions = {
        "OPTIMIZER": [
            "maintained consistent quality output",
            "balanced workload effectively",
            "optimized content strategy",
            "achieved sustainable pace"
        ],
        "HUSTLER": [
            "posted high-volume content",
            "chased engagement metrics",
            "increased posting frequency",
            "pushed for viral content"
        ],
        "TRUE_BELIEVER": [
            "experimented with creative formats",
            "focused on artistic expression",
            "explored new content styles",
            "prioritized creative vision"
        ],
        "BURNOUT": [
            "reduced activity due to exhaustion",
            "took a break from posting",
            "showed signs of fatigue",
            "entered recovery mode"
        ]
    }
    
    # Add context based on metrics
    base_actions = descriptions.get(state, ["updated their status"])
    action = base_actions[hash(str(burnout + reward)) % len(base_actions)]
    
    # Add reward context
    if reward > 0.7:
        action += " (high reward)"
    elif reward < 0.3 and state != "BURNOUT":
        action += " (low reward)"
    
    return action

def _format_time_ago(current_tick, event_tick):
    """Format time difference as 'X ticks ago'."""
    diff = current_tick - event_tick
    if diff == 0:
        return "just now"
    elif diff == 1:
        return "1 tick ago"
    else:
        return f"{diff} ticks ago"

def _get_state_emoji(state):
    """Get emoji for state."""
    emojis = {
        "OPTIMIZER": "🎯",
        "HUSTLER": "⚡",
        "TRUE_BELIEVER": "✨",
        "BURNOUT": "🔥"
    }
    return emojis.get(state, "👤")

def _get_state_color(state):
    """Get Tailwind color classes for state badge."""
    colors = {
        "OPTIMIZER": "bg-green-900 text-green-300",
        "HUSTLER": "bg-yellow-900 text-yellow-300",
        "TRUE_BELIEVER": "bg-blue-900 text-blue-300",
        "BURNOUT": "bg-red-900 text-red-300"
    }
    return colors.get(state, "bg-gray-900 text-gray-300")