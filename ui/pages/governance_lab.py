from fasthtml.common import Div, H1, P
from ui.components import policy_controls, scenario_selector, transparency_panel
from simulation.environment import GLOBAL_ENVIRONMENT


def GovernanceLabPage():
    """Platform governance settings and policy configuration.
    
    Combines scenario selection and fine-grained policy controls.
    UX: Like 'counting calories' - see how each policy parameter affects system dynamics.
    """
    cfg = GLOBAL_ENVIRONMENT.policy_engine.config
    events = GLOBAL_ENVIRONMENT.last_tick_explanations
    
    # Get current scenario name (if any)
    from simulation.scenarios.presets import ALL_SCENARIOS
    current_scenario = None
    for name, scenario in ALL_SCENARIOS.items():
        if scenario.policy.mode == cfg.mode:
            current_scenario = name
            break
    
    content = Div(
        # Header
        H1("⚙️ Governance Lab", cls="text-4xl font-bold text-gray-100 mb-2"),
        P("Configure platform policies and compare reinforcement strategies",
          cls="text-lg text-gray-400 mb-8"),
        
        # Two-column layout
        Div(
            # Left: Scenario Selection
            Div(
                scenario_selector(current_scenario or "Creator-First Platform", source="governance"),
                cls="space-y-4"
            ),
            
            # Right: Policy Controls + Transparency
            Div(
                policy_controls(cfg.mode, cfg),
                transparency_panel(cfg, events),
                cls="space-y-4"
            ),
            
            cls="grid grid-cols-1 lg:grid-cols-2 gap-6"
        ),
        
        cls="max-w-7xl mx-auto p-6"
    )
    
    return content