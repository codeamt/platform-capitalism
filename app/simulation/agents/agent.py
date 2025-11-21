from app.simulation.agents.state_machine import CreatorStateMachine, StateContext
from app.simulation.agents.strategy_selector import StrategySelector

class Agent:
    def __init__(self, profile):
        self.profile = profile
        self.state_machine = CreatorStateMachine(self)
        self.selector = StrategySelector()
        self.history = []
        self.decision_trace = []

    def update_state(self, rewards, policy_cfg):
        ctx = StateContext(
            arousal=self.profile.arousal_level,
            addiction=self.profile.addiction_drive,
            burnout=self.profile.burnout,
            resilience=self.profile.emotional_resilience,
            quality=rewards.get("quality", 0),
            diversity=rewards.get("diversity", 0),
            consistency=rewards.get("consistency", 0)
        )
        next_state = self.state_machine.compute_transition(ctx, rewards, policy_cfg)
        self.profile.current_state = next_state
        self.profile.strategy = self.selector.select(self)
        self.history.append({"tick": len(self.history), "state": next_state.name, **rewards})
        return next_state

    def as_dict(self):
        return {
            "id": self.profile.id,
            "state": self.profile.current_state.name,
            "arousal": self.profile.arousal_level,
            "burnout": self.profile.burnout,
            "strategy": self.profile.strategy
        }
