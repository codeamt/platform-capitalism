from simulation.agents.state_machine import CreatorStateMachine, StateContext, CreatorState
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
        history_entry = {
            "tick": current_tick if current_tick is not None else len(self.history),
            "state": next_state.name,
            "burnout": self.profile.burnout,
            "addiction": self.profile.addiction_drive,
            "resilience": self.profile.emotional_resilience,
            **rewards
        }
        
        # Include posts generated this tick (if content generation was called)
        if hasattr(self, '_current_tick_posts'):
            history_entry["posts_generated"] = self._current_tick_posts
            # Keep _current_tick_posts for UI display (don't delete it)
        
        self.history.append(history_entry)
        return next_state
    
    def _evolve_traits(self, state, rewards, policy_cfg):
        """Update agent traits based on current state and rewards.
        
        Key research insight: Intermittent reinforcement drives addiction and burnout,
        while differential reinforcement promotes sustainable, healthy patterns.
        """
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
    
    def _parse_frequency_from_strategy(self, strategy_description: str) -> float:
        """Infers a baseline content generation multiplier from the strategy description.
        
        This replaces a need for complex strategy parsing with simple keyword checks.
        
        Args:
            strategy_description: Human-readable strategy description string
            
        Returns:
            float: Content output multiplier (0.5 = low, 1.0 = normal, 1.5 = high)
        """
        description = strategy_description.lower()
        
        # High frequency strategies
        if "aggressive" in description or "high frequency" in description or "rapid" in description:
            return 1.5
        
        # Low frequency strategies
        elif "low-risk" in description or "conservative" in description or "withdrawal" in description:
            return 0.5
        
        # Moderate/balanced strategies
        elif "steady" in description or "balanced" in description or "consistent" in description:
            return 1.0
        
        # Default to normal output
        return 1.0
    
    def simulate_content_generation(self) -> float:
        """Simulates content output for the current tick.
        
        Adjusts output based on:
        1. The agent's long-term strategy (inferred frequency)
        2. The reward received in the previous tick (agency/feedback loop)
        
        This implements agency: agents learn from rewards and adjust behavior.
        Positive rewards encourage more output, negative rewards cause hesitation.
        
        Returns:
            float: Number of posts generated this tick
        """
        # Get strategy-based frequency multiplier
        strategy_desc = self._get_strategy_description(self.profile.strategy)
        base_frequency_multiplier = self._parse_frequency_from_strategy(strategy_desc)
        
        # --- Implementing Agency: Feedback from Previous Tick ---
        feedback_modifier = 0.0
        if self.history:
            # Check the 'reward' logged in the *last* completed tick
            previous_reward = self.history[-1].get('final_reward', 0.0)
            
            # Positive Reinforcement: If rewarded, slightly exceed the planned frequency
            if previous_reward > 0.1:
                # Add up to +0.2 to the multiplier, scaled by reward magnitude
                feedback_modifier = min(0.2, previous_reward * 0.5)
            
            # Negative Reinforcement: If penalized, reduce output or stick rigidly to plan
            elif previous_reward < -0.1:
                # Subtract up to -0.1 from the multiplier
                feedback_modifier = max(-0.1, previous_reward * 0.2)
        
        # --- Calculate Final Content Output ---
        # Use quality as a proxy for base productivity (agents with higher quality tend to be more productive)
        base_output = self.profile.quality
        
        # Combine strategy, feedback, and ensure output is not negative
        effective_frequency = max(0.0, base_frequency_multiplier + feedback_modifier)
        
        # Final posts generated (scale by max potential of 10.0 posts per tick/day)
        # This produces realistic ranges: 3-10 posts/day for active creators
        posts_generated = round(base_output * effective_frequency * 10.0, 1)
        
        # Store the result temporarily to be consumed by the Environment's history logging
        self._current_tick_posts = posts_generated
        
        return posts_generated
    
    # =========================================================================
    # FUTURE-PROOFING: Hugging Face / LLM Integration Stubs
    # =========================================================================
    # These methods are placeholders for future content generation features.
    # See FEEDBACK.md lines 359-458 for full implementation details.
    
    def _build_markov_corpus(self):
        """Build a Markov chain corpus from agent's historical content.
        
        Future Implementation:
        - Analyze agent's content history to build a statistical model
        - Use agent's quality, diversity, and consistency traits to shape corpus
        - Generate realistic text patterns based on agent's "voice"
        
        Returns:
            dict: Markov chain transition probabilities (stub returns empty dict)
        
        Example:
            {
                "the": {"quick": 0.3, "lazy": 0.2, "brown": 0.5},
                "quick": {"brown": 0.8, "fox": 0.2}
            }
        """
        # STUB: Return empty corpus
        # TODO: Implement Markov chain builder when content history is available
        return {}
    
    def generate_content_prompt_hf(self, temperature=0.7, max_tokens=100):
        """Generate a content prompt for Hugging Face text generation.
        
        Future Implementation:
        - Use agent traits (quality, diversity, strategy) to craft prompts
        - Integrate with HF Inference API or local models
        - Generate realistic social media posts based on agent persona
        - Apply content moderation and safety filters
        
        Args:
            temperature (float): Sampling temperature for generation (0.0-1.0)
                - Low (0.1-0.3): Conservative, predictable content
                - Medium (0.5-0.7): Balanced creativity
                - High (0.8-1.0): Creative, diverse content
            max_tokens (int): Maximum length of generated content
        
        Returns:
            dict: Prompt configuration for HF API (stub returns placeholder)
        
        Example:
            {
                "model": "gpt2",
                "prompt": "As a content creator focused on...",
                "temperature": 0.7,
                "max_tokens": 100,
                "top_p": 0.9
            }
        """
        # STUB: Return placeholder prompt configuration
        # TODO: Integrate with Hugging Face Inference API
        
        # Map agent strategy to content style
        strategy_prompts = {
            "rapid_posting": "Create a quick, engaging social media post about trending topics.",
            "strategic_pause": "Write a thoughtful, well-researched post with depth.",
            "consistent_quality": "Generate a balanced post that maintains quality standards.",
            "quality_focus": "Craft a high-quality, polished post with strong narrative.",
            "volume_focus": "Create a short, punchy post optimized for engagement."
        }
        
        base_prompt = strategy_prompts.get(
            self.profile.strategy,
            "Create a social media post."
        )
        
        # Adjust temperature based on diversity trait
        adjusted_temp = temperature * (0.5 + self.profile.diversity * 0.5)
        
        return {
            "model": "gpt2",  # Placeholder model
            "prompt": base_prompt,
            "temperature": adjusted_temp,
            "max_tokens": max_tokens,
            "top_p": 0.9,
            "agent_id": self.profile.id,
            "quality_target": self.profile.quality,
            "diversity_target": self.profile.diversity
        }
