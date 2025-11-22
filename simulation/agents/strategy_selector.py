from simulation.agents.state_machine import CreatorState
import random

class StrategySelector:
    """Selects content creation strategy based on agent state and traits.
    
    Strategies represent different approaches to content creation:
    - rapid_posting: High volume, quick turnaround
    - consistent_quality: Balanced output with quality focus
    - creative_experimentation: Novel, diverse content
    - withdrawal: Reduced activity, recovery mode
    - adaptive_hustling: High output with quality awareness
    - mindful_creation: Quality-first with breaks
    """
    
    def select(self, agent):
        """Select strategy based on agent's current state and personality traits.
        
        Args:
            agent: The agent to select a strategy for
            
        Returns:
            str: The selected strategy name
        """
        state = agent.profile.current_state
        p = agent.profile
        
        # Base strategy from state
        if state == CreatorState.HUSTLER:
            # High arousal agents go full rapid, others might be more measured
            if p.arousal_level > 0.7:
                return "rapid_posting"
            elif p.quality > 0.6:
                return "adaptive_hustling"  # Hustling but quality-aware
            else:
                return "rapid_posting"
                
        elif state == CreatorState.OPTIMIZER:
            # Resilient optimizers are more consistent
            if p.emotional_resilience > 0.7:
                return "consistent_quality"
            elif p.burnout > 0.5:
                return "mindful_creation"  # Quality but with self-care
            else:
                return "consistent_quality"
                
        elif state == CreatorState.TRUE_BELIEVER:
            # High diversity agents experiment more
            if p.diversity > 0.6:
                return "creative_experimentation"
            elif p.quality > 0.7:
                return "artistic_excellence"  # Creative but polished
            else:
                return "creative_experimentation"
                
        elif state == CreatorState.BURNOUT:
            # Severity of withdrawal depends on burnout level
            if p.burnout > 0.8:
                return "complete_withdrawal"  # Need serious break
            elif p.emotional_resilience > 0.6:
                return "strategic_pause"  # Planned recovery
            else:
                return "withdrawal"
        
        # Fallback
        return "neutral"
    
    def get_strategy_description(self, strategy: str) -> str:
        """Get human-readable description of a strategy."""
        descriptions = {
            "rapid_posting": "High-volume content creation, prioritizing quantity and engagement",
            "adaptive_hustling": "High output balanced with quality awareness",
            "consistent_quality": "Steady, reliable content with quality focus",
            "mindful_creation": "Quality-first approach with self-care breaks",
            "creative_experimentation": "Novel, diverse content exploring new ideas",
            "artistic_excellence": "Highly creative and polished content",
            "withdrawal": "Reduced activity for recovery",
            "complete_withdrawal": "Full break from content creation",
            "strategic_pause": "Planned recovery period with minimal activity",
            "neutral": "Baseline content creation approach",
        }
        return descriptions.get(strategy, "Unknown strategy")
    
    def get_strategy_metrics(self, strategy: str) -> dict:
        """Get expected performance metrics for a strategy.
        
        Returns multipliers for quality, consistency, and output volume.
        """
        metrics = {
            "rapid_posting": {"quality": 0.6, "consistency": 0.7, "volume": 1.5},
            "adaptive_hustling": {"quality": 0.8, "consistency": 0.8, "volume": 1.3},
            "consistent_quality": {"quality": 1.0, "consistency": 1.2, "volume": 1.0},
            "mindful_creation": {"quality": 1.1, "consistency": 0.9, "volume": 0.8},
            "creative_experimentation": {"quality": 0.9, "consistency": 0.6, "volume": 0.9},
            "artistic_excellence": {"quality": 1.3, "consistency": 0.8, "volume": 0.7},
            "withdrawal": {"quality": 0.3, "consistency": 0.3, "volume": 0.3},
            "complete_withdrawal": {"quality": 0.1, "consistency": 0.1, "volume": 0.1},
            "strategic_pause": {"quality": 0.5, "consistency": 0.4, "volume": 0.4},
            "neutral": {"quality": 1.0, "consistency": 1.0, "volume": 1.0},
        }
        return metrics.get(strategy, {"quality": 1.0, "consistency": 1.0, "volume": 1.0})