from simulation.agents.state_machine import CreatorStateMachine, StateContext
from simulation.agents.strategy_selector import StrategySelector

class Agent:
    def __init__(self, profile):
        self.profile = profile
        self.state_machine = CreatorStateMachine(self)
        self.selector = StrategySelector()
        self.history = []
        self.decision_trace = []

    def update_state(self, rewards, policy_cfg, current_tick=None):
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
        
        # Evolve agent traits based on state and rewards
        self._evolve_traits(next_state, rewards, policy_cfg)
        
        # Record history with trait snapshots for sparklines
        self.history.append({
            "tick": current_tick if current_tick is not None else len(self.history),
            "state": next_state.name,
            "burnout": self.profile.burnout,
            "addiction": self.profile.addiction_drive,
            "resilience": self.profile.emotional_resilience,
            **rewards
        })
        return next_state
    
    def _evolve_traits(self, state, rewards, policy_cfg):
        """Update agent traits based on current state and rewards.
        
        Key research insight: Intermittent reinforcement drives addiction and burnout,
        while differential reinforcement promotes sustainable, healthy patterns.
        """
        from simulation.agents.state_machine import CreatorState
        
        reward_magnitude = rewards.get("final_reward", 0)
        predictability = rewards.get("predictability", 0.5)
        
        # === BURNOUT DYNAMICS ===
        # Burnout increases when hustling, decreases when resting
        if state == CreatorState.HUSTLER:
            # Intermittent reinforcement causes MORE burnout (chasing unpredictable rewards)
            burnout_increase = 0.05 if policy_cfg.mode == "differential" else 0.08
            self.profile.burnout = min(1.0, self.profile.burnout + burnout_increase)
        elif state == CreatorState.BURNOUT:
            # Recovery is faster with differential (predictable rest rewards)
            recovery_rate = 0.03 if policy_cfg.mode == "differential" else 0.02
            self.profile.burnout = max(0.0, self.profile.burnout - recovery_rate)
        else:
            # Baseline burnout reduction
            self.profile.burnout = max(0.0, self.profile.burnout - 0.01)
        
        # === AROUSAL/ANXIETY DYNAMICS ===
        # Unpredictable rewards create anxiety and hypervigilance
        if policy_cfg.mode == "intermittent":
            # Intermittent: High arousal from unpredictability
            if reward_magnitude > 0:
                # Got reward - dopamine spike
                self.profile.arousal_level = min(1.0, self.profile.arousal_level + 0.06)
            else:
                # Missed reward - anxiety increases
                self.profile.arousal_level = min(1.0, self.profile.arousal_level + 0.03)
        else:
            # Differential: Stable arousal levels
            if reward_magnitude > 0.5:
                self.profile.arousal_level = min(1.0, self.profile.arousal_level + 0.02)
            else:
                self.profile.arousal_level = max(0.0, self.profile.arousal_level - 0.02)
        
        # === ADDICTION DYNAMICS ===
        # Intermittent reinforcement is HIGHLY addictive (like gambling)
        if policy_cfg.mode == "intermittent":
            # Unpredictable rewards drive compulsive behavior
            if reward_magnitude > 0.3:
                # Big reward hit - addiction spike
                self.profile.addiction_drive = min(1.0, self.profile.addiction_drive + 0.07)
            else:
                # Near-miss keeps addiction high
                self.profile.addiction_drive = min(1.0, self.profile.addiction_drive + 0.02)
        elif policy_cfg.mode == "differential":
            # Predictable rewards reduce addiction over time
            self.profile.addiction_drive = max(0.0, self.profile.addiction_drive - 0.02)
        else:  # hybrid
            # Moderate addiction effects
            if reward_magnitude > 0.3:
                self.profile.addiction_drive = min(1.0, self.profile.addiction_drive + 0.03)
            else:
                self.profile.addiction_drive = max(0.0, self.profile.addiction_drive - 0.01)
        
        # === RESILIENCE DYNAMICS ===
        # Differential reinforcement builds resilience through predictability
        if policy_cfg.mode == "differential" and predictability > 0.8:
            # Predictable environment builds confidence and resilience
            self.profile.emotional_resilience = min(1.0, self.profile.emotional_resilience + 0.01)
        elif policy_cfg.mode == "intermittent":
            # Unpredictability erodes resilience
            self.profile.emotional_resilience = max(0.0, self.profile.emotional_resilience - 0.01)

    def get_state_probabilities(self, rewards):
        """Get current state transition probabilities for this agent."""
        ctx = StateContext(
            arousal=self.profile.arousal_level,
            addiction=self.profile.addiction_drive,
            burnout=self.profile.burnout,
            resilience=self.profile.emotional_resilience,
            quality=rewards.get("quality", 0),
            diversity=rewards.get("diversity", 0),
            consistency=rewards.get("consistency", 0)
        )
        return self.state_machine.get_transition_probabilities(ctx, rewards)
    
    def get_strategy_info(self):
        """Get human-readable strategy information for UI display."""
        return {
            "name": self.profile.strategy,
            "description": self._get_strategy_description(self.profile.strategy)
        }
    
    def _get_strategy_description(self, strategy):
        """Get description for a given strategy."""
        descriptions = {
            "rapid_posting": "High volume, frequent content",
            "consistent_quality": "Steady, high-quality output",
            "experimental": "Diverse, exploratory content",
            "minimal_effort": "Low engagement, survival mode",
            "strategic_rest": "Recovery and planning phase",
            "passionate_burst": "Intense creative periods",
            "calculated_risk": "Strategic experimentation",
        }
        return descriptions.get(strategy, "Unknown strategy")
    
    def as_dict(self):
        return {
            "id": self.profile.id,
            "state": self.profile.current_state.name,
            "arousal": round(self.profile.arousal_level, 3),
            "burnout": round(self.profile.burnout, 3),
            "addiction": round(self.profile.addiction_drive, 3),
            "resilience": round(self.profile.emotional_resilience, 3),
            "strategy": self.profile.strategy,
            "ticks_alive": len(self.history)
        }
