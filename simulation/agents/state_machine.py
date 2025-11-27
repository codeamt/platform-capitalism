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
    """Probabilistic state machine for creator behavior.
    
    States represent different creator mindsets:
    - OPTIMIZER: Balanced, consistent content creation
    - HUSTLER: High-output, chasing engagement
    - TRUE_BELIEVER: Creative experimentation, intrinsic motivation
    - BURNOUT: Exhausted, reduced activity
    """
    
    def __init__(self, agent):
        self.agent = agent

    def compute_transition(self, ctx: StateContext, rewards, policy_cfg):
        """Compute probabilistic state transition based on context and rewards.
        
        Args:
            ctx: Current agent context (arousal, burnout, etc.)
            rewards: Reward breakdown from policy engine
            policy_cfg: Current policy configuration
            
        Returns:
            CreatorState: The next state based on weighted probabilities
        """
        # Compute transition scores for each state
        transitions = {
            CreatorState.HUSTLER: (
                ctx.arousal * 0.4 + 
                ctx.addiction * 0.6 + 
                rewards.get("quality", 0) * 0.3
            ),
            CreatorState.OPTIMIZER: (
                ctx.consistency * 0.5 + 
                ctx.resilience * 0.5 + 
                rewards.get("consistency", 0) * 0.4
            ),
            CreatorState.TRUE_BELIEVER: (
                ctx.diversity * 0.5 +  # Increased from 0.4
                ctx.quality * 0.5 +     # Increased from 0.4
                (1 - ctx.addiction) * 0.4  # Increased from 0.2 to make this state more accessible
            ),
            CreatorState.BURNOUT: (
                ctx.burnout * 0.7 + 
                (1 - ctx.resilience) * 0.3
            ),
        }
        
        # Add state persistence bonus (hysteresis) - agents tend to stay in current state
        # This prevents rapid state flipping and creates more realistic behavior patterns
        current_state = self.agent.profile.current_state
        persistence_bonus = 0.25  # 25% bonus to current state score
        if current_state in transitions:
            transitions[current_state] += persistence_bonus
        
        # Add small random noise to each transition score (platform algorithm variability)
        for state in transitions:
            transitions[state] += random.gauss(0, 0.05)
        
        # Normalize to probabilities
        total = sum(transitions.values()) + 1e-6  # Avoid division by zero
        probs = {state: score / total for state, score in transitions.items()}
        
        # Sample from probability distribution
        rnd = random.random()
        cumulative = 0.0
        for state, prob in probs.items():
            cumulative += prob
            if rnd < cumulative:
                return state
        
        # Fallback (should rarely happen)
        return self.agent.profile.current_state
    
    def get_transition_probabilities(self, ctx: StateContext, rewards):
        """Get current transition probabilities without sampling.
        
        Useful for debugging and visualization.
        """
        transitions = {
            CreatorState.HUSTLER: ctx.arousal * 0.4 + ctx.addiction * 0.6 + rewards.get("quality", 0) * 0.3,
            CreatorState.OPTIMIZER: ctx.consistency * 0.5 + ctx.resilience * 0.5 + rewards.get("consistency", 0) * 0.4,
            CreatorState.TRUE_BELIEVER: ctx.diversity * 0.4 + ctx.quality * 0.4 + (1 - ctx.addiction) * 0.2,
            CreatorState.BURNOUT: ctx.burnout * 0.7 + (1 - ctx.resilience) * 0.3,
        }
        total = sum(transitions.values()) + 1e-6
        return {state.name: round(score / total, 3) for state, score in transitions.items()}