#!/bin/bash
# Stop on the first sign of trouble
set -e

# Announce the start of the process
echo "Starting to update Poetry lock file..."

# Update the Poetry lock file
echo "Running 'poetry lock --no-update'..."
poetry lock --no-update
echo "'poetry lock --no-update' completed successfully."

# Add the updated lock file to the commit
echo "Adding the updated poetry.lock to the staging area..."
git add poetry.lock
echo "poetry.lock added to the staging area successfully."

# Final message
echo "Poetry lock file update completed successfully."
