# Test Suite

Automated tests for the Platform Capitalism Simulation.

---

## Running Tests

### Quick Test (Pytest)
```bash
make test
```

### Manual Validation Script
```bash
make test-manual
```

### With Coverage
```bash
make test-coverage
```

---

## Test Structure

### `test_simulation.py` (Pytest Suite)
Automated pytest tests covering:

- **Content Generation** - Post generation, history tracking
- **Policy Engine** - Reward calculations, presets
- **Environment** - State management, tick integration
- **Scenarios** - Loading, switching scenarios
- **Integration** - End-to-end simulation runs
- **CPM Economics** - Earnings calculations

### `validate_simulation.py` (Manual Script)
Legacy validation script with detailed output.

---

## Test Coverage

Current test coverage:

| Module | Coverage |
|--------|----------|
| `simulation/agents/` | ✅ Core functionality |
| `simulation/policy_engine/` | ✅ All presets |
| `simulation/environment.py` | ✅ Full lifecycle |
| `simulation/scenarios.py` | ✅ All scenarios |

---

## CI/CD

Tests run automatically on:
- Push to `main` branch
- Pull requests

See `.github/workflows/ci.yml` for configuration.

---

## Writing New Tests

### Example Test

```python
def test_new_feature():
    """Test description."""
    agent = Agent(AgentProfile(id=1))
    env = Environment(agents=[agent])
    
    # Test setup
    env.tick()
    
    # Assertions
    assert len(agent.history) > 0
    assert "new_metric" in agent.history[-1]
```

### Test Organization

- **Class-based:** Group related tests in classes
- **Descriptive names:** `test_what_it_does`
- **One assertion per test:** Keep tests focused
- **Use fixtures:** For complex setup (see pytest docs)

---

## Debugging Failed Tests

```bash
# Run specific test
pytest tests/test_simulation.py::TestContentGeneration::test_works_with_empty_history -v

# Show print statements
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -x

# Run last failed tests
pytest tests/ --lf
```

---

## Adding Tests to CI

Tests automatically run in GitHub Actions. To add new test files:

1. Create `test_*.py` in `tests/` directory
2. Follow pytest naming conventions
3. Push to GitHub - CI runs automatically

---

## Test Dependencies

Installed via `pyproject.toml`:
- `pytest>=7.4.0` - Test framework
- `ruff>=0.1.0` - Linting (optional in CI)

---

## Future Test Additions

Potential areas for expansion:

- [ ] UI component tests (FastHTML routes)
- [ ] API endpoint tests (HTMX interactions)
- [ ] Performance benchmarks
- [ ] Load testing for research deployments
- [ ] Mobile app integration tests (when implemented)

---

**All tests passing?** ✅ You're good to deploy!
