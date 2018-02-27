#!/bin/bash
source ./standard-common-config.sh

# Node set
#Nodeset( name=lincolnb-htcondor-10-workers state=new owner=lincolnb node_number=10 app_type=htcondor app_role=worker-nodes cores=1 memory_mb=None storage_mb=None app_host=None app_port=None app_sectoken=None environment=None description=None displayname=htcondor-10-workers url=None docurl=None )
RUN_CHECK_CLIENT nodeset-create --owner lincolnb --node_number 10 --app_type htcondor --app_role worker-nodes --displayname="htcondor-10-workers-nodeset" lincolnb-htcondor-10-workers

# Cluster containing that nodeset
# Cluster( name=lincolnb-htcondor-10-workers state=new owner=lincolnb nodesets=[u'lincolnb-htcondor-10-workers'] description=10 HTCondor workers  displayname=htcondor-10-workers url=None docurl=None )
RUN_CHECK_CLIENT cluster-create --owner lincolnb --description "HTCondor with 10 Workers" --displayname="htcondor-10-workers" lincolnb-htcondor-10-workers --public

# Add the nodeset to the cluster
RUN_CHECK_CLIENT cluster-addnodeset lincolnb-htcondor-10-workers lincolnb-htcondor-10-workers


RUN_CHECK_CLIENT nodeset-create --owner btovar --node_number 1 --app_type htcondor --app_role worker-nodes --displayname="htcondor-1-worker-nodeset" btovar-htcondor-1-worker
RUN_CHECK_CLIENT cluster-create --owner btovar --description "HTCondor with 1 Worker" --displayname="htcondor-1-worker" btovar-htcondor-1-worker --public
RUN_CHECK_CLIENT cluster-addnodeset btovar-htcondor-1-worker btovar-htcondor-1-worker

RUN_CHECK_CLIENT nodeset-create --owner btovar --node_number 50 --app_type htcondor --app_role worker-nodes --displayname="htcondor-50-workers-nodeset" btovar-htcondor-50-workers
RUN_CHECK_CLIENT cluster-create --owner btovar --description "HTCondor with 50 Workers" --displayname="htcondor-50-workers" btovar-htcondor-50-workers --public
RUN_CHECK_CLIENT cluster-addnodeset btovar-htcondor-50-workers btovar-htcondor-50-workers

RUN_CHECK_CLIENT nodeset-create --owner btovar --node_number 1 --app_type workqueue --app_role worker-nodes --displayname="wq-1-worker-nodeset" btovar-wq-1-worker
RUN_CHECK_CLIENT cluster-create --owner btovar --description "WorkQueue with 1 Worker" --displayname="wq-1-worker" btovar-wq-1-worker --public
RUN_CHECK_CLIENT cluster-addnodeset btovar-wq-1-worker btovar-wq-1-worker

RUN_CHECK_CLIENT nodeset-create --owner btovar --node_number 50 --app_type workqueue --app_role worker-nodes --displayname="wq-50-workers-nodeset" btovar-wq-50-workers
RUN_CHECK_CLIENT cluster-create --owner btovar --description "WorkQueue with 50 Workers" --displayname="wq-50-workers" btovar-wq-50-workers --public
RUN_CHECK_CLIENT cluster-addnodeset btovar-wq-50-workers btovar-wq-50-workers

