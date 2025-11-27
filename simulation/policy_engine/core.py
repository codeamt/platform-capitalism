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
        }
        
        # Content volume reward (based on posts generated this tick)
        posts_generated = getattr(agent, '_current_tick_posts', 1.0)  # Default to 1.0 if not set
        # Normalize posts_generated (typically 0-10 range) to a 0-1 scale for reward calculation
        normalized_volume = min(1.0, posts_generated / 10.0)
        base_rewards["volume"] = normalized_volume * p.volume_weight  # Volume contributes to rewards
        
        # Break reward: Reward agents for resting when burned out
        # If burnout is high (>0.5) and volume is low (<0.3), reward the break
        if pr.burnout > 0.5 and normalized_volume < 0.3:
            base_rewards["break_bonus"] = pr.burnout * p.break_reward  # Higher burnout = bigger break reward
        else:
            base_rewards["break_bonus"] = 0.0
        
        # Monetary reward: Simulates platform payments (CPM, ad revenue, tips, etc.)
        # Base payment per post, with bonuses for quality and engagement
        if posts_generated > 0:
            # Base payment per post
            base_payment = posts_generated * p.base_payment
            
            # Quality bonus: High quality content gets paid more
            quality_bonus = 1.0 + (pr.quality * (p.quality_bonus_multiplier - 1.0))
            
            # Engagement bonus: Consistency + diversity proxy for audience engagement
            engagement_score = (pr.consistency + pr.diversity) / 2.0
            engagement_bonus = 1.0 + (engagement_score * (p.engagement_multiplier - 1.0))
            
            # Total monetary reward (normalized 0-1 scale)
            base_rewards["monetary"] = base_payment * quality_bonus * engagement_bonus
            
            # CPM-based earnings (realistic dollar amounts)
            if p.enable_cpm_earnings:
                # Calculate total views: posts × avg_views_per_post
                total_views = posts_generated * p.avg_views_per_post
                
                # Base CPM earnings: (views / 1000) × CPM rate
                base_cpm_earnings = (total_views / 1000.0) * p.cpm_rate
                
                # Apply quality and engagement multipliers
                # High quality + high engagement = more views/better CPM
                final_cpm_earnings = base_cpm_earnings * quality_bonus * engagement_bonus
                
                # Store earnings in dollars (not normalized)
                base_rewards["cpm_earnings"] = round(final_cpm_earnings, 2)
            else:
                base_rewards["cpm_earnings"] = 0.0
        else:
            base_rewards["monetary"] = 0.0
            base_rewards["cpm_earnings"] = 0.0
        
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
        base_rewards["volume"] *= volume_multiplier  # Apply volume strategy multiplier

        # === PLATFORM ALGORITHM NOISE ===
        # Real platforms have algorithmic variability (A/B tests, recommendation randomness)
        algorithm_noise = random.gauss(1.0, 0.25)  # ±25% variance from algorithm
        
        # === VIRAL MECHANICS ===
        # Exceptional content can go viral (power-law distribution)
        viral_multiplier = 1.0
        if pr.quality > 0.75 and pr.diversity > 0.65:
            # High quality + diverse content has viral potential
            # Use Pareto distribution for long-tail viral hits
            viral_roll = random.random()
            if viral_roll < 0.05:  # 5% chance of viral content
                viral_multiplier = random.paretovariate(1.5)  # Power-law: most 1-3x, rare 10x+
        
        # === CONTENT FAILURE PENALTY ===
        # Low quality content can backfire (negative engagement, backlash)
        failure_penalty = 0.0
        if pr.quality < 0.3 or pr.consistency < 0.2:
            # Poor quality or inconsistent content gets penalized
            failure_penalty = -random.uniform(0.05, 0.15)
        
        # Apply mode-specific transformations
        if p.mode == "intermittent":
            rewards = self._apply_intermittent(base_rewards, agent, algorithm_noise, viral_multiplier, failure_penalty)
        elif p.mode == "hybrid":
            rewards = self._apply_hybrid(base_rewards, agent, algorithm_noise, viral_multiplier, failure_penalty)
        else:  # differential
            rewards = base_rewards
            # Calculate final_reward excluding cpm_earnings (it's a tracking metric, not a reward)
            reward_sum = sum(v for k, v in rewards.items() if k != "cpm_earnings")
            # Apply variance and viral mechanics
            final_reward = (reward_sum * volume_multiplier * algorithm_noise * viral_multiplier) + failure_penalty
            rewards["final_reward"] = final_reward
            rewards["predictability"] = 0.85  # High but not perfect (algorithm still has some variance)
            rewards["algorithm_variance"] = algorithm_noise
            rewards["viral_multiplier"] = viral_multiplier
            if failure_penalty < 0:
                rewards["failure_penalty"] = failure_penalty
        
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
    def _apply_intermittent(self, base_rewards, agent, algorithm_noise, viral_multiplier, failure_penalty):
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
                "final_reward": failure_penalty,  # Can still get failure penalty
                "predictability": 0.0,  # Completely unpredictable
                "intermittent_miss": -0.05,  # Psychological cost of missing reward
            }
        
        # When reward DOES come, add high variance (jackpot effect)
        variance_multiplier = random.uniform(0.5, p.intermittent_variance)
        # Exclude cpm_earnings from reward sum (it's a tracking metric)
        reward_sum = sum(v for k, v in base_rewards.items() if k != "cpm_earnings")
        # Apply all variance sources (intermittent, algorithm, viral)
        total = (reward_sum * variance_multiplier * algorithm_noise * viral_multiplier) + failure_penalty
        
        # Intermittent rewards are opaque - creator doesn't know WHY they got it
        result = {
            "final_reward": total,
            "predictability": 0.1,  # Very low predictability
            "intermittent_hit": total * 0.2 if total > 0 else 0,  # Dopamine spike from unpredictability
            "algorithm_variance": algorithm_noise,
            "viral_multiplier": viral_multiplier
        }
        if failure_penalty < 0:
            result["failure_penalty"] = failure_penalty
        # Preserve cpm_earnings for tracking
        if "cpm_earnings" in base_rewards:
            result["cpm_earnings"] = base_rewards["cpm_earnings"]
        return result
    
    # ---------------------------------------------------------
    # Hybrid mode (compromise approach)
    # ---------------------------------------------------------
    def _apply_hybrid(self, base_rewards, agent, algorithm_noise, viral_multiplier, failure_penalty):
        """Blend differential and intermittent approaches."""
        p = self.config
        
        # Differential component (predictable with some variance)
        # Exclude cpm_earnings from reward sum
        reward_sum = sum(v for k, v in base_rewards.items() if k != "cpm_earnings")
        differential_total = (reward_sum * algorithm_noise * viral_multiplier) + failure_penalty
        
        # Intermittent component (unpredictable)
        intermittent_result = self._apply_intermittent(base_rewards.copy(), agent, algorithm_noise, viral_multiplier, failure_penalty)
        intermittent_total = intermittent_result.get("final_reward", 0)
        
        # Blend based on hybrid_mix parameter
        blended_total = (differential_total * p.hybrid_mix) + (intermittent_total * (1 - p.hybrid_mix))
        
        result = {
            "final_reward": blended_total,
            "predictability": p.hybrid_mix * 0.7,  # Predictability scales with differential weight (but never perfect)
            "differential_component": differential_total * p.hybrid_mix,
            "intermittent_component": intermittent_total * (1 - p.hybrid_mix),
            "algorithm_variance": algorithm_noise,
            "viral_multiplier": viral_multiplier
        }
        if failure_penalty < 0:
            result["failure_penalty"] = failure_penalty
        # Preserve cpm_earnings for tracking
        if "cpm_earnings" in base_rewards:
            result["cpm_earnings"] = base_rewards["cpm_earnings"]
        return result
    
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