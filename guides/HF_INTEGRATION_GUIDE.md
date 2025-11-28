# Hugging Face Integration Guide

## Overview

The Platform Capitalism simulation now includes optional text content generation using Hugging Face models. This feature allows agents to generate realistic social media posts based on their personality traits, state, and strategy.

## Features

### 1. **Intelligent Content Generation**
- Generate realistic social media posts using HF models
- Content quality and diversity driven by agent traits
- Automatic prompt engineering based on agent strategy

### 2. **Graceful Fallback**
- Template-based generation when HF API is unavailable
- No API key required for basic functionality
- Seamless degradation without errors

### 3. **Agent-Driven Prompts**
- Prompts tailored to agent personality
- Temperature adjusted by diversity trait
- Content length based on quality target

## Quick Start

### Installation

```bash
# Install dependencies (includes huggingface-hub)
uv sync

# Or manually add the dependency
uv add huggingface-hub
```

### Configuration (Optional)

1. **Get HF API Key**: https://huggingface.co/settings/tokens

2. **Set Environment Variable**:
   ```bash
   export HUGGINGFACE_API_KEY="your_key_here"
   ```

3. **Or add to `.env` file**:
   ```env
   HUGGINGFACE_API_KEY=your_key_here
   ```

### Basic Usage

#### Enable Text Generation in Simulation

```python
from simulation.environment import GLOBAL_ENVIRONMENT

# Run tick with text generation enabled
GLOBAL_ENVIRONMENT.tick(generate_text_content=True)
```

#### Generate Content for Specific Agent

```python
from simulation.content_generator import generate_agent_content

# Generate content for an agent
agent = GLOBAL_ENVIRONMENT.agents[0]
result = generate_agent_content(agent, temperature=0.7, max_tokens=100)

print(result["content"])
# Output: "Just posted new content! Check it out and let me know what you think. 🚀"
```

## API Reference

### `ContentGenerator` Class

Main class for content generation with HF API support.

```python
from simulation.content_generator import ContentGenerator

# Initialize with API key
generator = ContentGenerator(api_key="your_key", model="gpt2")

# Or use environment variable
generator = ContentGenerator()  # Reads HUGGINGFACE_API_KEY

# Generate content
result = generator.generate_content(
    prompt="Create a social media post",
    temperature=0.7,
    max_tokens=100,
    quality_target=0.8,
    diversity_target=0.6
)
```

#### Methods

**`generate_content(prompt, temperature, max_tokens, quality_target, diversity_target)`**
- Main content generation method
- Automatically uses HF API or fallback
- Returns dict with content and metadata

**`_generate_with_hf(...)`**
- Direct HF API generation
- Raises exception on failure
- Used internally by `generate_content()`

**`_generate_fallback(...)`**
- Template-based generation
- Always succeeds
- Used when HF API unavailable

**`generate_markov_content(corpus, seed_word, length)`**
- Statistical content generation (future)
- Uses Markov chain from corpus
- Alternative fallback method

### `generate_agent_content()` Function

High-level function for agent-specific content generation.

```python
from simulation.content_generator import generate_agent_content

result = generate_agent_content(
    agent,                    # Agent instance
    temperature=0.7,          # Sampling temperature
    max_tokens=100           # Max content length
)
```

**Returns:**
```python
{
    "content": str,           # Generated text
    "method": str,            # "huggingface" or "template_fallback"
    "model": str,             # Model name (e.g., "gpt2")
    "word_count": int,        # Number of words
    "char_count": int,        # Number of characters
    "quality_score": float,   # Estimated quality (0-1)
    "temperature": float,     # Actual temperature used
    "quality_target": float,  # Agent's quality trait
    "diversity_target": float,# Agent's diversity trait
    "agent_id": str,          # Agent identifier
    "agent_state": str,       # Current state (e.g., "OPTIMIZER")
    "agent_strategy": str     # Current strategy
}
```

### Agent Methods

**`agent.generate_content_prompt_hf(temperature, max_tokens)`**

Generate HF prompt configuration based on agent traits.

```python
agent = agents[0]
config = agent.generate_content_prompt_hf(temperature=0.7, max_tokens=100)

# Returns:
{
    "model": "gpt2",
    "prompt": "Create a quick, engaging social media post...",
    "temperature": 0.65,      # Adjusted by agent.diversity
    "max_tokens": 100,
    "top_p": 0.9,
    "agent_id": "agent_1",
    "quality_target": 0.8,
    "diversity_target": 0.6
}
```

**`agent._build_markov_corpus()`**

Build Markov chain from agent's content history (stub for future).

```python
corpus = agent._build_markov_corpus()
# Returns: {} (stub implementation)
```

## Content Generation Strategies

### Strategy-Based Prompts

Different agent strategies generate different prompt styles:

| Strategy | Prompt Style | Example |
|----------|-------------|---------|
| `rapid_posting` | Quick, engaging | "Create a quick, engaging social media post about trending topics." |
| `strategic_pause` | Thoughtful, researched | "Write a thoughtful, well-researched post with depth." |
| `consistent_quality` | Balanced | "Generate a balanced post that maintains quality standards." |
| `quality_focus` | High-quality, polished | "Craft a high-quality, polished post with strong narrative." |
| `volume_focus` | Short, punchy | "Create a short, punchy post optimized for engagement." |

### Temperature Adjustment

Temperature is automatically adjusted based on agent's diversity trait:

```python
adjusted_temp = temperature * (0.5 + agent.diversity * 0.5)

# Examples:
# diversity=0.2 → temp=0.7 * 0.6 = 0.42 (conservative)
# diversity=0.5 → temp=0.7 * 0.75 = 0.525 (balanced)
# diversity=0.9 → temp=0.7 * 0.95 = 0.665 (creative)
```

## Fallback Mode

When HF API is unavailable, the system uses intelligent template-based generation:

### Template Selection

Templates are selected based on diversity trait:

- **High diversity (>0.7)**: All 8 templates available
- **Medium diversity (0.4-0.7)**: First 5 templates
- **Low diversity (<0.4)**: First 3 templates (consistent)

### Quality Enhancement

High-quality agents (quality > 0.7) get additional detail:

```python
if quality_target > 0.7:
    content += random.choice([
        " I've been researching this for a while.",
        " This is based on recent insights.",
        " Looking forward to your feedback!",
        " Let's build something amazing together."
    ])
```

## Integration Examples

### Example 1: Generate Content During Tick

```python
from simulation.environment import GLOBAL_ENVIRONMENT

# Enable text generation for this tick
GLOBAL_ENVIRONMENT.tick(generate_text_content=True)

# Access generated content
for agent in GLOBAL_ENVIRONMENT.agents:
    if hasattr(agent, '_current_tick_content'):
        for content in agent._current_tick_content:
            print(f"Agent {agent.profile.id}: {content['content']}")
```

### Example 2: Batch Content Generation

```python
from simulation.content_generator import generate_agent_content

# Generate content for all agents
results = []
for agent in GLOBAL_ENVIRONMENT.agents:
    result = generate_agent_content(agent)
    results.append(result)

# Analyze content quality
avg_quality = sum(r['quality_score'] for r in results) / len(results)
print(f"Average content quality: {avg_quality:.2f}")
```

### Example 3: Custom Content Generation

```python
from simulation.content_generator import ContentGenerator

# Create custom generator
generator = ContentGenerator(model="gpt2")

# Generate with custom parameters
result = generator.generate_content(
    prompt="Write a viral social media post about AI",
    temperature=0.9,  # High creativity
    max_tokens=150,
    quality_target=0.9,
    diversity_target=0.8
)

print(result['content'])
```

## Error Handling

The content generator handles errors gracefully:

```python
# Missing API key → Uses fallback
generator = ContentGenerator(api_key=None)
result = generator.generate_content(...)
# result['method'] == "template_fallback"

# API failure → Automatic fallback
try:
    result = generator._generate_with_hf(...)
except Exception:
    result = generator._generate_fallback(...)
```

## Performance Considerations

### API Rate Limits

HF API has rate limits. For high-volume simulations:

1. **Cache generated content** for similar agents
2. **Use fallback mode** for non-critical simulations
3. **Batch requests** when possible
4. **Monitor API usage** in HF dashboard

### Optimization Tips

```python
# 1. Disable text generation for fast simulations
GLOBAL_ENVIRONMENT.tick(generate_text_content=False)  # Default

# 2. Generate content only for specific agents
if agent.profile.quality > 0.8:
    content = generate_agent_content(agent)

# 3. Use lower max_tokens for faster generation
result = generate_agent_content(agent, max_tokens=50)
```

## Testing

Run content generation tests:

```bash
# Test content generator
uv run pytest tests/test_content_generator.py -v

# Test all functionality
uv run pytest tests/ -v
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'huggingface_hub'"

**Solution:**
```bash
uv sync
# or
uv add huggingface-hub
```

### Issue: Content generation returns fallback mode

**Possible causes:**
1. No API key set
2. Invalid API key
3. API rate limit exceeded
4. Network connection issues

**Solution:**
```bash
# Check API key
echo $HUGGINGFACE_API_KEY

# Verify API key at: https://huggingface.co/settings/tokens

# Test connection
python -c "from huggingface_hub import InferenceClient; print('OK')"
```

### Issue: Generated content is low quality

**Solutions:**
1. Increase `quality_target` parameter
2. Use higher-quality model (e.g., "gpt2-large")
3. Adjust temperature (lower = more conservative)
4. Provide more specific prompts

## Future Enhancements

### Planned Features

1. **Markov Chain Generation**: Statistical content from agent history
2. **Multi-Model Support**: Switch between GPT-2, GPT-J, etc.
3. **Content Moderation**: Filter inappropriate content
4. **Sentiment Analysis**: Analyze generated content sentiment
5. **A/B Testing**: Compare different generation strategies

### Contributing

To add new generation methods:

1. Extend `ContentGenerator` class
2. Add new method (e.g., `_generate_with_markov()`)
3. Update `generate_content()` to use new method
4. Add tests in `tests/test_content_generator.py`

## Resources

- **HF API Docs**: https://huggingface.co/docs/api-inference
- **Model Hub**: https://huggingface.co/models
- **API Tokens**: https://huggingface.co/settings/tokens
- **Rate Limits**: https://huggingface.co/docs/api-inference/rate-limits

## Support

For issues or questions:
1. Check this guide
2. Review test examples in `tests/test_content_generator.py`
3. Check implementation in `simulation/content_generator.py`
4. Open GitHub issue with reproduction steps
