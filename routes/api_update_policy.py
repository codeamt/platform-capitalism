from fasthtml.common import APIRouter
from simulation.environment import GLOBAL_ENVIRONMENT
from simulation.policy_engine.config import PolicyConfig
from ui.pages.dashboard import DashboardPage
from ui.pages.governance_lab import GovernanceLabPage

rt = APIRouter()

@rt("/api/update-policy", methods=["POST"])
def update_policy(
    quality_weight: float = None,
    diversity_weight: float = None,
    consistency_weight: float = None,
    break_reward: float = None,
    burnout_penalty: float = None,
    sustainability_bonus: float = None,
    baseline_guarantee: float = None,
    intermittent_probability: float = None,
    intermittent_variance: float = None,
):
    """Update policy configuration and return updated governance lab content."""
    cfg = GLOBAL_ENVIRONMENT.policy_engine.config

    # Update only provided parameters
    if quality_weight is not None:
        cfg.quality_weight = quality_weight
    if diversity_weight is not None:
        cfg.diversity_weight = diversity_weight
    if consistency_weight is not None:
        cfg.consistency_weight = consistency_weight
    if break_reward is not None:
        cfg.break_reward = break_reward
    if burnout_penalty is not None:
        cfg.burnout_penalty = burnout_penalty
    if sustainability_bonus is not None:
        cfg.sustainability_bonus = sustainability_bonus
    if baseline_guarantee is not None:
        cfg.baseline_guarantee = baseline_guarantee
    if intermittent_probability is not None:
        cfg.intermittent_probability = intermittent_probability
    if intermittent_variance is not None:
        cfg.intermittent_variance = intermittent_variance

    GLOBAL_ENVIRONMENT.policy_engine.config = cfg
    return GovernanceLabPage()

@rt("/api/tick", methods=["POST"])
def run_tick():
    """Run a single simulation tick and return updated dashboard."""
    GLOBAL_ENVIRONMENT.tick()
    return DashboardPage()

@rt("/api/reset", methods=["POST"])
def reset_simulation():
    """Reset the simulation and return updated dashboard."""
    # Reset all agents to initial state
    for agent in GLOBAL_ENVIRONMENT.agents:
        agent.history = []
        # Reset traits to initial values
        agent.profile.burnout = 0.0
        agent.profile.arousal = 0.5
        agent.profile.addiction_drive = agent.profile.addiction_drive  # Keep personality trait
    
    GLOBAL_ENVIRONMENT.tick_count = 0
    GLOBAL_ENVIRONMENT.last_tick_explanations = []
    
    return DashboardPage()