from fasthtml.common import Div, H2, H3, Form, Input, Label, Button, P, Option, Optgroup, Span
from monsterui.all import Card, CardBody, Select

def preset_selector():
    """Quick-load buttons for policy presets.
    
    Allows users to quickly experiment with different governance models
    by auto-populating the policy form with preset configurations.
    """
    from simulation.policy_engine.config import POLICY_PRESETS
    
    return Card(
        CardBody(
            H2("⚡ Quick Load Presets", cls="text-xl font-bold mb-3 text-gray-100"),
            P("Instantly load common policy configurations", cls="text-sm text-gray-400 mb-4"),
            
            # Preset buttons grid
            Div(
                *[_preset_button(preset_id, preset_data) for preset_id, preset_data in POLICY_PRESETS.items()],
                cls="grid grid-cols-1 gap-2"
            ),
            
            # Info text
            P(
                "💡 Presets auto-populate the policy form below. You can then fine-tune individual parameters.",
                cls="text-xs text-gray-400 italic mt-4 p-2 bg-gray-700 rounded"
            )
        ),
        cls="bg-gray-800 border-gray-700"
    )

def _preset_button(preset_id: str, preset_data: dict):
    """Create a button for a single preset."""
    # Color coding by preset type
    colors = {
        "optimal": "bg-green-600 hover:bg-green-700 border-green-500",
        "exploitative": "bg-red-600 hover:bg-red-700 border-red-500",
        "balanced": "bg-blue-600 hover:bg-blue-700 border-blue-500",
        "cooperative": "bg-purple-600 hover:bg-purple-700 border-purple-500",
    }
    color_class = colors.get(preset_id, "bg-gray-600 hover:bg-gray-700 border-gray-500")
    
    return Form(
        Input(type="hidden", name="preset", value=preset_id),
        Button(
            Div(
                Span(preset_data["name"], cls="font-semibold"),
                P(preset_data["description"], cls="text-xs opacity-90 mt-1"),
                cls="text-left"
            ),
            type="submit",
            cls=f"w-full px-4 py-3 {color_class} text-white rounded-lg border-2 transition-all"
        ),
        hx_post="/api/load-preset",
        hx_target="#main-content",
        hx_swap="outerHTML"
    )

def scenario_selector(current_scenario="Creator-First Platform", source="dashboard"):
    """Dropdown to select between different platform scenarios.
    
    Args:
        current_scenario: Currently active scenario name
        source: Either 'dashboard' or 'governance' - determines which page to refresh
    """
    from simulation.scenarios.presets import ALL_SCENARIOS
    
    # Group scenarios by type
    exploitative = ["Algorithmic Slot Machine", "Engagement Maximizer"]
    sustainable = ["Creator-First Platform", "Cooperative Commons"]
    hybrid = ["Platform in Transition", "Mostly Differential"]
    
    # Get current scenario description
    current_desc = ALL_SCENARIOS.get(current_scenario, ALL_SCENARIOS["Creator-First Platform"]).description if current_scenario else ""
    
    return Card(
        CardBody(
            H2("🎬 Scenario Selector", cls="text-xl font-bold mb-3 text-gray-100"),
            P("Compare exploitative vs. sustainable platform governance", cls="text-sm text-gray-400 mb-4"),
            
            Form(
                # Hidden field to track source page
                Input(type="hidden", name="source", value=source),
                
                # Scenario dropdown with grouped options
                Div(
                    Label("Select Platform Scenario", cls="text-sm font-semibold text-gray-300 mb-2"),
                    Select(
                        Optgroup(label="⚠️ Exploitative Systems (Intermittent)")(
                            *[Option(name, value=name, selected=(name == current_scenario)) for name in exploitative]
                        ),
                        Optgroup(label="✅ Sustainable Systems (Differential)")(
                            *[Option(name, value=name, selected=(name == current_scenario)) for name in sustainable]
                        ),
                        Optgroup(label="🔀 Hybrid Systems (Mixed)")(
                            *[Option(name, value=name, selected=(name == current_scenario)) for name in hybrid]
                        ),
                        name="scenario",
                        id="scenario-select",
                        icon=True,
                        insertable=False,
                        placeholder="Choose a scenario...",
                        cls_custom="button: uk-input-fake justify-between w-full bg-gray-700 text-gray-100 border-gray-600; dropdown: w-full",
                        hx_post="/scenarios/load",
                        hx_target="#main-content",
                        hx_swap="outerHTML",
                        hx_trigger="change",
                        hx_include="[name='source']"
                    ),
                    cls="mb-4"
                ),
                
                # Show current scenario description
                Div(
                    P("📝 Current Scenario:", cls="text-xs font-semibold text-gray-400 mb-1"),
                    P(current_desc, cls="text-sm text-gray-300 italic p-3 bg-gray-700 rounded"),
                    cls="mt-4"
                ) if current_scenario else None
            )
        ),
        cls="bg-gray-800 border-gray-700"
    )

def policy_controls(mode, cfg):
    """Fine-grained policy parameter controls."""
    # Mode badge
    mode_badges = {
        "differential": ("🌱 Differential", "bg-green-100 text-green-800"),
        "intermittent": ("🎰 Intermittent", "bg-red-100 text-red-800"),
        "hybrid": ("🔀 Hybrid", "bg-blue-100 text-blue-800"),
    }
    mode_text, mode_class = mode_badges.get(mode, (mode, "bg-gray-100 text-gray-800"))
    
    return Card(
        CardBody(
            # Header
            Div(
                H2("⚙️ Policy Parameters", cls="text-xl font-bold text-gray-100"),
                Div(mode_text, cls=f"px-3 py-1 rounded-full text-sm font-semibold {mode_class}"),
                cls="flex justify-between items-center mb-4"
            ),
            
            # Policy Impact Preview (like nutrition facts)
            _policy_impact_preview(cfg, mode),
            
            Form(
                # Reward weights
                Div(
                    H3("Reward Weights", cls="text-sm font-semibold text-gray-300 mb-2"),
                    _param_input("Quality Weight", "quality_weight", cfg.quality_weight),
                    _param_input("Diversity Weight", "diversity_weight", cfg.diversity_weight),
                    _param_input("Consistency Weight", "consistency_weight", cfg.consistency_weight),
                    _param_input("Volume Weight", "volume_weight", cfg.volume_weight),
                    _param_input("Break Reward", "break_reward", cfg.break_reward),
                    cls="mb-4"
                ),
                
                # Wellbeing parameters
                Div(
                    H3("Creator Wellbeing", cls="text-sm font-semibold text-gray-300 mb-2"),
                    _param_input("Burnout Penalty", "burnout_penalty", cfg.burnout_penalty),
                    _param_input("Sustainability Bonus", "sustainability_bonus", cfg.sustainability_bonus),
                    _param_input("Baseline Guarantee", "baseline_guarantee", cfg.baseline_guarantee),
                    cls="mb-4"
                ),
                
                # Intermittent parameters (if applicable)
                Div(
                    H3("Intermittent Parameters", cls="text-sm font-semibold text-gray-300 mb-2"),
                    _param_input("Probability", "intermittent_probability", cfg.intermittent_probability),
                    _param_input("Variance", "intermittent_variance", cfg.intermittent_variance),
                    cls="mb-4"
                ) if mode in ["intermittent", "hybrid"] else None,
                
                Button("Update Policy", 
                       type="submit",
                       cls="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"),
                action="/api/update-policy", 
                method="post",
                hx_post="/api/update-policy",
                hx_target="#main-content",
                hx_swap="outerHTML",
                hx_indicator="#loading-indicator"
            )
        ),
        cls="bg-gray-800 border-gray-700"
    )

def _policy_impact_preview(cfg, mode):
    """Show expected system behavior based on current policy (like nutrition facts)."""
    # Calculate key metrics
    total_reward_weight = cfg.quality_weight + cfg.diversity_weight + cfg.consistency_weight + cfg.volume_weight
    wellbeing_focus = cfg.burnout_penalty + cfg.sustainability_bonus + cfg.baseline_guarantee
    predictability = 1.0 if mode == "differential" else (0.5 if mode == "hybrid" else cfg.intermittent_probability)
    
    # Determine health rating
    health_score = (wellbeing_focus * 0.4) + (predictability * 0.4) + (cfg.break_reward * 0.2)
    if health_score > 0.6:
        health_label = "✅ Sustainable"
        health_color = "text-green-400"
    elif health_score > 0.3:
        health_label = "⚠️ Mixed"
        health_color = "text-yellow-400"
    else:
        health_label = "🚨 Exploitative"
        health_color = "text-red-400"
    
    return Div(
        H3("📊 Policy Impact Preview", cls="text-sm font-semibold text-gray-300 mb-2"),
        P("Expected system behavior with current settings:", cls="text-xs text-gray-400 mb-3"),
        
        # Key metrics grid
        Div(
            _impact_metric("Creator Health", health_label, health_color),
            _impact_metric("Predictability", f"{predictability:.0%}", "text-blue-400"),
            _impact_metric("Reward Focus", f"{total_reward_weight:.2f}", "text-purple-400"),
            _impact_metric("Wellbeing Support", f"{wellbeing_focus:.2f}", "text-green-400"),
            cls="grid grid-cols-2 gap-2 mb-3"
        ),
        
        # Interpretation
        P(
            "💡 " + _get_policy_interpretation(mode, health_score, predictability),
            cls="text-xs text-gray-400 italic p-2 bg-gray-700 rounded"
        ),
        
        cls="mb-4 p-3 bg-gray-700 rounded-lg border border-gray-600"
    )

def _impact_metric(label, value, color):
    """Small metric for impact preview."""
    return Div(
        P(label, cls="text-xs text-gray-400"),
        P(value, cls=f"text-sm font-bold {color}"),
        cls="p-2 bg-gray-800 rounded text-center"
    )

def _get_policy_interpretation(mode, health_score, predictability):
    """Get human-readable interpretation of policy impact."""
    if mode == "differential":
        return "Predictable rewards promote sustainable creator wellbeing and work-life balance."
    elif mode == "intermittent":
        if predictability < 0.3:
            return "Low reward probability creates addiction loops and burnout risk."
        else:
            return "Moderate unpredictability may drive engagement but risks creator burnout."
    else:  # hybrid
        if health_score > 0.5:
            return "Balanced approach - some unpredictability with wellbeing safeguards."
        else:
            return "Mixed signals - consider increasing wellbeing support or predictability."

def _param_input(label, name, value):
    """Helper for parameter input field."""
    return Div(
        Label(label, cls="text-xs font-medium text-gray-300"),
        Input(
            name=name, 
            value=f"{value:.2f}", 
            type="number", 
            step="0.01",
            min="0",
            max="1" if "weight" in name or "probability" in name else "10",
            cls="w-full px-2 py-1 border border-gray-600 bg-gray-700 text-gray-100 rounded text-sm focus:border-blue-500 focus:outline-none"
        ),
        cls="mb-2"
    )