from dataclasses import dataclass

@dataclass
class PolicyConfig:
    mode: str = "differential"   # differential | intermittent | hybrid
    quality_weight: float = 0.3
    diversity_weight: float = 0.2
    consistency_weight: float = 0.3
    break_reward: float = 0.1
    volatility_weight: float = 0.1

    # Intermittent reinforcement parameters
    intermittent_probability: float = 0.3

    # Hybrid mode parameters
    hybrid_mix: float = 0.5   # 0 = pure differential, 1 = pure intermittent