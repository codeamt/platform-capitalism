# Manual UI Testing Checklist

This checklist covers manual testing of the UI components and user workflows.

## Pre-Testing Setup

- [ ] Start the application: `python main.py`
- [ ] Open browser to `http://localhost:5001`
- [ ] Verify the app loads without errors

---

## Dashboard Page Tests

### Initial Load

- [ ] Dashboard loads with default "Creator-First Platform" scenario
- [ ] Status bar shows: Tick 0, 5 Agents
- [ ] All three tabs are visible: 🎮 Simulation, 👥 Agents, 📊 System Health

### Tab 1: Simulation

- [ ] Scenario selector displays current scenario
- [ ] Recent Activity shows "No activity yet" message
- [ ] Can select different scenarios from dropdown
- [ ] Selecting a scenario updates the page without full reload (HTMX)

### Tab 2: Agents

- [ ] Agent cards display in a slider/carousel
- [ ] Each card shows: Agent ID, status, state, strategy
- [ ] Wellbeing metrics display with progress bars
- [ ] Content traits show quality, diversity, consistency values
- [ ] Cards have consistent height (not growing indefinitely)

### Tab 3: System Health

- [ ] Agent Distribution pie chart displays
- [ ] Arousal Trend chart displays (empty initially)
- [ ] Charts have proper labels and legends

### Running Simulation

- [ ] Click "▶️ Run Tick" button
- [ ] Status bar updates to Tick 1
- [ ] Recent Activity populates with agent actions
- [ ] Agent cards update with new metrics
- [ ] Sparkline charts appear in agent cards (after 2+ ticks)
- [ ] System Health charts update with data points
- [ ] Run 5+ ticks and verify:
  - [ ] Charts persist (don't disappear)
  - [ ] Activity feed scrolls (max 10 items visible)
  - [ ] Arousal trend shows multiple data points

### Reset Functionality

- [ ] Click "🔄 Reset" button
- [ ] Tick count returns to 0
- [ ] All agent histories clear
- [ ] Charts reset
- [ ] Activity feed clears

---

## Governance Lab Page Tests

### Initial Load

- [ ] Navigate to "Governance Lab" from nav bar
- [ ] Page loads with two-column layout
- [ ] Left column shows: Scenario Selector, Transparency Panel
- [ ] Right column shows: Policy Parameters form

### Scenario Selector

- [ ] Current scenario is highlighted
- [ ] Scenarios grouped by type (Exploitative, Sustainable, Hybrid)
- [ ] Selecting a scenario updates the page
- [ ] Policy parameters update to match scenario
- [ ] Transparency panel updates

### Transparency Panel

- [ ] Displays current policy metrics in a table
- [ ] Table takes full width of container
- [ ] Shows: Quality Weight, Diversity Weight, Consistency Weight, Volatility Weight
- [ ] Values formatted to 2 decimal places
- [ ] Shows count of last tick explanations

### Policy Parameters

- [ ] Form displays current mode badge (Differential/Intermittent/Hybrid)
- [ ] Policy Impact Preview shows:
  - [ ] Creator Health rating
  - [ ] Predictability percentage
  - [ ] Reward Focus value
  - [ ] Wellbeing Support value
- [ ] All parameter inputs display current values
- [ ] Reward Weights section: Quality, Diversity, Consistency, Break
- [ ] Creator Wellbeing section: Burnout Penalty, Sustainability Bonus, Baseline Guarantee
- [ ] Intermittent Parameters section (only visible for intermittent/hybrid modes)

### Updating Policy

- [ ] Change a parameter value (e.g., Quality Weight from 0.3 to 0.5)
- [ ] Click "Update Policy" button
- [ ] Page updates without full reload (HTMX)
- [ ] Policy Impact Preview recalculates
- [ ] Transparency Panel reflects new values
- [ ] Scenario selector remains on current scenario (doesn't reset)

### Scenario Switching

- [ ] Load "Creator-First Platform"
- [ ] Note the policy parameters
- [ ] Switch to "Algorithmic Slot Machine"
- [ ] Verify policy parameters change dramatically
- [ ] Verify mode badge changes
- [ ] Verify Intermittent Parameters section appears
- [ ] Switch back to "Creator-First Platform"
- [ ] Verify parameters restore correctly

---

## Cross-Page Tests

### Navigation

- [ ] Click "Dashboard" in nav bar from Governance Lab
- [ ] Dashboard loads with updated policy
- [ ] Click "Governance Lab" from Dashboard
- [ ] Returns to Governance Lab

### State Persistence

- [ ] Load a scenario on Dashboard
- [ ] Navigate to Governance Lab
- [ ] Verify same scenario is selected
- [ ] Modify policy parameters
- [ ] Navigate to Dashboard
- [ ] Run a tick
- [ ] Verify simulation uses updated policy

### HTMX Interactions

- [ ] All form submissions update content without page reload
- [ ] Loading states appear briefly (if visible)
- [ ] No console errors during HTMX requests
- [ ] Browser back/forward buttons work correctly

---

## Chart Persistence Tests

### Agent Card Sparklines

- [ ] Run 3 ticks
- [ ] Navigate to Agents tab
- [ ] Verify sparklines appear
- [ ] Run 2 more ticks
- [ ] Verify sparklines update (don't disappear)
- [ ] Charts show last 10 ticks of data

### Dashboard Charts

- [ ] Run 5 ticks
- [ ] Navigate to System Health tab
- [ ] Verify both charts display
- [ ] Run 3 more ticks
- [ ] Verify charts update smoothly
- [ ] Charts don't flicker or disappear
- [ ] Data points accumulate correctly

---

## Responsive Design Tests

### Desktop (1920x1080)

- [ ] Two-column layouts display side-by-side
- [ ] Charts have appropriate sizes
- [ ] No horizontal scrolling

### Tablet (768x1024)

- [ ] Layouts adapt appropriately
- [ ] Navigation remains accessible
- [ ] Forms remain usable

### Mobile (375x667)

- [ ] Columns stack vertically
- [ ] Text remains readable
- [ ] Buttons are tappable
- [ ] Charts scale appropriately

---

## Error Handling Tests

### Invalid Inputs

- [ ] Try entering negative values in policy parameters
- [ ] Try entering values > 1 for weights
- [ ] Verify validation prevents invalid submissions

### Network Errors

- [ ] Stop the server mid-session
- [ ] Try clicking buttons
- [ ] Verify graceful error handling

---

## Performance Tests

### Load Time

- [ ] Dashboard loads in < 2 seconds
- [ ] Governance Lab loads in < 2 seconds
- [ ] Page transitions feel instant

### Simulation Speed

- [ ] Single tick completes in < 500ms
- [ ] 10 consecutive ticks complete smoothly
- [ ] No noticeable lag or freezing

### Memory

- [ ] Run 50+ ticks
- [ ] Check browser memory usage (DevTools)
- [ ] Verify no memory leaks
- [ ] Charts don't accumulate indefinitely (20 tick limit)

---

## Browser Compatibility

Test in:

- [ ] Chrome/Chromium (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

---

## Accessibility Tests

### Keyboard Navigation

- [ ] Tab through all interactive elements
- [ ] Forms are fully keyboard accessible
- [ ] Focus indicators are visible

### Screen Reader

- [ ] Headings are properly structured
- [ ] Form labels are associated correctly
- [ ] Charts have appropriate aria labels

---

## Sign-Off

**Tester:** ___________________
**Date:** ___________________
**Browser/OS:** ___________________
**Result:** ⬜ PASS  ⬜ FAIL

**Notes:**

```__

```
