from dataclasses import dataclass, field
from simulation.agents.state_machine import CreatorState
import random

@dataclass
class AgentProfile:
    id: int
    arousal_level: float = None
    addiction_drive: float = None
    burnout: float = None
    emotional_resilience: float = None
    quality: float = None
    diversity: float = None
    consistency: float = None
    strategy: str = "neutral"
    current_state: CreatorState = field(default_factory=lambda: CreatorState.OPTIMIZER)
    state_history: list = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize traits with random variation sampled from distributions.
        
        Uses normal distributions centered around typical values with reasonable
        variance to create diverse but realistic agent populations.
        """
        # Helper to sample from normal distribution and clamp to [0, 1]
        def sample(mean, std):
            return max(0.0, min(1.0, random.gauss(mean, std)))
        
        # Only initialize if not already set (allows scenario overrides)
        if self.arousal_level is None:
            self.arousal_level = sample(0.5, 0.15)  # Moderate arousal, some variation
        
        if self.addiction_drive is None:
            self.addiction_drive = sample(0.3, 0.15)  # Lower baseline, varies by personality
        
        if self.burnout is None:
            self.burnout = sample(0.2, 0.1)  # Start relatively fresh
        
        if self.emotional_resilience is None:
            self.emotional_resilience = sample(0.7, 0.15)  # Generally resilient, varies
        
        if self.quality is None:
            self.quality = sample(0.6, 0.2)  # Decent quality, wide variation
        
        if self.diversity is None:
            self.diversity = sample(0.5, 0.2)  # Moderate diversity, wide variation
        
        if self.consistency is None:
            self.consistency = sample(0.6, 0.2)  # Fairly consistent, varies by creator type
