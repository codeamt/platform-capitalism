import random
from simulation.policy_engine import PolicyEngine, PolicyConfig
from simulation.agents.agent import Agent

# Utility: compute platform volatility
def compute_volatility():
    return random.random() * 0.5

# Utility: ensure state history tracking
def ensure_state_history(agent):
    if not hasattr(agent.profile, "state_history"):
        agent.profile.state_history = []

# Utility: update agent's state history after each tick
def update_state_history(agent):
    ensure_state_history(agent)
    if agent.profile.state_history and agent.profile.state_history[-1][0] == agent.profile.current_state.name:
        state, duration = agent.profile.state_history[-1]
        agent.profile.state_history[-1] = (state, duration + 1)
    else:
        agent.profile.state_history.append((agent.profile.current_state.name, 1))

# Main Environment Class
class Environment:
    def __init__(self, agents=None):
        self.agents = agents or []
        self.policy_engine = PolicyEngine(PolicyConfig())
        self.last_tick_explanations = []
        self.tick_count = 0
        
        # History tracking for charts (last 20 ticks)
        self.history = {
            "ticks": [],
            "health_score": [],
            "avg_burnout": [],
            "avg_addiction": [],
            "avg_resilience": [],
            "state_distribution": [],  # List of dicts
            "avg_reward": [],
        }
        self.max_history_length = 20

    def volatility(self):
        return compute_volatility()

    def tick(self):
        """Run a single simulation tick: apply rewards, update state, record telemetry."""
        self.last_tick_explanations = []
        self.tick_count += 1
        
        for agent in self.agents:
            self.policy_engine.apply(agent, self)  # Updates agent state and logs telemetry
            update_state_history(agent)
        
        # Record history for charts
        self._record_history()

    def add_agent(self, agent: Agent):
        self.agents.append(agent)
    
    def _record_history(self):
        """Record current state to history for time-series charts."""
        if not self.agents:
            return
        
        summary = self.summary()
        
        # Append current metrics
        self.history["ticks"].append(self.tick_count)
        self.history["health_score"].append(summary["system_health_score"])
        self.history["avg_burnout"].append(summary["avg_burnout"])
        self.history["avg_addiction"].append(summary["avg_addiction"])
        self.history["avg_resilience"].append(summary["avg_resilience"])
        self.history["state_distribution"].append(summary["state_distribution"])
        
        # Calculate average reward from last tick
        if self.agents and self.agents[0].history:
            avg_reward = sum(a.history[-1].get("final_reward", 0) for a in self.agents) / len(self.agents)
            self.history["avg_reward"].append(avg_reward)
        else:
            self.history["avg_reward"].append(0)
        
        # Keep only last N entries
        for key in self.history:
            if len(self.history[key]) > self.max_history_length:
                self.history[key] = self.history[key][-self.max_history_length:]

    def summary(self):
        """Get comprehensive summary of simulation state.
        
        Returns key metrics for evaluating differential vs intermittent reinforcement:
        - Creator wellbeing (burnout, addiction, resilience)
        - System characteristics (predictability, transparency)
        - State distribution
        """
        if not self.agents:
            return {"num_agents": 0, "current_regime": self.policy_engine.config.mode}
        
        from simulation.agents.state_machine import CreatorState
        
        # State distribution
        state_counts = {state: 0 for state in CreatorState}
        for agent in self.agents:
            state_counts[agent.profile.current_state] += 1
        
        # Wellbeing metrics (key research outcomes)
        avg_burnout = sum(a.profile.burnout for a in self.agents) / len(self.agents)
        avg_addiction = sum(a.profile.addiction_drive for a in self.agents) / len(self.agents)
        avg_resilience = sum(a.profile.emotional_resilience for a in self.agents) / len(self.agents)
        avg_arousal = sum(a.profile.arousal_level for a in self.agents) / len(self.agents)
        
        # System health score (0-1, higher is better)
        # Good: low burnout, low addiction, high resilience
        system_health = (
            (1 - avg_burnout) * 0.4 +
            (1 - avg_addiction) * 0.3 +
            avg_resilience * 0.3
        )
        
        # Get policy engine statistics
        reward_stats = self.policy_engine.get_reward_statistics()
        
        return {
            # Basic info
            "num_agents": len(self.agents),
            "current_regime": self.policy_engine.config.mode,
            
            # Wellbeing metrics (RESEARCH OUTCOMES)
            "avg_burnout": round(avg_burnout, 3),
            "avg_addiction": round(avg_addiction, 3),
            "avg_resilience": round(avg_resilience, 3),
            "avg_arousal": round(avg_arousal, 3),
            "system_health_score": round(system_health, 3),
            
            # State distribution
            "state_distribution": {state.name: count for state, count in state_counts.items()},
            "burnout_rate": round(state_counts[CreatorState.BURNOUT] / len(self.agents), 3),
            
            # Reward characteristics
            "avg_reward": round(reward_stats.get("mean_reward", 0), 3),
            "reward_predictability": round(reward_stats.get("mean_predictability", 0), 3),
            "reward_variance": round(reward_stats.get("reward_variance", 0), 3),
            
            # Policy characteristics
            "transparency": self.policy_engine.config.reward_transparency,
            "baseline_guarantee": self.policy_engine.config.baseline_guarantee,
        }

# Global environment instance for use across UI
GLOBAL_ENVIRONMENT = Environment()