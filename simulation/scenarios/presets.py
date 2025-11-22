from simulation.scenarios.base import Scenario
from simulation.policy_engine.config import PolicyConfig

# ----------------------------------------------
# SCENARIO DEFINITIONS
# Research Goal: Demonstrate differential > intermittent
# ----------------------------------------------
ALL_SCENARIOS = {

    # === EXPLOITATIVE SYSTEMS (Intermittent Reinforcement) ===
    
    "Algorithmic Slot Machine": Scenario(
        name="Algorithmic Slot Machine",
        description="Pure intermittent reinforcement - unpredictable viral hits drive addiction and burnout. Mimics TikTok/Instagram algorithms.",
        policy=PolicyConfig(
            mode="intermittent",
            quality_weight=0.2,
            diversity_weight=0.1,
            consistency_weight=0.1,
            break_reward=0.0,  # No rest rewards
            volatility_weight=0.5,  # High algorithmic chaos
            intermittent_probability=0.2,  # Low chance of reward (more addictive)
            intermittent_variance=3.0,  # High variance (jackpot effect)
            reward_transparency=0.1,  # Opaque algorithm
            baseline_guarantee=0.0,  # No safety net
            burnout_penalty=0.0,  # Platform doesn't care
            sustainability_bonus=0.0
        ),
        agent_overrides={"arousal_level": 0.8, "addiction_drive": 0.6}
    ),
    
    "Engagement Maximizer": Scenario(
        name="Engagement Maximizer",
        description="High volatility, attention-grabbing content rewarded. Creators burn out chasing trends.",
        policy=PolicyConfig(
            mode="intermittent",
            quality_weight=0.3,
            diversity_weight=0.1,
            consistency_weight=0.1,
            break_reward=0.0,
            volatility_weight=0.6,
            intermittent_probability=0.25,
            intermittent_variance=2.5,
            reward_transparency=0.2,
            baseline_guarantee=0.0,
            burnout_penalty=0.0,
            sustainability_bonus=0.0
        ),
        agent_overrides={"arousal_level": 0.7, "burnout": 0.4}
    ),

    # === SUSTAINABLE SYSTEMS (Differential Reinforcement) ===
    
    "Creator-First Platform": Scenario(
        name="Creator-First Platform",
        description="Differential reinforcement - predictable rewards for quality, diversity, and consistency. Prioritizes creator wellbeing.",
        policy=PolicyConfig(
            mode="differential",
            quality_weight=0.3,
            diversity_weight=0.3,
            consistency_weight=0.3,
            break_reward=0.3,  # Strong rest rewards
            volatility_weight=0.0,  # Stable algorithm
            reward_transparency=1.0,  # Fully transparent
            baseline_guarantee=0.2,  # Universal basic income
            burnout_penalty=0.3,  # Actively discourages overwork
            sustainability_bonus=0.2  # Rewards healthy patterns
        ),
        agent_overrides={"emotional_resilience": 0.8, "burnout": 0.2}
    ),
    
    "Cooperative Commons": Scenario(
        name="Cooperative Commons",
        description="Emphasizes diversity and collaboration over competition. Transparent, predictable rewards.",
        policy=PolicyConfig(
            mode="differential",
            quality_weight=0.25,
            diversity_weight=0.4,  # High diversity reward
            consistency_weight=0.25,
            break_reward=0.25,
            volatility_weight=0.0,
            reward_transparency=1.0,
            baseline_guarantee=0.25,
            burnout_penalty=0.2,
            sustainability_bonus=0.15
        ),
        agent_overrides={"emotional_resilience": 0.9, "diversity": 0.7}
    ),

    # === HYBRID/COMPROMISE SYSTEMS ===
    
    "Platform in Transition": Scenario(
        name="Platform in Transition",
        description="Moving from intermittent to differential - shows the benefits of reform. 50/50 hybrid.",
        policy=PolicyConfig(
            mode="hybrid",
            hybrid_mix=0.5,  # Equal mix
            quality_weight=0.3,
            diversity_weight=0.25,
            consistency_weight=0.25,
            break_reward=0.2,
            volatility_weight=0.2,
            intermittent_probability=0.3,
            intermittent_variance=2.0,
            reward_transparency=0.6,
            baseline_guarantee=0.1,
            burnout_penalty=0.1,
            sustainability_bonus=0.1
        ),
        agent_overrides={"arousal_level": 0.5, "burnout": 0.3}
    ),
    
    "Mostly Differential": Scenario(
        name="Mostly Differential",
        description="Primarily differential with some algorithmic unpredictability (70/30 split).",
        policy=PolicyConfig(
            mode="hybrid",
            hybrid_mix=0.3,  # 70% differential, 30% intermittent
            quality_weight=0.3,
            diversity_weight=0.3,
            consistency_weight=0.3,
            break_reward=0.25,
            volatility_weight=0.1,
            intermittent_probability=0.35,
            intermittent_variance=1.5,
            reward_transparency=0.8,
            baseline_guarantee=0.15,
            burnout_penalty=0.2,
            sustainability_bonus=0.15
        ),
        agent_overrides={"arousal_level": 0.4, "burnout": 0.25, "emotional_resilience": 0.75}
    ),
}

# ----------------------------------------------
# APPLY SCENARIO
# ----------------------------------------------
def load_scenario(env, name: str):
    """Load a scenario and apply it to the environment.
    
    This resets the policy and optionally modifies agent traits to
    demonstrate different platform governance approaches.
    """
    scenario = ALL_SCENARIOS.get(name)
    if not scenario:
        raise ValueError(f"Unknown scenario: {name}")
    return scenario.apply(env)

def get_scenario_comparison():
    """Get a comparison of key metrics across scenarios for analysis."""
    return {
        name: {
            "mode": scenario.policy.mode,
            "transparency": scenario.policy.reward_transparency,
            "baseline_guarantee": scenario.policy.baseline_guarantee,
            "burnout_penalty": scenario.policy.burnout_penalty,
            "intermittent_prob": scenario.policy.intermittent_probability if scenario.policy.mode != "differential" else None,
        }
        for name, scenario in ALL_SCENARIOS.items()
    }