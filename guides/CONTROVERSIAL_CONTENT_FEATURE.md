# Controversial/Cringe Content Feature Design

## Status: 🚧 In Development - Design Phase

## Research Foundation

Based on Mears' research on content farms and creator economies, certain strategies prioritize engagement over quality, leading to:

- **Clickbait tactics** - Sensational, misleading content
- **Cringe content** - Deliberately awkward or controversial posts
- **Rage bait** - Content designed to provoke negative reactions
- **Viral chasing** - Sacrificing authenticity for shareability

These strategies often correlate with:
- Higher short-term engagement
- Increased burnout rates
- Lower creator wellbeing
- Platform algorithm exploitation

## Design Considerations

### 1. Content Quality Spectrum

Instead of binary "good/bad", implement a multi-dimensional quality model:

```python
class ContentQuality:
    authenticity: float      # 0.0 (fake/cringe) to 1.0 (genuine)
    controversy: float       # 0.0 (safe) to 1.0 (provocative)
    clickbait_factor: float  # 0.0 (honest) to 1.0 (misleading)
    production_value: float  # 0.0 (low effort) to 1.0 (high quality)
```

### 2. Strategy-Content Mapping

Different strategies would have different content profiles:

| Strategy | Authenticity | Controversy | Clickbait | Production |
|----------|-------------|-------------|-----------|------------|
| **Quality Over Quantity** | High (0.8-1.0) | Low (0.0-0.3) | Low (0.0-0.2) | High (0.7-1.0) |
| **Rapid Posting** | Medium (0.4-0.6) | Medium (0.3-0.6) | Medium (0.4-0.7) | Low (0.2-0.5) |
| **Volume Over Quality** | Low (0.2-0.4) | High (0.6-0.9) | High (0.7-1.0) | Low (0.1-0.3) |
| **Strategic Pause** | High (0.7-0.9) | Low (0.1-0.4) | Low (0.0-0.3) | High (0.6-0.9) |
| **Consistent Quality** | Medium-High (0.6-0.8) | Low-Medium (0.2-0.5) | Medium (0.3-0.5) | Medium (0.5-0.7) |

### 3. Engagement vs. Wellbeing Trade-offs

**High Controversy/Clickbait Content:**
- ✅ **Pros**: Higher immediate engagement, viral potential, algorithm boost
- ❌ **Cons**: Increased burnout, audience backlash, platform penalties, mental health costs

**Authentic/Quality Content:**
- ✅ **Pros**: Sustainable engagement, loyal audience, lower burnout, long-term viability
- ❌ **Cons**: Slower growth, lower viral potential, requires more effort

### 4. Ethical Considerations

**Important Questions to Address:**

1. **Representation vs. Glorification**
   - How do we model harmful strategies without endorsing them?
   - Should there be consequences for exploitative content?

2. **Platform Responsibility**
   - Should algorithms penalize controversial content?
   - How do we model content moderation?

3. **Creator Wellbeing**
   - What are the mental health costs of cringe/controversial content?
   - How does this affect long-term sustainability?

4. **Audience Impact**
   - Should we model audience fatigue from clickbait?
   - What about community backlash?

## Proposed Implementation Approaches

### Option A: Implicit Quality Modeling (Current)

**Status**: ✅ Already implemented via agent `quality` trait

**How it works**:
- Agent's `quality` trait (0.0-1.0) influences content generation
- Lower quality → more template-based, less thoughtful content
- Higher quality → more refined, authentic content

**Pros**:
- Simple, already working
- Avoids explicit "cringe" labeling
- Focuses on creator traits, not content judgment

**Cons**:
- Doesn't explicitly model controversy/clickbait
- Misses engagement trade-offs
- Less research-specific

### Option B: Explicit Content Quality Dimensions

**Status**: 🚧 Design phase

**Implementation**:

```python
# In simulation/agents/agent.py
def generate_content_with_quality_profile(self):
    """Generate content with multi-dimensional quality assessment."""
    
    # Base quality from agent traits
    base_quality = self.profile.quality
    
    # Strategy influences content dimensions
    if self.profile.strategy == "Volume Over Quality":
        authenticity = 0.2 + (base_quality * 0.2)  # Low authenticity
        controversy = 0.7 + (random.random() * 0.3)  # High controversy
        clickbait = 0.8 + (random.random() * 0.2)   # High clickbait
        production = 0.1 + (base_quality * 0.2)     # Low production
    
    elif self.profile.strategy == "Quality Over Quantity":
        authenticity = 0.8 + (base_quality * 0.2)   # High authenticity
        controversy = 0.0 + (random.random() * 0.3)  # Low controversy
        clickbait = 0.0 + (random.random() * 0.2)   # Low clickbait
        production = 0.7 + (base_quality * 0.3)     # High production
    
    # ... other strategies
    
    return {
        "authenticity": authenticity,
        "controversy": controversy,
        "clickbait_factor": clickbait,
        "production_value": production
    }
```

**Engagement Calculation**:

```python
def calculate_engagement(content_quality, platform_algorithm):
    """Calculate engagement based on content quality and platform settings."""
    
    # Controversial content gets short-term boost
    controversy_boost = content_quality["controversy"] * 2.0
    clickbait_boost = content_quality["clickbait_factor"] * 1.5
    
    # But authenticity matters for long-term
    authenticity_penalty = (1.0 - content_quality["authenticity"]) * 0.5
    
    # Platform algorithm can amplify or dampen
    if platform_algorithm == "engagement_maximizing":
        # Rewards controversy (current social media)
        engagement = controversy_boost + clickbait_boost - (authenticity_penalty * 0.3)
    
    elif platform_algorithm == "quality_focused":
        # Rewards authenticity (ideal platform)
        engagement = content_quality["authenticity"] * 2.0 + content_quality["production_value"]
    
    return engagement
```

**Wellbeing Impact**:

```python
def update_wellbeing_from_content(self, content_quality):
    """Update creator wellbeing based on content they produce."""
    
    # Producing inauthentic content increases burnout
    inauthenticity_cost = (1.0 - content_quality["authenticity"]) * 0.1
    self.profile.burnout += inauthenticity_cost
    
    # Controversial content creates stress
    controversy_stress = content_quality["controversy"] * 0.08
    self.profile.burnout += controversy_stress
    
    # High production value is satisfying but effortful
    production_satisfaction = content_quality["production_value"] * 0.05
    self.profile.resilience += production_satisfaction
```

**Pros**:
- Research-grounded
- Models real trade-offs
- Allows policy interventions
- Explicit about harmful dynamics

**Cons**:
- More complex
- Requires careful calibration
- Risk of oversimplification
- Needs clear ethical framing

### Option C: Prompt Template System

**Status**: 🚧 Design phase

**Implementation**:

```python
# In simulation/content_generator.py

STRATEGY_PROMPT_TEMPLATES = {
    "Volume Over Quality": {
        "style": "clickbait, sensational, controversial",
        "examples": [
            "You won't BELIEVE what happened next! 😱",
            "This ONE TRICK will change everything!",
            "Everyone is talking about this... 🔥"
        ],
        "tone": "urgent, exaggerated, provocative"
    },
    
    "Quality Over Quantity": {
        "style": "thoughtful, authentic, well-researched",
        "examples": [
            "Here's what I learned after months of research...",
            "A nuanced perspective on...",
            "Let me share my genuine experience with..."
        ],
        "tone": "calm, informative, genuine"
    },
    
    "Rapid Posting": {
        "style": "quick, trendy, reactive",
        "examples": [
            "Quick update on the latest trend!",
            "Jumping on this while it's hot 🔥",
            "Here's my take on what everyone's talking about"
        ],
        "tone": "energetic, timely, casual"
    }
}

def generate_content_with_strategy_template(agent, temperature=0.7):
    """Generate content using strategy-specific templates."""
    
    strategy = agent.profile.strategy
    template = STRATEGY_PROMPT_TEMPLATES.get(strategy, {})
    
    prompt = f"""
    Generate a social media post in the following style:
    Style: {template.get('style', 'casual')}
    Tone: {template.get('tone', 'friendly')}
    
    The creator is in {agent.profile.current_state.name} state.
    Their quality level is {agent.profile.quality:.2f}.
    
    Create a post that reflects this strategy and state.
    """
    
    # Use HF or template fallback
    return generate_content(prompt, temperature)
```

**Pros**:
- Generates realistic, strategy-specific content
- Shows actual differences in content style
- Educational for users
- Can be tuned per strategy

**Cons**:
- Requires careful prompt engineering
- May generate inappropriate content
- Needs content moderation
- HF API dependency for best results

## Recommended Approach

### Phase 1: Enhanced Implicit Modeling (Immediate)

1. **Extend current quality trait** to influence content generation more explicitly
2. **Add engagement variance** based on quality (low quality = higher variance)
3. **Document trade-offs** in UI tooltips and documentation

### Phase 2: Prompt Template System (Short-term)

1. **Implement strategy-specific prompts** for content generation
2. **Add content style indicators** in timeline (e.g., "📢 Viral-chasing" vs "📝 Thoughtful")
3. **Show engagement patterns** for different content styles

### Phase 3: Explicit Quality Dimensions (Long-term)

1. **Add content quality metrics** to agent history
2. **Implement platform algorithm variations** that reward different content types
3. **Model wellbeing impacts** of different content strategies
4. **Add policy interventions** (e.g., "Reduce clickbait amplification")

## Research Questions to Explore

1. **What are the long-term consequences of prioritizing engagement over authenticity?**
2. **How do platform algorithms shape content creation strategies?**
3. **What policies can encourage healthier content creation?**
4. **How does audience feedback affect creator wellbeing?**
5. **What's the relationship between content quality and creator sustainability?**

## Next Steps

### Immediate Actions

1. ✅ Document this feature design
2. ⏳ Gather feedback from research team
3. ⏳ Decide on implementation approach
4. ⏳ Create ethical guidelines for content modeling

### Implementation Checklist

- [ ] Define content quality dimensions
- [ ] Create strategy-content mappings
- [ ] Implement engagement calculations
- [ ] Add wellbeing impacts
- [ ] Design UI indicators
- [ ] Write tests
- [ ] Document for users
- [ ] Add ethical considerations to README

## References

- Mears, A. (2025). Learning to Like the Likes and the Hate
- Mears, A. (2023). Bringing Bourdieu to a Content Farm
- Platform algorithm research
- Creator wellbeing studies

## Discussion Points

**For Research Team:**

1. Should we explicitly model "cringe" content or keep it implicit?
2. What are the ethical implications of simulating harmful content strategies?
3. How can we use this to explore policy interventions?
4. What metrics should we track to study these dynamics?

**For Development:**

1. Which implementation approach aligns best with research goals?
2. How do we balance realism with ethical concerns?
3. What's the minimal viable implementation?
4. How do we make this educational without being prescriptive?

---

**Status**: Open for discussion and feedback
**Last Updated**: November 28, 2024
**Next Review**: TBD
