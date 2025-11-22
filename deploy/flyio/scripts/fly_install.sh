#!/bin/bash
curl -L https://fly.io/install.sh | sh

chmod +x scripts/deploy.sh
./scripts/fly_deploy.sh

flyctl open
flyctl logs