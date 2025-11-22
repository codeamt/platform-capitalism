#!/bin/bash
# Dynamic scaling script for Fly.io

# Get current load from metrics endpoint
LOAD=$(curl -s <http://localhost:9100/metrics> | grep 'simulation_agents' | awk '{print $2}')

# Scale rules
if (( $(echo "$LOAD > 5000" | bc -l) )); then
    SCALE_TO=3
elif (( $(echo "$LOAD > 2000" | bc -l) )); then
    SCALE_TO=2
else
    SCALE_TO=1
fi

# Execute scaling
flyctl scale count $SCALE_TO --app platform-capitalism-sim --yes

echo "Scaled to $SCALE_TO instances based on $LOAD agents"