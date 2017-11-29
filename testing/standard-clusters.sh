#!/bin/bash
source ./standard-common-config.sh

# Only one nodeset per cluster for now. Just workers..
RUN_CHECK_CLIENT nodeset-create --owner lincolnb --node_number 10 --app_type htcondor --app_role worker-nodes htcondor-workers-1

# virtual cluster holder
RUN_CHECK_CLIENT cluster-create --owner lincolnb htcondor-10workers

# Add nodeset to cluster
RUN_CHECK_CLIENT cluster-addnodeset htcondor-10workers htcondor-workers-1
