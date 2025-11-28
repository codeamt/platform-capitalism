"""
Tests for content generation module.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from simulation.agents.agent import Agent
from simulation.agents.profile import AgentProfile
from simulation.agents.state_machine import CreatorState


def test_content_generator_import():
    """Test that content generator can be imported."""
    try:
        from simulation.content_generator import ContentGenerator, generate_agent_content
        assert ContentGenerator is not None
        assert generate_agent_content is not None
    except ImportError:
        pytest.skip("Content generator dependencies not installed")


def test_content_generator_fallback():
    """Test that content generator works without HF API key."""
    try:
        from simulation.content_generator import ContentGenerator
        
        # Create generator without API key
        generator = ContentGenerator(api_key=None)
        
        # Generate content using fallback
        result = generator.generate_content(
            prompt="Test prompt",
            temperature=0.7,
            max_tokens=100,
            quality_target=0.5,
            diversity_target=0.5
        )
        
        # Verify result structure
        assert "content" in result
        assert "method" in result
        assert result["method"] == "template_fallback"
        assert "word_count" in result
        assert "quality_score" in result
        assert len(result["content"]) > 0
        
    except ImportError:
        pytest.skip("Content generator dependencies not installed")


def test_agent_content_generation():
    """Test content generation for an agent."""
    try:
        from simulation.content_generator import generate_agent_content
        
        # Create a test agent
        profile = AgentProfile(
            id="test_agent",
            quality=0.8,
            diversity=0.6,
            consistency=0.7
        )
        profile.current_state = CreatorState.OPTIMIZER
        profile.strategy = "consistent_quality"
        
        agent = Agent(profile)
        
        # Generate content
        result = generate_agent_content(agent, temperature=0.7, max_tokens=100)
        
        # Verify result
        assert "content" in result
        assert "agent_id" in result
        assert result["agent_id"] == "test_agent"
        assert "agent_state" in result
        assert result["agent_state"] == "OPTIMIZER"
        assert "agent_strategy" in result
        assert result["agent_strategy"] == "consistent_quality"
        
    except ImportError:
        pytest.skip("Content generator dependencies not installed")


def test_agent_prompt_generation():
    """Test that agent can generate HF prompts."""
    profile = AgentProfile(
        id="test_agent",
        quality=0.8,
        diversity=0.6,
        consistency=0.7
    )
    profile.current_state = CreatorState.OPTIMIZER
    profile.strategy = "consistent_quality"
    
    agent = Agent(profile)
    
    # Generate prompt config
    config = agent.generate_content_prompt_hf(temperature=0.7, max_tokens=100)
    
    # Verify config structure
    assert "model" in config
    assert "prompt" in config
    assert "temperature" in config
    assert "max_tokens" in config
    assert "quality_target" in config
    assert "diversity_target" in config
    assert config["quality_target"] == 0.8
    assert config["diversity_target"] == 0.6


def test_markov_corpus_stub():
    """Test that Markov corpus method exists."""
    profile = AgentProfile(id="test_agent")
    agent = Agent(profile)
    
    # Call stub method
    corpus = agent._build_markov_corpus()
    
    # Should return empty dict (stub implementation)
    assert isinstance(corpus, dict)
    assert len(corpus) == 0
