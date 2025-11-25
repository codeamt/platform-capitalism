"""Decision tree visualization for agent content generation logic.

Shows the two-branch decision process:
1. Strategy Branch: Base output multiplier
2. Feedback Branch: Reward-based adjustment
"""
from fasthtml.common import Div, Span, P


def decision_tree(agent):
    """Render a visual decision tree showing agent's content generation logic.
    
    Args:
        agent: Agent instance with profile and history
    
    Returns:
        FastHTML Div component with decision tree visualization
    """
    # Get strategy info
    strategy = agent.profile.strategy
    strategy_desc = _get_strategy_description(strategy)
    
    # Get feedback info from last reward
    last_reward = None
    feedback_category = "No History"
    feedback_color = "text-gray-400"
    
    if agent.history:
        last_entry = agent.history[-1]
        last_reward = last_entry.get("final_reward", 0)
        feedback_category, feedback_color = _categorize_feedback(last_reward)
    
    return Div(
        # Header
        P("🧠 Decision Process", cls="text-xs font-semibold text-gray-300 mb-2"),
        
        # Decision tree container
        Div(
            # Branch 1: Strategy
            _strategy_branch(strategy, strategy_desc, agent),
            
            # Connector
            Div(
                Span("↓", cls="text-gray-600 text-lg"),
                cls="text-center py-1"
            ),
            
            # Branch 2: Feedback
            _feedback_branch(feedback_category, feedback_color, last_reward),
            
            # Result
            Div(
                Span("↓", cls="text-gray-600 text-lg"),
                cls="text-center py-1"
            ),
            
            _result_node(agent),
            
            cls="bg-gray-900 rounded p-3 border border-gray-700"
        ),
        
        cls="mt-3"
    )


def _strategy_branch(strategy, description, agent):
    """Render the strategy branch of the decision tree."""
    # Get posts generated to show in description
    posts_generated = getattr(agent, '_current_tick_posts', None)
    
    # Show description with current output if available
    if posts_generated is not None:
        enhanced_desc = f"{description} (~{posts_generated:.1f} posts/day)"
    else:
        enhanced_desc = description
    
    return Div(
        # Node label
        Div(
            Span("📋 Strategy", cls="text-xs font-semibold text-blue-400"),
            cls="mb-1"
        ),
        
        # Selected path
        Div(
            Div(
                Span(strategy, cls="text-xs font-medium text-gray-200"),
                cls="bg-blue-900 bg-opacity-30 border border-blue-700 rounded px-2 py-1"
            ),
            Div(
                Span(enhanced_desc, cls="text-xs text-gray-400 italic"),
                cls="mt-1"
            ),
            cls="ml-2"
        ),
        
        cls="mb-2"
    )


def _feedback_branch(category, color, reward_value):
    """Render the feedback branch of the decision tree."""
    reward_display = f"{reward_value:.2f}" if reward_value is not None else "N/A"
    
    return Div(
        # Node label
        Div(
            Span("🎯 Previous Reward", cls="text-xs font-semibold text-green-400"),
            cls="mb-1"
        ),
        
        # Selected path
        Div(
            Div(
                Span(category, cls=f"text-xs font-medium {color}"),
                Span(f" ({reward_display})", cls="text-xs text-gray-500"),
                cls="bg-green-900 bg-opacity-20 border border-green-700 rounded px-2 py-1"
            ),
            Div(
                Span(_get_action_description(category), cls="text-xs text-gray-400 italic"),
                cls="mt-1"
            ),
            cls="ml-2"
        ),
        
        cls="mb-2"
    )


def _result_node(agent):
    """Render the result node showing final output."""
    # Get actual posts generated if available
    posts_generated = getattr(agent, '_current_tick_posts', None)
    
    if posts_generated is not None:
        output_text = f"{posts_generated:.1f} posts generated"
        subtitle = "Base × Feedback Modifier"
    else:
        output_text = "Base × Feedback Modifier"
        subtitle = "Awaiting first tick"
    
    return Div(
        Div(
            Span("📊 Content Output", cls="text-xs font-semibold text-purple-400"),
            cls="mb-1"
        ),
        Div(
            Span(output_text, cls="text-xs font-bold text-purple-300"),
            cls="ml-2 mb-1"
        ),
        Div(
            Span(subtitle, cls="text-xs text-gray-500 italic"),
            cls="ml-2"
        ),
        cls="mb-1"
    )


def _get_strategy_description(strategy):
    """Get a brief description of the strategy's output characteristics."""
    descriptions = {
        "Quality Over Quantity": "Low volume, high quality",
        "Spray and Pray": "High volume, varied quality",
        "Niche Expert": "Focused, consistent output",
        "Trend Chaser": "Opportunistic, variable",
        "Consistent Creator": "Steady, reliable output"
    }
    return descriptions.get(strategy, "Balanced output")


def _categorize_feedback(reward):
    """Categorize reward into feedback type and return color.
    
    Returns:
        tuple: (category_name, tailwind_color_class)
    """
    if reward > 0.6:
        return "Strong Positive", "text-green-300"
    elif reward > 0.3:
        return "Positive", "text-green-400"
    elif reward > 0.1:
        return "Slight Positive", "text-green-500"
    elif reward > -0.1:
        return "Neutral", "text-gray-400"
    elif reward > -0.3:
        return "Slight Negative", "text-orange-400"
    elif reward > -0.6:
        return "Negative", "text-red-400"
    else:
        return "Strong Negative", "text-red-300"


def _get_action_description(category):
    """Get action description based on feedback category."""
    actions = {
        "Strong Positive": "Increase output significantly",
        "Positive": "Increase output moderately",
        "Slight Positive": "Slight increase in output",
        "Neutral": "Maintain current output",
        "Slight Negative": "Slight decrease in output",
        "Negative": "Decrease output moderately",
        "Strong Negative": "Decrease output significantly",
        "No History": "Use base strategy output"
    }
    return actions.get(category, "Adjust output accordingly")