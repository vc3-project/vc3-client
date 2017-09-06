#!/bin/bash -xe
CLIENT=vc3-client
CONFIG=/etc/vc3/vc3-client.conf
#CONFIG=~/git/vc3-client/etc/vc3-client.conf
#CONFIG=~/vc3/etc/vc3-client.conf

# DEFAULT values
DEBUG=0
DEBUGS=""

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

# Only one nodeset per cluster for now. Just workers..
$CLIENT $DEBUGS -c $CONFIG nodeset-create --owner lincolnb --node_number 10 --app_type htcondor --app_role worker-nodes --environment condorglidein-env1 htcondor-workers-1

# virtual cluster holder
$CLIENT $DEBUGS -c $CONFIG cluster-create --owner lincolnb htcondor-10workers

# Add nodeset to cluster
$CLIENT $DEBUGS -c $CONFIG cluster-addnodeset htcondor-10workers htcondor-workers-1
