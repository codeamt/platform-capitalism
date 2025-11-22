from dataclasses import dataclass

@dataclass
class PolicyConfig:
    """Platform reward policy configuration.
    
    Modes:
    - differential: Predictable rewards for specific behaviors (quality, diversity, consistency)
    - intermittent: Unpredictable rewards (like slot machines, drives addiction)
    - hybrid: Mix of both approaches
    
    Research Goal: Demonstrate that differential reinforcement creates healthier,
    more sustainable creator ecosystems than intermittent reinforcement.
    """
    
    mode: str = "differential"   # differential | intermittent | hybrid
    
    # Differential reinforcement weights (rewarding specific behaviors)
    quality_weight: float = 0.3      # Reward high-quality content
    diversity_weight: float = 0.2    # Reward diverse, novel content
    consistency_weight: float = 0.3  # Reward regular, reliable posting
    break_reward: float = 0.1        # Reward taking breaks (anti-burnout)
    
    # Platform volatility (algorithmic unpredictability)
    volatility_weight: float = 0.1   # How much random algorithm changes affect rewards
    
    # Intermittent reinforcement parameters (the "bad" approach)
    intermittent_probability: float = 0.3  # Chance of getting reward (lower = more addictive)
    intermittent_variance: float = 2.0     # Reward variance multiplier (higher = more unpredictable)
    
    # Hybrid mode parameters
    hybrid_mix: float = 0.5   # 0 = pure differential, 1 = pure intermittent
    
    # Fairness and transparency settings
    reward_transparency: float = 1.0  # How clear rewards are to creators (0-1)
    baseline_guarantee: float = 0.0   # Minimum reward floor (safety net)
    
    # Creator wellbeing parameters
    burnout_penalty: float = 0.0      # Penalty for high burnout (encourages rest)
    sustainability_bonus: float = 0.0  # Bonus for maintaining healthy patterns