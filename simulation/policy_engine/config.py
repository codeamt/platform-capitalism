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
    volume_weight: float = 0.15      # Reward content volume (posts generated)
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
    
    # Creator wellbeing parameters (OPTIMAL SUSTAINABILITY SETTINGS)
    burnout_penalty: float = 0.40      # Penalty for high burnout (encourages rest)
    sustainability_bonus: float = 0.10  # Bonus for maintaining healthy patterns
    
    # Monetary reward parameters (simulates platform payments)
    base_payment: float = 0.05         # Base payment per post (normalized 0-1 scale)
    quality_bonus_multiplier: float = 1.5  # Multiplier for high-quality content
    engagement_multiplier: float = 1.0     # Multiplier based on consistency/diversity (proxy for engagement)
    
    # CPM-based earnings (realistic creator economy metrics)
    cpm_rate: float = 10.0             # Cost per mille ($/1000 views) - range: $2-$40
    avg_views_per_post: float = 5000   # Average views per post (varies by audience size)
    enable_cpm_earnings: bool = True   # Toggle CPM-based earnings calculation


# Optimal Policy Configuration Preset
# This configuration maximizes aggregate content creation while minimizing agent burnout.
# It creates a self-regulating system where agents are rewarded for productivity but
# strongly deterred from crossing into high burnout territory.
OPTIMAL_POLICY_CONFIG = PolicyConfig(
    mode="differential",
    quality_weight=0.3,
    diversity_weight=0.2,
    consistency_weight=0.3,
    volume_weight=0.15,        # Reward content generation
    break_reward=0.1,
    burnout_penalty=0.40,      # Strong negative weight for sustainability
    sustainability_bonus=0.10,  # Bonus for healthy patterns
    baseline_guarantee=0.0,
    reward_transparency=1.0,
    base_payment=0.05,         # Fair payment per post
    quality_bonus_multiplier=1.5,  # Moderate quality bonus
    engagement_multiplier=1.0,     # No engagement penalty/bonus
    cpm_rate=10.0,             # Mid-range CPM (balanced market)
    avg_views_per_post=5000,   # Moderate audience size
    enable_cpm_earnings=True
)


# ----------------------------------------------
# POLICY PRESETS FOR GOVERNANCE LAB
# ----------------------------------------------

POLICY_PRESETS = {
    "optimal": {
        "name": "🌱 Optimal Sustainability",
        "description": "Maximizes content creation while minimizing burnout. Strong guardrails for creator wellbeing.",
        "config": OPTIMAL_POLICY_CONFIG
    },
    
    "exploitative": {
        "name": "🎰 Exploitative (Intermittent)",
        "description": "Unpredictable rewards drive addiction and burnout. Mimics algorithmic slot machines.",
        "config": PolicyConfig(
            mode="intermittent",
            quality_weight=0.2,
            diversity_weight=0.1,
            consistency_weight=0.1,
            volume_weight=0.3,         # High volume reward (exploitative)
            break_reward=0.0,
            volatility_weight=0.5,
            intermittent_probability=0.2,  # Low chance = more addictive
            intermittent_variance=3.0,     # High variance = jackpot effect
            reward_transparency=0.1,
            baseline_guarantee=0.0,
            burnout_penalty=0.0,           # Platform doesn't care
            sustainability_bonus=0.0,
            base_payment=0.02,             # Low base payment (exploitative)
            quality_bonus_multiplier=2.5,  # High quality bonus (forces quality grind)
            engagement_multiplier=1.5,     # High engagement requirement
            cpm_rate=5.0,                  # Low CPM (exploitative, low-value market)
            avg_views_per_post=3000,       # Smaller audience (harder to grow)
            enable_cpm_earnings=True
        )
    },
    
    "balanced": {
        "name": "🔀 Balanced Hybrid",
        "description": "Mix of predictable and unpredictable rewards. Moderate wellbeing support.",
        "config": PolicyConfig(
            mode="hybrid",
            hybrid_mix=0.5,  # 50/50 split
            quality_weight=0.3,
            diversity_weight=0.25,
            consistency_weight=0.25,
            volume_weight=0.2,         # Moderate volume reward
            break_reward=0.2,
            volatility_weight=0.2,
            intermittent_probability=0.3,
            intermittent_variance=2.0,
            reward_transparency=0.6,
            baseline_guarantee=0.1,
            burnout_penalty=0.15,
            sustainability_bonus=0.1,
            base_payment=0.04,             # Moderate payment
            quality_bonus_multiplier=1.8,  # Moderate quality bonus
            engagement_multiplier=1.2,     # Moderate engagement bonus
            cpm_rate=15.0,                 # Good CPM (competitive market)
            avg_views_per_post=7000,       # Growing audience
            enable_cpm_earnings=True
        )
    },
    
    "cooperative": {
        "name": "🤝 Cooperative Commons",
        "description": "Emphasizes diversity and collaboration. Transparent, predictable, and supportive.",
        "config": PolicyConfig(
            mode="differential",
            quality_weight=0.25,
            diversity_weight=0.4,  # High diversity reward
            consistency_weight=0.25,
            volume_weight=0.1,         # Low volume reward (quality over quantity)
            break_reward=0.25,
            volatility_weight=0.0,
            reward_transparency=1.0,
            baseline_guarantee=0.25,  # Universal basic income
            burnout_penalty=0.3,
            sustainability_bonus=0.2,
            base_payment=0.08,             # High base payment (equitable)
            quality_bonus_multiplier=1.2,  # Low quality bonus (less competitive)
            engagement_multiplier=1.0,     # No engagement pressure
            cpm_rate=20.0,                 # High CPM (premium market, North America)
            avg_views_per_post=10000,      # Large, engaged audience
            enable_cpm_earnings=True
        )
    }
}


def get_preset(preset_name: str) -> PolicyConfig:
    """Get a policy preset configuration by name.
    
    Args:
        preset_name: Name of preset ("optimal", "exploitative", "balanced", "cooperative")
        
    Returns:
        PolicyConfig instance
        
    Raises:
        ValueError: If preset_name is not found
    """
    preset = POLICY_PRESETS.get(preset_name)
    if not preset:
        raise ValueError(f"Unknown preset: {preset_name}. Available: {list(POLICY_PRESETS.keys())}")
    return preset["config"]