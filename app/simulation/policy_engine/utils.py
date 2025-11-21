import random

def variable_ratio_reward(base, ratio=5):
    """Simulate variable ratio reinforcement (e.g., slot-machine style)."""
    return base * random.randint(1, ratio)


def variable_interval_reward(base, max_interval=10):
    """Simulate variable interval reinforcement (time-based)."""
    return base * (random.random() * max_interval)