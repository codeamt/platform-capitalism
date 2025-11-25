# Testing

## Run Tests

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run manual validation
make test-manual
```

## Test Structure

- `tests/test_simulation.py` - Automated pytest suite
- `tests/validate_simulation.py` - Manual validation script

## What's Tested

- Agent state transitions
- Reward calculations
- Content generation
- CPM earnings accuracy
- Burnout accumulation
- Scenario loading

See the [README](../../README.md#testing) for more details.
