"""Pytest test suite for platform-capitalism simulation.

Run with: pytest tests/
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from simulation.agents.agent import Agent
from simulation.agents.profile import AgentProfile
from simulation.environment import Environment
from simulation.policy_engine.config import PolicyConfig, OPTIMAL_POLICY_CONFIG, get_preset
from simulation.scenarios import load_scenario, ALL_SCENARIOS


class TestContentGeneration:
    """Test content generation functionality."""
    
    def test_content_generation_returns_number(self):
        """Content generation should return a valid numeric value."""
        agent = Agent(AgentProfile(id=1))
        agent.profile.strategy = "Quality Over Quantity"
        
        posts = agent.simulate_content_generation()
        
        assert isinstance(posts, (int, float))
        assert posts >= 0
    
    def test_current_tick_posts_attribute(self):
        """Should set _current_tick_posts attribute."""
        agent = Agent(AgentProfile(id=1))
        
        posts = agent.simulate_content_generation()
        
        assert hasattr(agent, '_current_tick_posts')
        assert agent._current_tick_posts == posts
    
    def test_works_with_empty_history(self):
        """Content generation should work with no history."""
        agent = Agent(AgentProfile(id=1))
        agent.history = []
        
        posts = agent.simulate_content_generation()
        
        assert posts > 0


class TestPolicyEngine:
    """Test policy engine functionality."""
    
    def test_optimal_policy_config_exists(self):
        """OPTIMAL_POLICY_CONFIG should be defined correctly."""
        assert OPTIMAL_POLICY_CONFIG is not None
        assert OPTIMAL_POLICY_CONFIG.mode == "differential"
        assert OPTIMAL_POLICY_CONFIG.burnout_penalty == 0.40
    
    def test_all_presets_load(self):
        """All policy presets should load correctly."""
        presets = ["optimal", "exploitative", "balanced", "cooperative"]
        
        for preset_name in presets:
            preset_config = get_preset(preset_name)
            assert isinstance(preset_config, PolicyConfig)
    
    def test_environment_uses_optimal_by_default(self):
        """Environment should use OPTIMAL_POLICY_CONFIG by default."""
        env = Environment()
        
        assert env.policy_engine.config.burnout_penalty == 0.40


class TestEnvironment:
    """Test environment functionality."""
    
    def test_tracks_arousal_in_history(self):
        """Environment history should track arousal."""
        agent = Agent(AgentProfile(id=1))
        env = Environment(agents=[agent])
        
        assert "avg_arousal" in env.history
    
    def test_tick_integrates_content_generation(self):
        """Tick should integrate content generation."""
        agent = Agent(AgentProfile(id=1))
        env = Environment(agents=[agent])
        
        env.tick()
        
        assert len(agent.history) > 0
        last_entry = agent.history[-1]
        assert "posts_generated" in last_entry
    
    def test_reset_full_state(self):
        """reset_full_state() should clear all state."""
        agent = Agent(AgentProfile(id=1))
        env = Environment(agents=[agent])
        
        env.tick()
        env.tick()
        env.tick()
        assert env.tick_count == 3
        
        env.reset_full_state()
        
        assert env.tick_count == 0
        assert len(env.history["ticks"]) == 0
    
    def test_tracks_current_scenario(self):
        """Environment should track current_scenario."""
        env = Environment()
        
        assert hasattr(env, 'current_scenario')


class TestScenarios:
    """Test scenario loading functionality."""
    
    def test_all_scenarios_exist(self):
        """All expected scenarios should be defined."""
        expected_scenarios = [
            "Algorithmic Slot Machine",
            "Engagement Maximizer",
            "Creator-First Platform",
            "Cooperative Commons",
            "Platform in Transition",
            "Mostly Differential"
        ]
        
        for scenario_name in expected_scenarios:
            assert scenario_name in ALL_SCENARIOS
    
    def test_scenarios_load_correctly(self):
        """Scenarios should load and set current_scenario."""
        agent = Agent(AgentProfile(id=1))
        env = Environment(agents=[agent])
        
        load_scenario(env, "Creator-First Platform")
        
        assert env.current_scenario == "Creator-First Platform"
        assert env.policy_engine.config.mode == "differential"
    
    def test_scenarios_can_be_switched(self):
        """Scenarios should be switchable."""
        agent = Agent(AgentProfile(id=1))
        env = Environment(agents=[agent])
        
        load_scenario(env, "Creator-First Platform")
        load_scenario(env, "Algorithmic Slot Machine")
        
        assert env.current_scenario == "Algorithmic Slot Machine"
        assert env.policy_engine.config.mode == "intermittent"


class TestIntegration:
    """Test end-to-end integration."""
    
    def test_full_simulation_run(self):
        """Full simulation should run for multiple ticks."""
        agents = [Agent(AgentProfile(id=i)) for i in range(5)]
        env = Environment(agents=agents)
        
        load_scenario(env, "Creator-First Platform")
        
        for _ in range(5):
            env.tick()
        
        assert env.tick_count == 5
        assert len(env.history["ticks"]) == 5
        assert len(env.history["avg_arousal"]) == 5
    
    def test_all_agents_generate_content(self):
        """All agents should generate content and track history."""
        agents = [Agent(AgentProfile(id=i)) for i in range(5)]
        env = Environment(agents=agents)
        
        for _ in range(5):
            env.tick()
        
        for agent in agents:
            assert len(agent.history) == 5
            for entry in agent.history:
                assert "posts_generated" in entry
                assert isinstance(entry["posts_generated"], (int, float))


class TestCPMEconomics:
    """Test CPM-based earnings calculations."""
    
    def test_cpm_earnings_in_history(self):
        """Agent history should include CPM earnings."""
        agent = Agent(AgentProfile(id=1))
        env = Environment(agents=[agent])
        
        env.tick()
        
        assert len(agent.history) > 0
        last_entry = agent.history[-1]
        assert "cpm_earnings" in last_entry
        assert isinstance(last_entry["cpm_earnings"], (int, float))
        assert last_entry["cpm_earnings"] >= 0
    
    def test_cpm_varies_by_scenario(self):
        """CPM rates should vary by scenario."""
        agent = Agent(AgentProfile(id=1))
        env = Environment(agents=[agent])
        
        # Get exploitative preset (low CPM = 5.0)
        exploitative_config = get_preset("exploitative")
        exploitative_cpm = exploitative_config.cpm_rate
        
        # Get cooperative preset (high CPM = 20.0)
        cooperative_config = get_preset("cooperative")
        cooperative_cpm = cooperative_config.cpm_rate
        
        assert cooperative_cpm > exploitative_cpm
        assert exploitative_cpm == 5.0
        assert cooperative_cpm == 20.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
