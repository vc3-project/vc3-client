#!/bin/bash
DEBUG='-d'
CLIENT=~/git/vc3-client/vc3client/clientcli.py
CONFIG=~/git/vc3-client/etc/vc3-client.conf

echo $CLIENT -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover
$CLIENT -c $CONFIG user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover
echo $CLIENT -c $CONFIG user-create --firstname Angus --lastname MacGuyver --email angus@bnl.gov --institution BNL angus
$CLIENT -c $CONFIG user-create --firstname Angus --lastname MacGuyver --email angus@bnl.gov --institution BNL angus

echo $CLIENT -c $CONFIG project-create --owner jhover --members jhover  jhoverproject
$CLIENT -c $CONFIG project-create --owner jhover --members jhover  jhoverproject
echo $CLIENT -c $CONFIG project-adduser jhoverproject angus
$CLIENT -c $CONFIG project-adduser jhoverproject angus

echo $CLIENT -c $CONFIG project-list --project jhoverproject
$CLIENT -c $CONFIG project-list --project jhoverproject

