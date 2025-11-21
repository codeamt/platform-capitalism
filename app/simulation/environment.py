import random
from app.simulation.policy_engine import PolicyEngine, PolicyConfig
from app.simulation.agents.agent import Agent

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

    def volatility(self):
        return compute_volatility()

    def tick(self):
        """Run a single simulation tick: apply rewards, update state, record telemetry."""
        self.last_tick_explanations = []
        for agent in self.agents:
            rewards = self.policy_engine.apply(agent, self)
            update_state_history(agent)
            agent.history.append({
                "state": agent.profile.current_state.name,
                **rewards
            })

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def summary(self):
        return {
            "num_agents": len(self.agents),
            "avg_burnout": sum(a.profile.burnout for a in self.agents) / len(self.agents) if self.agents else 0,
            "avg_arousal": sum(a.profile.arousal_level for a in self.agents) / len(self.agents) if self.agents else 0,
            "current_regime": self.policy_engine.config.mode,
        }

# Global environment instance for use across UI
GLOBAL_ENVIRONMENT = Environment()