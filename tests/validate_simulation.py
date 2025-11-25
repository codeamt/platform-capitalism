"""Validation script for platform-capitalism simulation.

Run this script to validate that all Phase 1-3 features work correctly.
Usage: python tests/validate_simulation.py (from project root)
"""
import sys
from pathlib import Path

# Add project root to path so imports work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from simulation.agents.agent import Agent
from simulation.agents.profile import AgentProfile
from simulation.environment import Environment, GLOBAL_ENVIRONMENT
from simulation.policy_engine.config import PolicyConfig, OPTIMAL_POLICY_CONFIG, get_preset
from simulation.scenarios import load_scenario, ALL_SCENARIOS


def validate_content_generation():
    """Validate that content generation works correctly."""
    print("\n=== Validating Content Generation ===")
    
    agent = Agent(AgentProfile(id=1))
    agent.profile.strategy = "Quality Over Quantity"
    
    # Test 1: Content generation returns a number
    posts = agent.simulate_content_generation()
    assert isinstance(posts, (int, float)), "Content generation should return a number"
    assert posts >= 0, "Posts should be non-negative"
    print("✓ Content generation returns valid numeric value")
    
    # Test 2: Temporary attribute is set
    assert hasattr(agent, '_current_tick_posts'), "Should set _current_tick_posts"
    assert agent._current_tick_posts == posts, "Should store generated posts"
    print("✓ Temporary _current_tick_posts attribute set correctly")
    
    # Test 3: Works with empty history
    agent.history = []
    posts = agent.simulate_content_generation()
    assert posts > 0, "Should work with empty history"
    print("✓ Content generation works with no history")
    
    print("✅ Content Generation: PASSED")


def validate_policy_engine():
    """Validate that policy engine computes rewards correctly."""
    print("\n=== Validating Policy Engine ===")
    
    # Test 1: Optimal policy config exists
    assert OPTIMAL_POLICY_CONFIG is not None, "OPTIMAL_POLICY_CONFIG should exist"
    assert OPTIMAL_POLICY_CONFIG.mode == "differential", "Should be differential mode"
    assert OPTIMAL_POLICY_CONFIG.burnout_penalty == 0.40, "Should have correct burnout penalty"
    print("✓ OPTIMAL_POLICY_CONFIG defined correctly")
    
    # Test 2: Policy presets exist
    presets = ["optimal", "exploitative", "balanced", "cooperative"]
    for preset_name in presets:
        preset_config = get_preset(preset_name)
        assert isinstance(preset_config, PolicyConfig), f"{preset_name} should return PolicyConfig"
    print(f"✓ All {len(presets)} policy presets load correctly")
    
    # Test 3: Environment uses optimal config by default
    env = Environment()
    assert env.policy_engine.config.burnout_penalty == 0.40, "Should use optimal config by default"
    print("✓ Environment uses OPTIMAL_POLICY_CONFIG by default")
    
    print("✅ Policy Engine: PASSED")


def validate_environment():
    """Validate environment functionality."""
    print("\n=== Validating Environment ===")
    
    # Test 1: Environment tracks arousal in history
    agent = Agent(AgentProfile(id=1))
    env = Environment(agents=[agent])
    
    assert "avg_arousal" in env.history, "History should track avg_arousal"
    print("✓ Environment history tracks arousal")
    
    # Test 2: Tick integrates content generation
    env.tick()
    assert len(agent.history) > 0, "Agent should have history after tick"
    last_entry = agent.history[-1]
    assert "posts_generated" in last_entry, "History should include posts_generated"
    print("✓ Tick integrates content generation")
    
    # Test 3: reset_full_state() works
    env.tick()
    env.tick()
    assert env.tick_count == 3, "Should have 3 ticks"
    env.reset_full_state()
    assert env.tick_count == 0, "Should reset to 0"
    assert len(env.history["ticks"]) == 0, "History should be cleared"
    print("✓ reset_full_state() clears all state")
    
    # Test 4: current_scenario tracking
    assert hasattr(env, 'current_scenario'), "Should have current_scenario attribute"
    print("✓ Environment tracks current_scenario")
    
    print("✅ Environment: PASSED")


def validate_scenarios():
    """Validate that all scenarios load correctly."""
    print("\n=== Validating Scenarios ===")
    
    # Test 1: All scenarios exist
    expected_scenarios = [
        "Algorithmic Slot Machine",
        "Engagement Maximizer",
        "Creator-First Platform",
        "Cooperative Commons",
        "Platform in Transition",
        "Mostly Differential"
    ]
    
    for scenario_name in expected_scenarios:
        assert scenario_name in ALL_SCENARIOS, f"{scenario_name} should exist"
    print(f"✓ All {len(expected_scenarios)} scenarios defined")
    
    # Test 2: Scenarios can be loaded
    agent = Agent(AgentProfile(id=1))
    env = Environment(agents=[agent])
    
    load_scenario(env, "Creator-First Platform")
    assert env.current_scenario == "Creator-First Platform", "Should set current_scenario"
    assert env.policy_engine.config.mode == "differential", "Should apply policy"
    print("✓ Scenarios load and set current_scenario")
    
    # Test 3: Loading scenario doesn't break on policy change
    load_scenario(env, "Algorithmic Slot Machine")
    assert env.current_scenario == "Algorithmic Slot Machine", "Should update scenario"
    assert env.policy_engine.config.mode == "intermittent", "Should change policy mode"
    print("✓ Scenarios can be switched")
    
    print("✅ Scenarios: PASSED")


def validate_integration():
    """Validate end-to-end integration."""
    print("\n=== Validating Integration ===")
    
    # Create environment with agents
    agents = [Agent(AgentProfile(id=i)) for i in range(5)]
    env = Environment(agents=agents)
    
    # Load a scenario
    load_scenario(env, "Creator-First Platform")
    
    # Run multiple ticks
    for _ in range(5):
        env.tick()
    
    # Validate results
    assert env.tick_count == 5, "Should have 5 ticks"
    assert len(env.history["ticks"]) == 5, "History should have 5 entries"
    assert len(env.history["avg_arousal"]) == 5, "Should track arousal for all ticks"
    
    # All agents should have history
    for agent in agents:
        assert len(agent.history) == 5, f"Agent {agent.profile.id} should have 5 history entries"
        for entry in agent.history:
            assert "posts_generated" in entry, "Each entry should have posts_generated"
    
    print("✓ Full simulation runs for 5 ticks")
    print("✓ All agents generate content and track history")
    print("✓ Environment tracks all metrics")
    
    print("✅ Integration: PASSED")


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("PLATFORM CAPITALISM SIMULATION - VALIDATION SUITE")
    print("=" * 60)
    
    try:
        validate_content_generation()
        validate_policy_engine()
        validate_environment()
        validate_scenarios()
        validate_integration()
        
        print("\n" + "=" * 60)
        print("🎉 ALL VALIDATIONS PASSED!")
        print("=" * 60)
        print("\nThe simulation is working correctly. All Phase 1-3 features validated.")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ VALIDATION FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())