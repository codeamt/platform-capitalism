from dataclasses import dataclass, field
from app.simulation.agents.state_machine import CreatorState

@dataclass
class AgentProfile:
    id: int
    arousal_level: float = 0.5
    addiction_drive: float = 0.5
    burnout: float = 0.3
    emotional_resilience: float = 0.7
    quality: float = 0.5
    diversity: float = 0.5
    consistency: float = 0.5
    strategy: str = "neutral"
    current_state: CreatorState = field(default_factory=lambda: CreatorState.OPTIMIZER)
    state_history: list = field(default_factory=list)
