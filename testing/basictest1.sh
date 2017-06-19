#!/bin/bash
DEBUG='-d'
CLIENT=~/git/vc3-client/vc3client/clientcli.py
CONFIG=~/git/vc3-client/etc/vc3-client.conf

echo $CLIENT $DEBUG -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover
$CLIENT $DEBUG -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover
echo $CLIENT $DEBUG -c $CONFIG user-create --firstname Angus --lastname MacGuyver --email angus@bnl.gov --institution BNL angus
$CLIENT $DEBUG -c $CONFIG user-create --firstname Angus --lastname MacGuyver --email angus@bnl.gov --institution BNL angus
echo $CLIENT $DEBUG -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL adminjhover
$CLIENT $DEBUG -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL adminjhover

echo $CLIENT $DEBUG -c $CONFIG user-list
$CLIENT $DEBUG -c $CONFIG user-list

echo $CLIENT $DEBUG -c $CONFIG project-create --owner jhover --members jhover  jhoverproject
$CLIENT $DEBUG -c $CONFIG project-create --owner jhover --members jhover  jhoverproject
echo $CLIENT $DEBUG -c $CONFIG project-adduser jhoverproject angus
$CLIENT $DEBUG -c $CONFIG project-adduser jhoverproject angus

echo $CLIENT $DEBUG -c $CONFIG project-list
$CLIENT $DEBUG -c $CONFIG project-list

echo $CLIENT $DEBUG -c $CONFIG project-list --project jhoverproject
$CLIENT $DEBUG -c $CONFIG project-list --project jhoverproject

echo $CLIENT $DEBUG -c $CONFIG resource-create  --owner adminjhover --accesstype remote-batch --accessmethod ssh --accessflavor slurm   sdcc-ic
$CLIENT $DEBUG -c $CONFIG resource-create  --owner adminjhover --accesstype remote-batch --accessmethod ssh --accessflavor slurm sdcc-ic

echo $CLIENT $DEBUG -c $CONFIG resource-list
$CLIENT $DEBUG -c $CONFIG resource-list

echo $CLIENT $DEBUG -c $CONFIG resource-list --resource sdcc-ic
$CLIENT $DEBUG -c $CONFIG resource-list --resource sdcc-ic

echo $CLIENT $DEBUG -c $CONFIG allocation-create --owner jhover --resource sdcc-ic --accountname jhover  jhover.sdcc-ic
$CLIENT $DEBUG -c $CONFIG allocation-create --owner jhover --resource sdcc-ic --accountname jhover jhover.sdcc-ic

echo $CLIENT $DEBUG -c $CONFIG allocation-list
$CLIENT $DEBUG -c $CONFIG allocation-list


