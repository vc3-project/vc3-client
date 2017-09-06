#!/bin/bash -xe
./standard-users-projects.sh
./standard-resources.sh
./standard-environments.sh
# standard-clusters depends on environments
./standard-clusters.sh
./standard-allocations.sh



