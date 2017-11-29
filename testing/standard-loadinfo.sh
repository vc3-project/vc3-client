#!/bin/bash -e

./standard-users-projects.sh "$@"
./standard-resources.sh "$@"
./standard-environments.sh "$@"
./standard-clusters.sh "$@"
./standard-allocations.sh "$@"
