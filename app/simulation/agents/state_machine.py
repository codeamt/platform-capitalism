from enum import Enum, auto
from dataclasses import dataclass
import random

class CreatorState(Enum):
    OPTIMIZER = auto()
    HUSTLER = auto()
    TRUE_BELIEVER = auto()
    BURNOUT = auto()

@dataclass
class StateContext:
    arousal: float
    addiction: float
    burnout: float
    resilience: float
    quality: float
    diversity: float
    consistency: float

class CreatorStateMachine:
    def __init__(self, agent):
        self.agent = agent
        self.state = CreatorState.OPTIMIZER

    def compute_transition(self, ctx: StateContext, rewards, policy_cfg):
        transitions = {
            CreatorState.HUSTLER: ctx.arousal * 0.4 + ctx.addiction * 0.6 + rewards.get("quality", 0) * 0.3,
            CreatorState.OPTIMIZER: ctx.consistency * 0.5 + ctx.resilience * 0.5 + rewards.get("consistency", 0) * 0.4,
            CreatorState.TRUE_BELIEVER: ctx.diversity * 0.4 + ctx.quality * 0.4 + (1 - ctx.addiction) * 0.2,
            CreatorState.BURNOUT: ctx.burnout * 0.7 + (1 - ctx.resilience) * 0.3,
        }
        total = sum(transitions.values()) + 1e-6
        probs = {s: v / total for s, v in transitions.items()}
        rnd = random.random()
        cumulative = 0.0
        for s, p in probs.items():
            cumulative += p
            if rnd < cumulative:
                self.state = s
                return s
        return self.state

    def as_dict(self):
        return {"state": self.state.name}