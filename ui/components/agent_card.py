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
                cls="overflow-y-auto overflow-x-hidden",
                style="max-height: 400px; display: none; padding-bottom: 1rem;"
            ),
            
            # Initialize tabs for this card
            Script("""
                if (typeof initAgentTabs === 'function') {
                    setTimeout(initAgentTabs, 100);
                }
            """)
        ),
        cls="bg-gray-800 border-gray-700",
        style="height: auto; max-height: 600px; flex-shrink: 0;"
    )

def _metric_row(label, value, emoji, danger_threshold=0.7, inverse=False):
    """Helper to display a metric with color coding."""
    # Enhanced semantic color coding with better contrast
    if inverse:  # Higher is better (e.g., resilience)
        if value > 0.6:
            text_color = "text-emerald-400"
            bar_color = "bg-gradient-to-r from-emerald-500 to-emerald-600"
            glow = "shadow-emerald-500/20"
        elif value > 0.4:
            text_color = "text-amber-400"
            bar_color = "bg-gradient-to-r from-amber-500 to-yellow-500"
            glow = "shadow-amber-500/20"
        else:
            text_color = "text-red-400"
            bar_color = "bg-gradient-to-r from-red-500 to-red-600"
            glow = "shadow-red-500/30 shadow-lg"
    else:  # Lower is better (e.g., burnout, addiction)
        if value > danger_threshold:
            text_color = "text-red-400"
            bar_color = "bg-gradient-to-r from-red-500 to-red-600"
            glow = "shadow-red-500/30 shadow-lg"
        elif value > 0.4:
            text_color = "text-amber-400"
            bar_color = "bg-gradient-to-r from-amber-500 to-yellow-500"
            glow = "shadow-amber-500/20"
        else:
            text_color = "text-emerald-400"
            bar_color = "bg-gradient-to-r from-emerald-500 to-emerald-600"
            glow = "shadow-emerald-500/20"
    
    # Progress bar width
    bar_width = f"{int(value * 100)}%"
    
    # Add pulse animation for critical values
    is_critical = (not inverse and value > danger_threshold) or (inverse and value < 0.4)
    pulse_class = "animate-pulse" if is_critical else ""
    
    return Div(
        Div(
            Span(f"{emoji} {label}", cls=f"text-xs font-medium text-gray-300 {pulse_class if is_critical else ''}"),
            Span(f"{value:.2f}", cls=f"text-xs font-bold {text_color}"),
            cls="flex justify-between mb-1"
        ),
        Div(
            Div(cls=f"h-2 rounded {bar_color} {glow} transition-all duration-300", style=f"width: {bar_width}"),
            cls="w-full bg-gray-700 rounded h-2"
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
        
        # Two sparklines side by side with improved visibility
        Div(
            # Burnout sparkline
            Div(
                P("🔥 Burnout", cls="text-xs font-semibold text-gray-300 mb-1"),
                Div(
                    Canvas(id=f"burnout-{agent_id}", width="150", height="60", style="max-height: 60px; width: 100%;"),
                    cls="bg-gray-750 rounded p-2 border border-gray-700"
                ),
                cls="flex-1"
            ),
            
            # Reward sparkline
            Div(
                P("🎯 Rewards", cls="text-xs font-semibold text-gray-300 mb-1"),
                Div(
                    Canvas(id=f"reward-{agent_id}", width="150", height="60", style="max-height: 60px; width: 100%;"),
                    cls="bg-gray-750 rounded p-2 border border-gray-700"
                ),
                cls="flex-1"
            ),
            
            cls="grid grid-cols-2 gap-3"
        ),
        
        # Initialize sparkline charts using external JS
        Script(f"""
            initBurnoutSparkline('{agent_id}', {json.dumps(ticks)}, {json.dumps(burnout_history)});
            initRewardSparkline('{agent_id}', {json.dumps(ticks)}, {json.dumps(reward_history)});
            // Re-initialize tabs after charts load
            if (typeof initAgentTabs === 'function') {{
                setTimeout(initAgentTabs, 200);
            }}
        """),
        
        cls="mt-2"
    )