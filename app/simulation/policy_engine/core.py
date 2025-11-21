from app.simulation.policy_engine.config import PolicyConfig

class PolicyEngine:
    def __init__(self, config: PolicyConfig):
        self.config = config

    # ---------------------------------------------------------
    # Main reward computation hook
    # ---------------------------------------------------------
    def compute_rewards(self, agent, env):
        p = self.config
        pr = agent.profile

        # Base differential rewards
        rewards = {
            "quality": pr.quality * p.quality_weight,
            "diversity": pr.diversity * p.diversity_weight,
            "consistency": pr.consistency * p.consistency_weight,
            "break_bonus": (1 - pr.burnout) * p.break_reward,
            "volatility_spike": env.volatility() * p.volatility_weight,
        }

        # Intermittent reinforcement modifier
        if p.mode == "intermittent":
            rewards = self._apply_intermittent(rewards)

        # Hybrid mode blending
        if p.mode == "hybrid":
            differential = sum(rewards.values())
            intermittent = self._apply_intermittent(rewards.copy())
            rewards = self._blend_hybrid(differential, intermittent)

        rewards["final_reward"] = sum(rewards.values())
        return rewards

    # ---------------------------------------------------------
    # Policy application: compute → update agent state → log
    # ---------------------------------------------------------
    def apply(self, agent, env):
        rewards = self.compute_rewards(agent, env)
        agent.update_state(rewards, self.config)

        env.last_tick_explanations.append({
            "agent_id": agent.profile.id,
            "reward_breakdown": rewards,
            "regime": self.config.mode
        })
        return rewards

    # ---------------------------------------------------------
    # Intermittent reinforcement helper
    # ---------------------------------------------------------
    def _apply_intermittent(self, rewards):
        import random
        if random.random() > self.config.intermittent_probability:
            # No reward delivered this tick
            return {k: 0 for k in rewards}
        return rewards

    # ---------------------------------------------------------
    # Hybrid mode blending helper
    # ---------------------------------------------------------
    def _blend_hybrid(self, diff_reward, intermittent_reward):
        p = self.config.hybrid_mix
        return {
            "hybrid": diff_reward * (1 - p) + intermittent_reward["final_reward"] * p
        }