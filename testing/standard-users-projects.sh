#!/bin/bash -xe
CLIENT=vc3-client
CONFIG=/etc/vc3/vc3-client.conf
#CONFIG=~/git/vc3-client/etc/vc3-client.conf
#CONFIG=~/vc3/etc/vc3-client.conf

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

# Users
$CLIENT $DEBUGS -c $CONFIG user-create --firstname Lincoln --lastname Bryant --email lincolnb@uchicago.edu --institution UChicago lincolnb
$CLIENT $DEBUGS -c $CONFIG project-create --owner lincolnb --members lincolnb lincolnb

$CLIENT $DEBUGS -c $CONFIG user-create --firstname Benedikt --lastname Riedel --email briedel@uchicago.edu --institution UChicago briedel
$CLIENT $DEBUGS -c $CONFIG project-create --owner briedel --members briedel briedel

$CLIENT $DEBUGS -c $CONFIG user-create --firstname Judith --lastname Stephen --email jlstephen@uchicago.edu --institution UChicago jlstephen
$CLIENT $DEBUGS -c $CONFIG project-create --owner jlsteven --members jlsteven jlsteven

$CLIENT $DEBUGS -c $CONFIG user-create --firstname Suchandra --lastname Thapa --email ssthapa@uchicago.edu --institution UChicago ssthapa
$CLIENT $DEBUGS -c $CONFIG project-create --owner ssthapa --members ssthapa ssthapa

$CLIENT $DEBUGS -c $CONFIG user-create --firstname Jose --lastname Caballero --email caballero@bnl.gov --institution BrookhavenNationalLab caballero
$CLIENT $DEBUGS -c $CONFIG project-create --owner caballero --members caballero caballero

$CLIENT $DEBUGS -c $CONFIG user-create --firstname Jeremy --lastname Van --email jeremyvan@uchicago --institution UChicago jeremyvan
$CLIENT $DEBUGS -c $CONFIG project-create --owner jeremyvan --members jeremyvan jeremyvan

$CLIENT $DEBUGS -c $CONFIG user-create --firstname Ben --lastname Tovar --email btovar@nd.edu --institution NotreDame btovar
$CLIENT $DEBUGS -c $CONFIG project-create --owner btovar --members btovar btovar

$CLIENT $DEBUGS -c $CONFIG user-create --firstname Rob --lastname Gardner --email rwg@uchicago.edu --institution UChicago rwg
$CLIENT $DEBUGS -c $CONFIG project-create --owner rwg --members rwg rwg


# New group project
$CLIENT $DEBUGS -c $CONFIG project-create --owner lincolnb --members lincolnb,briedel SouthPoleTelescope

