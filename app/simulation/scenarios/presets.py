from app.simulation.scenarios.base import Scenario
from app.simulation.policy_engine.config import PolicyConfig

# ----------------------------------------------
# SCENARIO DEFINITIONS
# ----------------------------------------------
ALL_SCENARIOS = {

    # High-pressure markets emulate volatility-heavy influencer economy
    "High Pressure Market": Scenario(
        name="High Pressure Market",
        description="High volatility, low redistribution — resembles algorithmic arms race.",
        policy=PolicyConfig(
            mode="intermittent",
            quality_weight=0.4,
            diversity_weight=0.1,
            consistency_weight=0.2,
            break_reward=0.05,
            volatility_weight=0.4,
            intermittent_probability=0.25
        ),
        agent_overrides={"arousal_level": 0.7}
    ),

    # Fairness-oriented governance
    "Fairness Focused": Scenario(
        name="Fairness Focused",
        description="Platform prioritizes diversity and equal visibility.",
        policy=PolicyConfig(
            mode="differential",
            quality_weight=0.2,
            diversity_weight=0.5,
            consistency_weight=0.2,
            break_reward=0.2,
            volatility_weight=0.0
        ),
        agent_overrides={"emotional_resilience": 0.9}
    ),

    # Fatigue-driven markets emulate burnout cycles
    "Fatigue Cycle": Scenario(
        name="Fatigue Cycle",
        description="Creators oscillate between activity spikes and burnout phases.",
        policy=PolicyConfig(
            mode="hybrid",
            hybrid_mix=0.5,
            quality_weight=0.3,
            diversity_weight=0.3,
            consistency_weight=0.3,
            break_reward=0.3,
            volatility_weight=0.2
        ),
        agent_overrides={"burnout": 0.4}
    ),

    # Stable, low-stress environment
    "Supportive Platform": Scenario(
        name="Supportive Platform",
        description="Low volatility, high resilience reinforcement.",
        policy=PolicyConfig(
            mode="differential",
            quality_weight=0.3,
            diversity_weight=0.3,
            consistency_weight=0.4,
            break_reward=0.5,
            volatility_weight=0.0
        ),
        agent_overrides={"arousal_level": 0.3, "burnout": 0.1}
    ),
}

# ----------------------------------------------
# APPLY SCENARIO
# ----------------------------------------------
def load_scenario(env, name: str):
    scenario = ALL_SCENARIOS.get(name)
    if not scenario:
        raise ValueError(f"Unknown scenario: {name}")
    return scenario.apply(env)