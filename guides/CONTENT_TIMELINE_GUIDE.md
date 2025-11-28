# Content Timeline Feature Guide

## Overview

The Recent Activity Feed has been upgraded to a **Content Timeline** that displays generated social media posts from agents, emulating a real social media feed.

## Features

### Timeline Display

The Content Timeline shows:
- **Agent avatar** with state emoji (🎯 Optimizer, ⚡ Hustler, ✨ True Believer, 🔥 Burnout)
- **Creator name** and timestamp
- **State badge** with color coding
- **Post count** for the tick
- **Generated content** (when text generation is enabled)
- **Content metadata** (generation method, word count)

### Visual Layout

Each timeline item displays like a social media post:

```
┌─────────────────────────────────────────┐
│ 🎯  Creator 1 • 2 ticks ago            │
│     OPTIMIZER  📝 5.2 posts             │
│                                         │
│     "Just posted new content! Check    │
│      it out and let me know what you   │
│      think. 🚀"                        │
│                                         │
│     ✨ Template Fallback  📊 15 words  │
└─────────────────────────────────────────┘
```

## Enabling Content Generation

### Option 1: Enable in Code

To enable text generation for the timeline, modify the tick endpoint:

```python
# In routes/dashboard.py or wherever tick is handled
from simulation.environment import GLOBAL_ENVIRONMENT

# Enable text generation
GLOBAL_ENVIRONMENT.tick(generate_text_content=True)
```

### Option 2: Add Toggle to UI

You can add a toggle button to the dashboard:

```python
# In ui/pages/dashboard.py
Button(
    "🤖 Generate Content",
    hx_post="/api/tick?generate_content=true",
    hx_target="#main-content",
    hx_swap="outerHTML",
    cls="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
)
```

Then update the tick route:

```python
# In routes/api_tick.py
@app.post("/api/tick")
def tick(request):
    generate_content = request.query_params.get("generate_content") == "true"
    GLOBAL_ENVIRONMENT.tick(generate_text_content=generate_content)
    return DashboardPage()
```

### Option 3: Always Enable (for Demo)

For demo purposes, you can always enable it:

```python
# In simulation/environment.py, modify the tick method default
def tick(self, generate_text_content=True):  # Changed from False to True
    # ... rest of method
```

## Content Generation Methods

The timeline will show which method was used to generate content:

### 1. Hugging Face (with API key)
- **Display**: "✨ Huggingface"
- **Quality**: High-quality, AI-generated posts
- **Requires**: `HUGGINGFACE_API_KEY` environment variable

### 2. Template Fallback (no API key)
- **Display**: "✨ Template Fallback"
- **Quality**: Template-based, contextual posts
- **Requires**: Nothing (always available)

## Example Timeline Output

With content generation enabled:

```
📱 Content Timeline
Live feed of creator posts and activity

┌─────────────────────────────────────────┐
│ ⚡  Creator 3 • just now                │
│     HUSTLER  📝 7.8 posts               │
│                                         │
│     "Working on something exciting     │
│      today. Stay tuned for updates!    │
│      🔥"                                │
│                                         │
│     ✨ Template Fallback  📊 12 words  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 🎯  Creator 1 • 1 tick ago             │
│     OPTIMIZER  📝 5.2 posts             │
│                                         │
│     "Just finished working on content  │
│      strategy. Excited to share! ✨"   │
│                                         │
│     ✨ Huggingface  📊 18 words        │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 🔥  Creator 2 • 2 ticks ago            │
│     BURNOUT  📝 2.1 posts               │
│                                         │
│     reduced activity due to exhaustion │
│                                         │
└─────────────────────────────────────────┘
```

## Implementation Details

### Data Flow

1. **Tick Execution** → `Environment.tick(generate_text_content=True)`
2. **Content Generation** → `generate_agent_content(agent)` for each agent
3. **Storage** → Content stored in `agent._current_tick_content`
4. **Display** → Activity feed reads from agent history and `_current_tick_content`

### Activity Feed Updates

The activity feed now:
- Checks for `_current_tick_content` attribute on agents
- Displays generated content if available
- Falls back to activity descriptions if no content
- Shows content metadata (method, word count)

### Styling

Timeline items use:
- **Gray background** (`bg-gray-750`) for cards
- **Darker inset** (`bg-gray-800`) for content text
- **Italic text** for generated content
- **State-based colors** for badges
- **Emoji indicators** for states and metadata

## Testing

### Quick Test

1. **Start the simulation**:
   ```bash
   make dev
   ```

2. **Load a scenario** (e.g., "Creator-First Platform")

3. **Enable content generation** (see options above)

4. **Run a few ticks** and watch the timeline populate

5. **Check the timeline** for generated posts

### Expected Behavior

- **With HF API key**: Rich, varied content from GPT-2
- **Without API key**: Template-based contextual posts
- **No content generation**: Activity descriptions only

## Customization

### Change Timeline Length

In `activity_feed.py`:

```python
# Show more/fewer items
activities = activities[:20]  # Changed from 10 to 20
```

### Adjust Content Display

Modify the content card styling:

```python
P(
    content_text,
    cls="text-sm text-gray-300 leading-relaxed mb-3 p-4 bg-gray-800 rounded-lg border-2 border-purple-700"
    # Customize: padding, background, border
)
```

### Add Engagement Metrics

You can extend the timeline to show likes, views, etc.:

```python
Div(
    Span(f"👁️ {views:,} views", cls="text-xs text-gray-500 mr-3"),
    Span(f"❤️ {likes:,} likes", cls="text-xs text-gray-500"),
    cls="flex items-center text-xs mt-2"
)
```

## Troubleshooting

### No Content Showing

**Issue**: Timeline shows activity descriptions instead of generated content

**Solutions**:
1. Verify `generate_text_content=True` in tick call
2. Check that `huggingface-hub` is installed: `uv sync`
3. Confirm agents have `_current_tick_content` attribute

### Content Not Updating

**Issue**: Same content appears for multiple ticks

**Solution**: Content is stored per tick. Make sure you're running new ticks, not refreshing the page.

### Performance Issues

**Issue**: Timeline loads slowly with many agents

**Solutions**:
1. Reduce timeline length (show fewer items)
2. Disable content generation for non-visible agents
3. Use template fallback instead of HF API

## Future Enhancements

Potential additions to the timeline:

1. **Engagement Simulation**
   - Simulated likes, comments, shares
   - Engagement rates based on content quality

2. **Content Filtering**
   - Filter by agent
   - Filter by state
   - Search content

3. **Infinite Scroll**
   - Load more items on scroll
   - Pagination

4. **Export Timeline**
   - Download as JSON
   - Export to CSV
   - Generate report

5. **Real-time Updates**
   - WebSocket integration
   - Live content streaming
   - Notification badges

## Related Documentation

- [HF Integration Guide](../docs/HF_INTEGRATION_GUIDE.md)
- [Content Generator API](../simulation/content_generator.py)
- [Activity Feed Component](../ui/components/activity_feed.py)
