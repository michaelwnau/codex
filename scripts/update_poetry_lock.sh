#!/bin/bash
# Stop on the first sign of trouble
set -e
# Update the Poetry lock file
poetry lock --no-update
# Add the updated lock file to the commit
git add poetry.lock
