from simulation.policy_engine.config import PolicyConfig
import random

class PolicyEngine:
    """Platform reward policy engine.
    
    Implements three reinforcement strategies:
    1. Differential: Predictable rewards for specific behaviors (GOOD)
    2. Intermittent: Unpredictable rewards that drive addiction (BAD)
    3. Hybrid: Mix of both approaches (COMPROMISE)
    """
    
    def __init__(self, config: PolicyConfig):
        self.config = config
        self.reward_history = []  # Track reward patterns for analysis

    # ---------------------------------------------------------
    # Main reward computation hook
    # ---------------------------------------------------------
    def compute_rewards(self, agent, env):
        """Compute rewards based on policy mode.
        
        Differential mode: Transparent, predictable rewards
        Intermittent mode: Unpredictable, addictive rewards
        Hybrid mode: Blend of both
        """
        p = self.config
        pr = agent.profile

        # Base differential rewards (the "good" approach)
        base_rewards = {
            "quality": pr.quality * p.quality_weight,
            "diversity": pr.diversity * p.diversity_weight,
            "consistency": pr.consistency * p.consistency_weight,
            "break_bonus": (1 - pr.burnout) * p.break_reward,
        }
        
        # Apply wellbeing modifiers (differential reinforcement cares about creator health)
        if p.mode == "differential":
            # Penalize burnout to encourage rest
            if pr.burnout > 0.7:
                base_rewards["burnout_penalty"] = -pr.burnout * p.burnout_penalty
            
            # Reward sustainable patterns
            if pr.burnout < 0.4 and pr.emotional_resilience > 0.6:
                base_rewards["sustainability_bonus"] = p.sustainability_bonus
            
            # Baseline guarantee (safety net)
            base_rewards["baseline_guarantee"] = p.baseline_guarantee
        
        # Platform volatility (affects all modes)
        base_rewards["volatility_spike"] = env.volatility() * p.volatility_weight
        
        # Apply strategy multipliers (from strategy selector)
        strategy_metrics = agent.selector.get_strategy_metrics(pr.strategy)
        base_rewards["quality"] *= strategy_metrics.get("quality", 1.0)
        base_rewards["consistency"] *= strategy_metrics.get("consistency", 1.0)
        volume_multiplier = strategy_metrics.get("volume", 1.0)

        # Apply mode-specific transformations
        if p.mode == "intermittent":
            rewards = self._apply_intermittent(base_rewards, agent)
        elif p.mode == "hybrid":
            rewards = self._apply_hybrid(base_rewards, agent)
        else:  # differential
            rewards = base_rewards
            rewards["final_reward"] = sum(rewards.values()) * volume_multiplier
            rewards["predictability"] = 1.0  # Fully predictable
        
        # Track for analysis
        self.reward_history.append({
            "agent_id": agent.profile.id,
            "mode": p.mode,
            "final_reward": rewards.get("final_reward", 0),
            "predictability": rewards.get("predictability", 0)
        })
        
        return rewards

    # ---------------------------------------------------------
    # Policy application: compute → update agent state → log
    # ---------------------------------------------------------
    def apply(self, agent, env):
        rewards = self.compute_rewards(agent, env)
        agent.update_state(rewards, self.config, current_tick=env.tick_count)

        env.last_tick_explanations.append({
            "agent_id": agent.profile.id,
            "reward_breakdown": rewards,
            "regime": self.config.mode
        })
        return rewards

    # ---------------------------------------------------------
    # Intermittent reinforcement (the "bad" approach)
    # ---------------------------------------------------------
    def _apply_intermittent(self, base_rewards, agent):
        """Apply intermittent reinforcement - unpredictable, addictive.
        
        Key characteristics:
        - Random reward delivery (like slot machines)
        - High variance when rewards do come
        - Drives addiction and anxiety
        - No transparency or predictability
        """
        p = self.config
        
        # Random chance of getting ANY reward
        if random.random() > p.intermittent_probability:
            # No reward this tick - drives anxiety and compulsive checking
            return {
                "final_reward": 0,
                "predictability": 0.0,  # Completely unpredictable
                "intermittent_miss": -0.05,  # Psychological cost of missing reward
            }
        
        # When reward DOES come, add high variance (jackpot effect)
        variance_multiplier = random.uniform(0.5, p.intermittent_variance)
        total = sum(base_rewards.values()) * variance_multiplier
        
        # Intermittent rewards are opaque - creator doesn't know WHY they got it
        return {
            "final_reward": total,
            "predictability": 0.1,  # Very low predictability
            "intermittent_hit": total * 0.2,  # Dopamine spike from unpredictability
        }
    
    # ---------------------------------------------------------
    # Hybrid mode (compromise approach)
    # ---------------------------------------------------------
    def _apply_hybrid(self, base_rewards, agent):
        """Blend differential and intermittent approaches."""
        p = self.config
        
        # Differential component (predictable)
        differential_total = sum(base_rewards.values())
        
        # Intermittent component (unpredictable)
        intermittent_result = self._apply_intermittent(base_rewards.copy(), agent)
        intermittent_total = intermittent_result.get("final_reward", 0)
        
        # Blend based on hybrid_mix parameter
        final_reward = (
            differential_total * (1 - p.hybrid_mix) + 
            intermittent_total * p.hybrid_mix
        )
        
        # Predictability is also blended
        predictability = 1.0 * (1 - p.hybrid_mix) + 0.1 * p.hybrid_mix
        
        return {
            **base_rewards,
            "final_reward": final_reward,
            "predictability": predictability,
            "differential_component": differential_total * (1 - p.hybrid_mix),
            "intermittent_component": intermittent_total * p.hybrid_mix,
        }
    
    # ---------------------------------------------------------
    # Analysis helpers
    # ---------------------------------------------------------
    def get_reward_statistics(self):
        """Get statistics about reward patterns for analysis."""
        if not self.reward_history:
            return {}
        
        rewards = [r["final_reward"] for r in self.reward_history]
        predictability = [r["predictability"] for r in self.reward_history]
        
        return {
            "mean_reward": sum(rewards) / len(rewards) if rewards else 0,
            "reward_variance": self._variance(rewards),
            "mean_predictability": sum(predictability) / len(predictability) if predictability else 0,
            "total_ticks": len(self.reward_history),
        }
    
    def _variance(self, data):
        """Calculate variance of a list."""
        if not data:
            return 0
        mean = sum(data) / len(data)
        return sum((x - mean) ** 2 for x in data) / len(data)