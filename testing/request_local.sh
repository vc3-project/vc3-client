#!/bin/bash -x
#
# VC3 Client Test 
#

set -xe

export PATH=$PATH:~/.local/bin

CLIENT=vc3-client
#CONFIG=/etc/vc3/vc3-client.conf
CONFIG=~/git/vc3-client/etc/vc3-client.conf
#CONFIG=~/vc3/etc/vc3-client.conf


# DEFAULT values
DEBUG=0
DEBUGS=""

CONDOR_COLLECTOR=condor.virtualclusters.org

# read the options
ARGS=`getopt -o d -l debug -- "$@"`  
eval set -- "$ARGS"

# extract options and their arguments into variables.
while true ; do
    case "$1" in
        -d|--debug) DEBUG=1 ; shift ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
    esac
done

# set variables accordingly...
if [ "$DEBUG" = "1" ] ; then
   DEBUGS=" -d "
else
   DEBUGS=""
fi


# Users
$CLIENT $DEBUGS -c $CONFIG user-create --firstname Ben --lastname Tovar --email btovar@nd.edu --institution ND btovar

# New project
$CLIENT $DEBUGS -c $CONFIG project-create --owner btovar --members btovar NDWQ

# Create resource
$CLIENT $DEBUGS -c $CONFIG resource-create --owner btovar --accesstype local --accessmethod local condor-schedd-local

# Create allocation
$CLIENT $DEBUGS -c $CONFIG allocation-create --owner btovar --resource condor-schedd-local --accountname btovar btovar.condor-schedd-local

# Create environment
# $CLIENT $DEBUGS -c $CONFIG environment-create\
#     --owner      btovar\
#     --packages   vc3-glidein\
#     --extra-args='--home=.'\
#     --extra-args='--install=.'\
#     --extra-args='--sys python:2.7=/usr'\
#     --filesmap   '~/git/vc3-client/testing/mycondorpassword=mycondorpassword,~/git/vc3-client/testing/filea.txt=filea.txt'\
#     --command    "vc3-glidein -c ${CONDOR_COLLECTOR} -C ${CONDOR_COLLECTOR} -p mycondorpassword"\
#     btovar-env1
# 
$CLIENT $DEBUGS -c $CONFIG environment-create\
    --owner      btovar\
    --packages   cctools-statics\
    --extra-args='--home=.'\
    --extra-args='--install=.'\
    --command    "work_queue_worker -M vc3.btovar.project -t300"\
    btovar-env1


# Node set for the virtual cluster
$CLIENT $DEBUGS -c $CONFIG nodeset-create --owner btovar --node_number 2 --app_type workqueue --app_role worker-nodes --environment btovar-env1 wq-workers-1

# virtual cluster holder
$CLIENT $DEBUGS -c $CONFIG cluster-create --owner btovar wq-10workers

# Add nodeset to cluster
$CLIENT $DEBUGS -c $CONFIG cluster-addnodeset wq-10workers wq-workers-1

# Create request
$CLIENT $DEBUGS -c $CONFIG request-create --owner btovar --cluster wq-10workers --allocations btovar.condor-schedd-local request_local

# Terminate a request
# $CLIENT $DEBUGS -c $CONFIG request-terminate --requestname september-demo-request
