#!/bin/bash -x
#
# VC3 Client Test 
#

export PATH=$PATH:~/.local/bin

CLIENT=vc3-client
#CONFIG=/etc/vc3/vc3-client.conf
CONFIG=~/vc3/etc/vc3-client.conf


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


# Users
$CLIENT $DEBUGS -c $CONFIG user-create --firstname Lincoln --lastname Bryant --email lincolnb@uchicago.edu --institution UChicago lincolnb
$CLIENT $DEBUGS -c $CONFIG user-create --firstname Benedikt --lastname Riedel --email briedel@uchicago.edu --institution UChicago briedel
$CLIENT $DEBUGS -c $CONFIG user-create --firstname Judith --lastname Stephen --email jlstephen@uchicago.edu --institution UChicago jlstephen

# New project
$CLIENT $DEBUGS -c $CONFIG project-create --owner lincolnb --members lincolnb,briedel SPT

# add user to existing project
$CLIENT $DEBUGS -c $CONFIG project-adduser SPT jlstephen

# Create resource
$CLIENT $DEBUGS -c $CONFIG resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor slurm --accesshost midway-login1.rcc.uchicago.edu --accessport 22 uchicago-midway
$CLIENT $DEBUGS -c $CONFIG resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor condor --accesshost condor.grid.uchicago.edu --accessport 22 uchicago-coreos
$CLIENT $DEBUGS -c $CONFIG resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor slurm --accesshost cori.nersc.gov --accessport 22 nersc-cori

# Create allocation
$CLIENT $DEBUGS -c $CONFIG allocation-create --owner lincolnb --resource uchicago-midway --accountname lincolnb lincolnb.uchicago-midway
$CLIENT $DEBUGS -c $CONFIG allocation-create --owner lincolnb --resource uchicago-coreos --accountname lincolnb lincolnb.uchicago-coreos
$CLIENT $DEBUGS -c $CONFIG allocation-create --owner lincolnb --resource nersc-cori --accountname briedel briedel.nersc-cori

# Node set for the virtual cluster
# Only one nodeset per cluster for now. Just workers..
#$CLIENT $DEBUGS -c $CONFIG nodeset-create --owner lincolnb --node_number 1 --app_type htcondor --app_role head-node htcondor-head-1
$CLIENT $DEBUGS -c $CONFIG nodeset-create --owner lincolnb --node_number 10 --app_type htcondor --app_role worker-nodes htcondor-workers-1

# virtual cluster holder
$CLIENT $DEBUGS -c $CONFIG cluster-create --owner lincolnb htcondor-10workers

# Add nodeset to cluster
$CLIENT $DEBUGS -c $CONFIG cluster-addnodeset htcondor-workers-1 htcondor-10workers

# Create environment
$CLIENT $DEBUGS -c $CONFIG environment-create --owner lincolnb --filesmap "~/git/vc3-client/testing/filea.txt=/etc/filea.txt,~/git/vc3-client/testing/fileb.txt=/etc/fileb.txt" lincolnb-env1

# List environments
#$CLIENT $DEBUGS -c $CONFIG environment-list

# Create request
$CLIENT $DEBUGS -c $CONFIG request-create --owner lincolnb --cluster htcondor-10workers --allocations lincolnb.uchicago-midway,lincolnb.uchicago-coreos --environments lincolnb-env1 september-demo-request




