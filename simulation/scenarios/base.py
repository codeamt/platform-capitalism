from dataclasses import dataclass
from simulation.policy_engine.config import PolicyConfig

@dataclass
class Scenario:
    name: str
    description: str
    policy: PolicyConfig
    agent_overrides: dict | None = None  # modify agent traits

    def apply(self, env):
        # Apply policy config
        env.policy_engine.config = self.policy
        
        # Track which scenario is loaded
        env.current_scenario = self.name

        # Optionally modify agent traits
        if self.agent_overrides:
            for agent in env.agents:
                for k, v in self.agent_overrides.items():
                    setattr(agent.profile, k, v)

        return env