from app.simulation.agents.state_machine import CreatorState

class StrategySelector:
    def select(self, agent):
        state = agent.profile.current_state
        if state == CreatorState.HUSTLER:
            return "rapid_posting"
        elif state == CreatorState.OPTIMIZER:
            return "consistent_quality"
        elif state == CreatorState.TRUE_BELIEVER:
            return "creative_experimentation"
        elif state == CreatorState.BURNOUT:
            return "withdrawal"
        return "neutral"