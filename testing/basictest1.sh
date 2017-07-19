#!/bin/bash
#
# VC3 Client Test 
#
CLIENT=~/git/vc3-client/vc3client/clientcli.py
CONFIG=~/git/vc3-client/etc/vc3-client.conf


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


echo $CLIENT $DEBUGS -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover
$CLIENT $DEBUGS -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover
echo $CLIENT $DEBUGS -c $CONFIG user-create --firstname Angus --lastname MacGuyver --email angus@bnl.gov --institution BNL angus
$CLIENT $DEBUGS -c $CONFIG user-create --firstname Angus --lastname MacGuyver --email angus@bnl.gov --institution BNL angus
echo $CLIENT $DEBUGS -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL adminjhover
$CLIENT $DEBUGS -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL adminjhover

echo $CLIENT $DEBUGS -c $CONFIG user-list
$CLIENT $DEBUGS -c $CONFIG user-list

echo $CLIENT $DEBUGS -c $CONFIG project-create --owner angus --members angus  angusproject
$CLIENT $DEBUGS -c $CONFIG project-create --owner angus --members angus  angusproject
echo $CLIENT $DEBUGS -c $CONFIG project-create --owner jhover --members jhover  jhoverproject
$CLIENT $DEBUGS -c $CONFIG project-create --owner jhover --members jhover  jhoverproject
echo $CLIENT $DEBUGS -c $CONFIG project-adduser jhoverproject angus
$CLIENT $DEBUGS -c $CONFIG project-adduser jhoverproject angus

echo $CLIENT $DEBUGS -c $CONFIG project-li st
$CLIENT $DEBUGS -c $CONFIG project-list

echo $CLIENT $DEBUGS -c $CONFIG project-list --project jhoverproject
$CLIENT $DEBUGS -c $CONFIG project-list --project jhoverproject

echo $CLIENT $DEBUGS -c $CONFIG resource-create  --owner adminjhover --accesstype remote-batch --accessmethod ssh --accessflavor slurm   sdcc-ic
$CLIENT $DEBUGS -c $CONFIG resource-create  --owner adminjhover --accesstype remote-batch --accessmethod ssh --accessflavor slurm sdcc-ic

echo $CLIENT $DEBUGS -c $CONFIG resource-list
$CLIENT $DEBUGS -c $CONFIG resource-list

echo $CLIENT $DEBUGS -c $CONFIG resource-list --resource sdcc-ic
$CLIENT $DEBUGS -c $CONFIG resource-list --resource sdcc-ic

echo $CLIENT $DEBUGS -c $CONFIG allocation-create --owner jhover --resource sdcc-ic --accountname jhover  jhover.sdcc-ic
$CLIENT $DEBUGS -c $CONFIG allocation-create --owner jhover --resource sdcc-ic --accountname jhover jhover.sdcc-ic

echo $CLIENT $DEBUGS -c $CONFIG allocation-list
$CLIENT $DEBUGS -c $CONFIG allocation-list

echo $CLIENT $DEBUGS -c $CONFIG nodeset-create --owner jhover --node_number 1 --app_type htcondor --app_role head-node htcondor-head.1
$CLIENT $DEBUGS -c $CONFIG nodeset-create --owner jhover --node_number 1 --app_type htcondor --app_role head-node htcondor-head.1

echo $CLIENT $DEBUGS -c $CONFIG nodeset-list
$CLIENT $DEBUGS -c $CONFIG nodeset-list




