#!/bin/bash
DEBUG='-d'
CLIENT=~/git/vc3-client/vc3client/clientcli.py
CONFIG=~/git/vc3-client/etc/vc3-client.conf

echo $CLIENT -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover
$CLIENT -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover
echo $CLIENT -c $CONFIG user-create --firstname Angus --lastname MacGuyver --email angus@bnl.gov --institution BNL angus
$CLIENT -c $CONFIG user-create --firstname Angus --lastname MacGuyver --email angus@bnl.gov --institution BNL angus
echo $CLIENT -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL adminjhover
$CLIENT -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL adminjhover

echo $CLIENT -c $CONFIG user-list
$CLIENT -c $CONFIG user-list

echo $CLIENT -c $CONFIG project-create --owner jhover --members jhover  jhoverproject
$CLIENT -c $CONFIG project-create --owner jhover --members jhover  jhoverproject
echo $CLIENT -c $CONFIG project-adduser jhoverproject angus
$CLIENT -c $CONFIG project-adduser jhoverproject angus

echo $CLIENT -c $CONFIG project-list
$CLIENT -c $CONFIG project-list

echo $CLIENT -c $CONFIG project-list --project jhoverproject
$CLIENT -c $CONFIG project-list --project jhoverproject

echo $CLIENT -c $CONFIG resource-create  --owner adminjhover --accesstype remote-batch --accessmethod ssh --accessflavor slurm   sdcc-ic
$CLIENT -c $CONFIG resource-create  --owner adminjhover --accesstype remote-batch --accessmethod ssh --accessflavor slurm sdcc-ic

echo $CLIENT -c $CONFIG resource-list
$CLIENT -c $CONFIG resource-list

echo $CLIENT -c $CONFIG resource-list --resource sdcc-ic
$CLIENT -c $CONFIG resource-list --resource sdcc-ic

echo $CLIENT -c $CONFIG allocation-create --owner jhover --resource sdcc-ic --accountname jhover  jhover.sdcc-ic
$CLIENT -c $CONFIG allocation-create --owner jhover --resource sdcc-ic --accountname jhover jhover.sdcc-ic

echo $CLIENT -c $CONFIG allocation-list
$CLIENT -c $CONFIG allocation-list


