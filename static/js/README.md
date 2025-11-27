# JavaScript Files

This directory contains external JavaScript files for the Platform Capitalism simulation UI.

## Files

### `charts.js`
Main chart initialization utilities using Chart.js:
- `initAgentDistributionPie()` - Pie chart for agent state distribution
- `initArousalTrendChart()` - Line chart for arousal trends over time
- `initRewardTimelineChart()` - Line chart with mean line for reward distribution

### `agent-sparklines.js`
Small inline charts for individual agent metrics:
- `initBurnoutSparkline()` - Burnout history sparkline
- `initRewardSparkline()` - Reward history sparkline

### `tabs.js`
Tab switching functionality for agent cards:
- `initAgentTabs()` - Handles switching between metrics and decision tree views
- Auto-initializes on page load

## Usage

These files are automatically included in the page layout via `ui/components/layout.py`.

Python components call JavaScript functions with inline Script tags that pass data:

```python
Script(f"""
    initAgentDistributionPie('canvasId', {labels}, {data}, {colors});
""")
```

## Benefits

- **Cleaner Python code**: No large inline JavaScript blocks
- **Reusability**: Functions can be called from multiple components
- **Maintainability**: Easier to debug and update JavaScript separately
- **Caching**: Browser can cache external JS files
- **IDE support**: Better syntax highlighting and linting for JavaScript
