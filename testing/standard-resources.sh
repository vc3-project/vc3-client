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

# Create resource
$CLIENT $DEBUGS -c $CONFIG resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor slurm  --accesshost midway-login1.rcc.uchicago.edu --accessport 22 uchicago-midway
$CLIENT $DEBUGS -c $CONFIG resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor condor --accesshost condor.grid.uchicago.edu --accessport 22 uchicago-coreos
$CLIENT $DEBUGS -c $CONFIG resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor slurm  --accesshost cori.nersc.gov --accessport 22 nersc-cori

$CLIENT $DEBUGS -c $CONFIG resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor condor --accesshost pool.virtualclusters.org --accessport 22 vc3-test-pool

