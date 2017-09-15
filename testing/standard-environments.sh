#!/bin/bash -xe
CLIENT=vc3-client
CONFIG=/etc/vc3/vc3-client.conf
#CONFIG=~/git/vc3-client/etc/vc3-client.conf
#CONFIG=~/vc3/etc/vc3-client.conf
CONDOR_COLLECTOR=condor-dev.virtualclusters.org

# DEFAULT values
DEBUG=0
DEBUGS=""

#######################################################

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

# Create environment
# below is likely wrong, as the file mappings go to /etc. Most likely, that will result in a permission denied error when writing the file.
# $CLIENT $DEBUGS -c $CONFIG environment-create --owner lincolnb --filesmap "~/git/vc3-client/testing/filea.txt=/etc/filea.txt,~/git/vc3-client/testing/fileb.txt=/etc/fileb.txt" lincolnb-env1
#$CLIENT $DEBUGS -c $CONFIG environment-create\
#    --owner      lincolnb\
#    --packages   vc3-glidein\
#    --extra-args='--home=.'\
#    --extra-args='--install=.'\
#    --extra-args='--sys python:2.7=/usr'\
#    --filesmap   '~/git/vc3-client/testing/mycondorpassword=mycondorpassword'\
#    --command    "vc3-glidein -c ${CONDOR_COLLECTOR} -C ${CONDOR_COLLECTOR} -p mycondorpassword"\
#    condorglidein-env1

PASSWORD_REMOTE_NAME=mycondorpassword
$CLIENT $DEBUGS -c $CONFIG environment-create\
    --owner      lincolnb\
    --envvar     VC3_CONDOR_PASSWORD_FILE=${PASSWORD_REMOTE_NAME}\
    --filesmap   "~/git/vc3-client/testing/mycondorpassword=${PASSWORD_REMOTE_NAME}"\
    condor-glidein-password-env1
